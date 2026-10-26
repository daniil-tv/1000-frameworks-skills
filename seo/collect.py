#!/usr/bin/env python3
"""Collect Wordstat demand into reviewable, versioned GitHub artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
ENDPOINT = "https://searchapi.api.cloud.yandex.net/v2/wordstat/topRequests"
QUESTION = {"как", "что", "зачем", "почему", "когда", "какие", "какой", "сколько", "где"}
COMMERCIAL = {"купить", "заказать", "цена", "стоимость", "курс", "обучение"}
PRACTICAL = {"пример", "шаблон", "этапы", "метод", "интервью", "вопросы", "как"}


def classify(phrase: str) -> str:
    words = set(re.findall(r"[\wё]+", phrase.lower()))
    if words & COMMERCIAL:
        return "commercial"
    if words & QUESTION:
        return "question"
    if words & PRACTICAL:
        return "practical"
    return "informational"


def get_pages() -> dict[str, dict]:
    pages = json.loads((ROOT / "pages.json").read_text(encoding="utf-8"))["pages"]
    result = {}
    for page in pages:
        page_id = page["id"]
        if not re.fullmatch(r"[a-z0-9-]+", page_id) or page_id in result:
            raise ValueError(f"Invalid or duplicate page ID: {page_id}")
        if not page.get("seeds") or len(page["seeds"]) > 8:
            raise ValueError(f"Page {page_id} needs 1–8 seeds")
        result[page_id] = page
    return result


def fetch_top(phrase: str, region: str, api_key: str, folder_id: str) -> dict:
    body = {"phrase": phrase, "numPhrases": 300, "devices": ["DEVICE_ALL"], "folderId": folder_id}
    if region:
        body["regions"] = [region]
    request = Request(
        ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Api-Key {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            return json.load(response)
    except HTTPError as exc:
        # Never echo the response body: it may contain account details.
        raise RuntimeError(f"Wordstat returned HTTP {exc.code} for one seed") from None
    except URLError as exc:
        raise RuntimeError("Wordstat network request failed") from None


def normalize(raw: list[dict]) -> dict:
    rows = {}
    for block in raw:
        for kind in ("results", "associations"):
            for item in block["response"].get(kind, []):
                phrase = " ".join(str(item.get("phrase", "")).lower().split())
                if not phrase:
                    continue
                try:
                    count = max(0, int(item.get("count", 0)))
                except (TypeError, ValueError):
                    continue
                row = rows.setdefault(phrase, {
                    "query": phrase, "monthly_queries": 0, "query_type": classify(phrase),
                    "seed_sources": [], "review": "pending", "cluster": "", "target_section": "",
                })
                row["monthly_queries"] = max(row["monthly_queries"], count)
                source = {"seed": block["seed"], "kind": kind}
                if source not in row["seed_sources"]:
                    row["seed_sources"].append(source)
    return {"queries": sorted(rows.values(), key=lambda r: (-r["monthly_queries"], r["query"]))}


def write_page(page: dict, region: str, api_key: str, folder_id: str, fixture: Path | None) -> int:
    if fixture:
        sample = json.loads(fixture.read_text(encoding="utf-8"))
        raw = [{"seed": seed, "response": sample} for seed in page["seeds"]]
    else:
        raw = [{"seed": seed, "response": fetch_top(seed, region, api_key, folder_id)} for seed in page["seeds"]]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    output = ROOT / "data" / page["id"]
    output.mkdir(parents=True, exist_ok=True)
    meta = {"page_id": page["id"], "title": page["title"], "url": page["url"],
            "locale": page["locale"], "region": region or "all", "seeds": page["seeds"],
            "collected_at": now, "source": "Yandex Wordstat Search API GetTop",
            "editorial_status": "needs_review"}
    semantics = {**meta, **normalize(raw)}
    (output / "wordstat.json").write_text(json.dumps({**meta, "responses": raw}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "semantics.json").write_text(json.dumps(semantics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"# {page['title']} — семантика", "", f"URL: {page['url']}",
             f"Собрано: {now}; регион: {region or 'все'}; статус: требует ручной проверки.", "",
             "| Запрос | Частотность Wordstat | Тип интента | Кластер | Проверка |",
             "|---|---:|---|---|---|"]
    for row in semantics["queries"][:100]:
        query = row["query"].replace("|", "\\|")
        lines.append(f"| {query} | {row['monthly_queries']} | {row['query_type']} | — | проверить |")
    (output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(semantics["queries"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", required=True, help="Page ID from pages.json or all")
    parser.add_argument("--region", default="225", help="Wordstat region ID; empty for all regions")
    parser.add_argument("--fixture", type=Path, help="Local-only JSON response for testing")
    args = parser.parse_args()
    if args.region and not re.fullmatch(r"\d+", args.region):
        parser.error("Region must be a numeric Wordstat region ID")
    pages = get_pages()
    if args.page != "all" and args.page not in pages:
        parser.error(f"Unknown page ID: {args.page}")
    api_key = os.environ.get("YANDEX_CLOUD_API_KEY", "")
    folder_id = os.environ.get("YANDEX_CLOUD_FOLDER_ID", "")
    if not args.fixture and (not api_key or not folder_id):
        parser.error("Set YANDEX_CLOUD_API_KEY and YANDEX_CLOUD_FOLDER_ID as Actions secrets")
    selected = pages.values() if args.page == "all" else [pages[args.page]]
    for page in selected:
        count = write_page(page, args.region, api_key, folder_id, args.fixture)
        print(f"{page['id']}: {count} queries saved for editorial review")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)

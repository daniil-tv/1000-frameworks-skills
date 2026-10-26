#!/usr/bin/env python3
"""GitHub runner for the unchanged local Wordstat and SEO modules."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analyze_intent import analyze
from src.cluster_keywords import build as build_keywords
from src.wordstat import WordstatConfig, WordstatError, collect


def pages() -> dict[str, dict]:
    entries = json.loads((ROOT / "seo/pages.json").read_text(encoding="utf-8"))["pages"]
    result = {}
    for page in entries:
        page_id = page["id"]
        if not re.fullmatch(r"[a-z0-9-]+", page_id) or page_id in result:
            raise ValueError("Invalid or duplicate page ID in seo/pages.json")
        if not 1 <= len(page.get("seeds", [])) <= 8:
            raise ValueError(f"Page {page_id} needs 1–8 seeds")
        result[page_id] = page
    return result


def run(page: dict, region: str) -> dict:
    page_id = page["id"]
    output = ROOT / "seo/data" / page_id
    output.mkdir(parents=True, exist_ok=True)
    raw = collect(page_id, page["seeds"], output / "wordstat.json", refresh=True)
    keywords = build_keywords(raw, topic=page["title"])
    intent = analyze(page_id, page["title"], keywords)
    (output / "keywords.json").write_text(json.dumps(keywords, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "intent.json").write_text(json.dumps(intent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = {"page_id": page_id, "title": page["title"], "url": page["url"],
                "locale": page["locale"], "region": region or "all", "seeds": page["seeds"],
                "collected_at": raw["collected_at"], "source": raw["source"],
                "editorial_status": "needs_review"}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"# {page['title']} — семантика", "", f"URL: {page['url']}",
             f"Собрано: {raw['collected_at']}; регион: {region or 'все'}; статус: требует ручной проверки.", "",
             "| Запрос | Частотность Wordstat | Предварительный интент | Проверка |",
             "|---|---:|---|---|"]
    for row in keywords.get("all_keywords", [])[:100]:
        phrase = row["keyword"].replace("|", "\\|")
        lines.append(f"| {phrase} | {row['count']} | {row['intent']} | проверить |")
    (output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"page_id": page_id, "keywords": len(keywords.get("all_keywords", [])),
            "questions": len(keywords.get("questions", [])), "status": intent.get("status")}


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect semantics using local 1000 Frameworks modules")
    parser.add_argument("--page", required=True, help="Page ID from seo/pages.json")
    parser.add_argument("--region", default="225", help="Numeric Wordstat region; empty for all regions")
    args = parser.parse_args()
    if args.region and not re.fullmatch(r"\d+", args.region):
        parser.error("Region must be numeric")
    registry = pages()
    if args.page not in registry:
        parser.error("Unknown page ID")
    os.environ["YANDEX_WORDSTAT_REGIONS"] = args.region
    if WordstatConfig.from_env().missing():
        parser.error("GitHub Actions secrets YANDEX_CLOUD_API_KEY and YANDEX_CLOUD_FOLDER_ID are required")
    key = WordstatConfig.from_env().api_key
    if any(char.isspace() for char in key):
        # Copy/paste into Secrets can insert a line break in an otherwise valid key.
        # The connector reads this environment variable; never print its value.
        key = "".join(key.split())
        os.environ["YANDEX_CLOUD_API_KEY"] = key
    if any(ord(char) < 33 or ord(char) > 126 for char in key):
        parser.error("YANDEX_CLOUD_API_KEY contains unsupported characters; save only the key value")
    try:
        result = run(registry[args.page], args.region)
    except (WordstatError, ValueError) as exc:
        # The unchanged connector includes API response details in exceptions.
        # Report only the HTTP status, never the response body or credentials.
        match = re.search(r"HTTP (\d{3})", str(exc))
        code = match.group(1) if match else "unavailable"
        raise SystemExit(f"Wordstat request failed (HTTP {code}); check Actions secrets and Yandex permissions") from None
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

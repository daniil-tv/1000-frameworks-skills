#!/usr/bin/env python3
"""Official Yandex Wordstat API connector with deterministic local caching."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TOP_URL = "https://searchapi.api.cloud.yandex.net/v2/wordstat/topRequests"
DYNAMICS_URL = "https://searchapi.api.cloud.yandex.net/v2/wordstat/dynamics"
REGIONS_URL = "https://searchapi.api.cloud.yandex.net/v2/wordstat/regions"


class WordstatError(RuntimeError):
    pass


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class WordstatConfig:
    folder_id: str
    api_key: str = ""
    iam_token: str = ""
    regions: tuple[str, ...] = ()
    cache_dir: Path = ROOT / "data/cache/wordstat"

    @classmethod
    def from_env(cls) -> "WordstatConfig":
        return cls(
            folder_id=os.getenv("YANDEX_CLOUD_FOLDER_ID", "").strip(),
            api_key=os.getenv("YANDEX_CLOUD_API_KEY", "").strip(),
            iam_token=os.getenv("YANDEX_CLOUD_IAM_TOKEN", "").strip(),
            regions=tuple(x.strip() for x in os.getenv("YANDEX_WORDSTAT_REGIONS", "").split(",") if x.strip()),
        )

    def missing(self) -> list[str]:
        missing = []
        if not self.folder_id:
            missing.append("YANDEX_CLOUD_FOLDER_ID")
        if not (self.api_key or self.iam_token):
            missing.append("YANDEX_CLOUD_API_KEY or YANDEX_CLOUD_IAM_TOKEN")
        return missing


class WordstatClient:
    def __init__(self, config: WordstatConfig) -> None:
        self.config = config
        missing = config.missing()
        if missing:
            raise WordstatError("Missing credentials: " + ", ".join(missing))
        config.cache_dir.mkdir(parents=True, exist_ok=True)

    @property
    def auth_header(self) -> str:
        return f"Bearer {self.config.iam_token}" if self.config.iam_token else f"Api-Key {self.config.api_key}"

    def _request(self, url: str, body: dict[str, Any], *, refresh: bool = False) -> tuple[dict[str, Any], bool]:
        body = {**body, "folderId": self.config.folder_id}
        fingerprint = hashlib.sha256((url + json.dumps(body, ensure_ascii=False, sort_keys=True)).encode()).hexdigest()
        cache_path = self.config.cache_dir / f"{fingerprint}.json"
        if cache_path.exists() and not refresh:
            return json.loads(cache_path.read_text(encoding="utf-8")), True
        request = Request(
            url,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={"Authorization": self.auth_header, "Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise WordstatError(f"Wordstat HTTP {exc.code}: {details[:1000]}") from exc
        except URLError as exc:
            raise WordstatError(f"Wordstat connection failed: {exc.reason}") from exc
        cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return payload, False

    def top(self, phrase: str, *, limit: int = 300, refresh: bool = False) -> tuple[dict[str, Any], bool]:
        body: dict[str, Any] = {
            "phrase": phrase,
            "numPhrases": max(1, min(limit, 2000)),
            "devices": ["DEVICE_ALL"],
        }
        if self.config.regions:
            body["regions"] = list(self.config.regions)
        return self._request(TOP_URL, body, refresh=refresh)

    def dynamics(self, phrase: str, *, months: int = 12, refresh: bool = False) -> tuple[dict[str, Any], bool]:
        today = date.today()
        end = date(today.year, today.month, 1) - timedelta(days=1)
        month_index = end.year * 12 + (end.month - 1) - (max(1, months) - 1)
        start = date(month_index // 12, month_index % 12 + 1, 1)
        body: dict[str, Any] = {
            "phrase": phrase,
            "period": "PERIOD_MONTHLY",
            "fromDate": f"{start.isoformat()}T00:00:00Z",
            "toDate": f"{end.isoformat()}T23:59:59Z",
            "devices": ["DEVICE_ALL"],
        }
        if self.config.regions:
            body["regions"] = list(self.config.regions)
        return self._request(DYNAMICS_URL, body, refresh=refresh)

    def regions(self, phrase: str, *, refresh: bool = False) -> tuple[dict[str, Any], bool]:
        return self._request(
            REGIONS_URL,
            {"phrase": phrase, "region": "REGION_REGIONS", "devices": ["DEVICE_ALL"]},
            refresh=refresh,
        )


def collect(page_id: str, seeds: list[str], output: Path, *, refresh: bool = False, limit: int = 300) -> dict[str, Any]:
    client = WordstatClient(WordstatConfig.from_env())
    seed_results = []
    for seed in seeds:
        payload, cache_hit = client.top(seed, limit=limit, refresh=refresh)
        seed_results.append({"seed": seed, "cache_hit": cache_hit, "payload": payload})
    dynamics, dynamics_cache = client.dynamics(seeds[0], refresh=refresh)
    payload = {
        "page_id": page_id,
        "status": "complete",
        "source": "Yandex Wordstat API",
        "collected_at": date.today().isoformat(),
        "regions": list(client.config.regions),
        "seeds": seed_results,
        "dynamics": {"seed": seeds[0], "cache_hit": dynamics_cache, "payload": dynamics},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Yandex Wordstat API connector")
    parser.add_argument("--env", default=".env")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    run = sub.add_parser("collect")
    run.add_argument("page_id")
    run.add_argument("--seed", action="append", required=True)
    run.add_argument("--output")
    run.add_argument("--limit", type=int, default=300)
    run.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    load_env(ROOT / args.env)
    config = WordstatConfig.from_env()
    if args.command == "doctor":
        missing = config.missing()
        print(json.dumps({"ready": not missing, "missing": missing, "regions": list(config.regions), "cache": str(config.cache_dir)}, ensure_ascii=False, indent=2))
        raise SystemExit(0 if not missing else 2)
    output = Path(args.output) if args.output else ROOT / f"data/wordstat/{args.page_id}.json"
    result = collect(args.page_id, args.seed, output, refresh=args.refresh, limit=args.limit)
    print(json.dumps({"page_id": args.page_id, "status": result["status"], "output": str(output)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except WordstatError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)

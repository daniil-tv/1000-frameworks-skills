#!/usr/bin/env python3
"""Normalize Wordstat output and create intent-aware semantic clusters."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORD_RE = re.compile(r"[a-zа-яё0-9]+", re.I)
QUESTION_WORDS = {"как", "что", "зачем", "почему", "когда", "какой", "какие", "где", "сколько"}
COMMERCIAL = {"цена", "стоимость", "заказать", "услуги", "агентство", "курс", "обучение"}
PRACTICAL = {"методы", "этапы", "план", "шаблон", "пример", "интервью", "опрос", "гайд", "чеклист"}
NOISE = {"вакансии", "работа", "зарплата", "скачать бесплатно", "реферат", "курсовая"}


def normalize(value: str) -> str:
    return " ".join(value.lower().replace("ё", "е").split())


def tokens(value: str) -> set[str]:
    return set(WORD_RE.findall(normalize(value)))


def stem(word: str) -> str:
    """Small deterministic stemmer for topic matching, not linguistic output."""
    for suffix in (
        "иями", "ями", "ами", "иями", "ение", "ания", "ения", "ование",
        "иями", "ого", "ему", "ому", "ыми", "ими", "ий", "ый", "ая",
        "яя", "ое", "ее", "ов", "ев", "ам", "ям", "ах", "ях", "ия",
        "ие", "ы", "и", "а", "я", "у", "ю", "е", "о",
    ):
        if len(word) - len(suffix) >= 5 and word.endswith(suffix):
            return word[:-len(suffix)]
    return word


def match_tokens(value: str) -> set[str]:
    return {stem(word) for word in tokens(value)}


def intent(value: str) -> str:
    words = tokens(value)
    if words & COMMERCIAL:
        return "commercial"
    if words & PRACTICAL:
        return "practical"
    if words & QUESTION_WORDS:
        return "informational_question"
    return "informational"


def is_noise(phrase: str, topic_tokens: set[str]) -> bool:
    normalized = normalize(phrase)
    if any(marker in normalized for marker in NOISE):
        return True
    return bool(topic_tokens) and not bool(match_tokens(normalized) & topic_tokens)


def build(raw: dict[str, Any], *, topic: str) -> dict[str, Any]:
    topic_tokens = match_tokens(topic)
    phrases: dict[str, dict[str, Any]] = {}
    excluded = []
    for seed_block in raw.get("seeds", []):
        seed = seed_block.get("seed", "")
        payload = seed_block.get("payload", {})
        for kind in ("results", "associations"):
            for row in payload.get(kind, []):
                phrase = normalize(str(row.get("phrase", "")))
                if not phrase:
                    continue
                if is_noise(phrase, topic_tokens):
                    excluded.append({"phrase": phrase, "reason": "noise_or_topic_mismatch", "seed": seed})
                    continue
                count = int(row.get("count") or 0)
                current = phrases.setdefault(phrase, {"keyword": phrase, "count": 0, "sources": [], "intent": intent(phrase)})
                current["count"] = max(current["count"], count)
                current["sources"].append({"seed": seed, "kind": kind})

    ordered = sorted(phrases.values(), key=lambda item: (-item["count"], item["keyword"]))
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in ordered:
        groups[row["intent"]].append(row)
    primary = [row for row in ordered if row["intent"] in {"informational", "informational_question", "practical"}][:30]
    commercial = groups.get("commercial", [])
    questions = [row for row in ordered if row["intent"] == "informational_question"]
    candidates = [
        {"keyword": row["keyword"], "count": row["count"], "status": "planned_candidate"}
        for row in commercial[:10]
        if row["count"] > 0
    ]
    return {
        "page_id": raw.get("page_id"),
        "status": "complete" if ordered else "needs_review",
        "topic": topic,
        "primary_cluster": primary,
        "secondary_clusters": {name: rows[:30] for name, rows in groups.items() if name not in {"informational"}},
        "questions": questions[:30],
        "candidate_child_pages": candidates,
        "possible_cannibalization": [],
        "excluded": excluded[:100],
        "all_keywords": ordered,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("page_id")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()
    input_path = Path(args.input) if args.input else ROOT / f"data/wordstat/{args.page_id}.json"
    output_path = Path(args.output) if args.output else ROOT / f"data/keywords/{args.page_id}.json"
    result = build(json.loads(input_path.read_text(encoding="utf-8")), topic=args.topic)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"page_id": args.page_id, "status": result["status"], "keywords": len(result["all_keywords"]), "output": str(output_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a deterministic search-intent/JTBD record from collected semantics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def analyze(page_id: str, topic: str, keywords: dict) -> dict:
    status = keywords.get("status")
    primary = keywords.get("primary_cluster", [])
    questions = [row.get("keyword", "") for row in keywords.get("questions", [])]
    if status != "complete" or not primary:
        return {
            "page_id": page_id,
            "status": "needs_review",
            "reason": "Wordstat semantics are not complete.",
        }
    return {
        "page_id": page_id,
        "status": "complete",
        "search_intent": "informational_practical",
        "user_job": f"Разобраться в теме «{topic}» и получить последовательность действий, которую можно применить в работе.",
        "context": "Пользователь планирует исследование или хочет улучшить существующий процесс принятия решений.",
        "trigger": "Команде не хватает проверенных данных о клиентах, их поведении, мотивации и выборе.",
        "expected_outcome": "Понятный выбор метода, порядок исследования, конкретные результаты и критерии качества.",
        "current_alternatives": ["внутренние мнения", "продуктовая аналитика без качественного контекста", "разовые опросы", "интервью без единого плана"],
        "criteria_of_success": ["понятно, какой вопрос исследуется", "метод соответствует вопросу", "выборка и данные достаточны", "выводы переводятся в решения"],
        "serp_questions": questions[:12],
        "primary_keywords": [row.get("keyword") for row in primary[:15]],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("page_id")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()
    input_path = Path(args.input) if args.input else ROOT / f"data/keywords/{args.page_id}.json"
    output_path = Path(args.output) if args.output else ROOT / f"data/intent/{args.page_id}.json"
    result = analyze(args.page_id, args.topic, json.loads(input_path.read_text(encoding="utf-8")))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

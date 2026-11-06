#!/usr/bin/env python3
"""Build a cautious page-specific search-intent hypothesis from Wordstat clusters."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Profiles describe the METHOD, not user behaviour inferred from query volume.
# If a page has no profile, do not assign it an interview/research job by default.
PROFILES = {
    "ansoff-matrix": {
        "user_job": "Сравнить варианты роста бизнеса по существующим и новым продуктам и рынкам.",
        "context": "Компания выбирает направление расширения и сопоставляет инвестиции, риски и ожидаемый спрос.",
        "trigger": "Нужно определить, развивать продажи существующего продукта, выходить на новый рынок, создавать продукт или диверсифицировать бизнес.",
        "expected_outcome": "Матрица из четырёх вариантов роста с допущениями, ресурсами, рисками и планом проверки.",
        "current_alternatives": ["выбор направления роста на основе мнений", "разрозненные прогнозы по продуктам и сегментам"],
        "criteria_of_success": ["границы продуктов и рынков определены", "четыре направления сравниваются на одинаковом горизонте", "допущения и экономика проверяемы"],
    },
    "bcg-matrix": {
        "user_job": "Сравнить направления портфеля по росту рынков и относительной рыночной доле.",
        "context": "Несколько направлений бизнеса конкурируют за общий инвестиционный бюджет.",
        "trigger": "Нужно определить приоритеты вложений и оценить роль каждого направления в портфеле.",
        "expected_outcome": "Матрица портфеля с расчётами, допущениями и вариантами распределения капитала.",
        "current_alternatives": ["распределение бюджета по прошлогодним долям", "инвестиции без сравнения позиций направлений"],
        "criteria_of_success": ["границы рынков сопоставимы", "рост рынка и относительная доля рассчитаны", "решения проверены по денежным потокам"],
    },
    "tows-matrix": {
        "user_job": "Разработать варианты стратегических действий из сочетаний внутренних и внешних факторов.",
        "context": "Есть подтверждённые факторы SWOT, но ещё нет приоритизированного плана действий.",
        "trigger": "Нужно связать сильные и слабые стороны с возможностями и угрозами.",
        "expected_outcome": "Варианты SO, ST, WO, WT с причинной логикой, рисками и проверками.",
        "current_alternatives": ["SWOT как перечень без действий", "решения без привязки к факторам"],
        "criteria_of_success": ["факторы имеют источники", "каждый вариант связан с конкретной парой факторов", "решения реализуемы и проверяемы"],
    },
    "test-card": {
        "user_job": "Спланировать проверку одной критичной бизнес-гипотезы до начала эксперимента.",
        "context": "Команда собирается принимать решение на основе результата теста.",
        "trigger": "Не определены проверяющий эксперимент, метрика и порог успеха.",
        "expected_outcome": "Test Card с гипотезой, экспериментом, измерением и заранее заданным критерием.",
        "current_alternatives": ["эксперимент без явной гипотезы", "оценка успеха после получения результатов"],
        "criteria_of_success": ["гипотеза опровержима", "метрика соответствует поведению", "порог задан до запуска"],
    },
    "learning-card": {
        "user_job": "Зафиксировать наблюдения и выводы после эксперимента и принять следующее решение.",
        "context": "Проверка гипотезы завершена; есть исходная Test Card и собранные данные.",
        "trigger": "Необходимо отделить факты наблюдения от объяснений команды.",
        "expected_outcome": "Learning Card с исходной гипотезой, наблюдениями, выводами и следующими действиями.",
        "current_alternatives": ["неструктурированные итоги теста", "выводы без ссылок на наблюдения"],
        "criteria_of_success": ["исходный критерий сохранён", "наблюдения отделены от интерпретаций", "следующее действие зафиксировано"],
    },
}

def analyze(page_id: str, topic: str, keywords: dict) -> dict:
    primary = keywords.get("primary_cluster", [])
    if keywords.get("status") != "complete" or not primary:
        return {"page_id": page_id, "status": "needs_review", "reason": "Wordstat semantics are not complete."}
    questions = [row.get("keyword", "") for row in keywords.get("questions", [])]
    profile = PROFILES.get(page_id)
    base = {
        "page_id": page_id,
        "status": "complete",
        "editorial_status": "needs_review",
        "search_intent": "informational_practical",
        "intent_source": "page_specific_rules" if profile else "generic_hypothesis",
        "serp_verified": False,
        "serp_questions": questions[:12],
        "primary_keywords": [row.get("keyword") for row in primary[:15]],
    }
    if profile:
        base.update(profile)
    else:
        base.update({
            "user_job": f"Понять назначение и способ применения метода «{topic}».",
            "context": "Нужно выбрать подходящий метод для конкретного управленческого решения.",
            "trigger": "Нужно разобраться в методе и проверить его применимость к своей задаче.",
            "expected_outcome": "Понимание назначения метода, входных данных, этапов и ограничений.",
            "current_alternatives": [],
            "criteria_of_success": ["метод соответствует задаче", "исходные данные и допущения обозначены", "результат и ограничения понятны"],
        })
    return base


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

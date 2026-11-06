"""Regression checks for method-specific intent selection."""

import unittest

from src.analyze_intent import analyze


class AnalyzeIntentTests(unittest.TestCase):
    def setUp(self):
        self.keywords = {
            "status": "complete",
            "primary_cluster": [{"keyword": "матрица ансоффа", "count": 1473}],
            "questions": [],
        }

    def test_ansoff_is_growth_strategy_not_interviews(self):
        result = analyze("ansoff-matrix", "Матрица Ансоффа", self.keywords)
        self.assertEqual(result["intent_source"], "page_specific_rules")
        self.assertIn("роста бизнеса", result["user_job"])
        self.assertNotIn("интервью", str(result).lower())
        self.assertNotIn("выборк", str(result).lower())
        self.assertEqual(result["editorial_status"], "needs_review")

    def test_unknown_method_does_not_inherit_customer_research(self):
        result = analyze("unknown-method", "Неизвестная методика", self.keywords)
        self.assertEqual(result["intent_source"], "generic_hypothesis")
        self.assertNotIn("интервью", str(result).lower())
        self.assertNotIn("клиент", str(result).lower())

    def test_missing_semantics_requires_review(self):
        result = analyze("ansoff-matrix", "Матрица Ансоффа", {"status": "needs_review"})
        self.assertEqual(result["status"], "needs_review")


if __name__ == "__main__":
    unittest.main()

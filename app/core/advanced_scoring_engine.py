import os
import json
from typing import Any, Callable, Dict
from app.utils.logger import get_logger

RISK_CONFIG_DEFAULT = {
    "age": {
        "18-25": 20,
        "25-40": 10,
        "40-60": 5,
        "60-100": 15,
    },
    "income": {
        "<20000": 25,
        "20000-50000": 15,
        "50000-100000": 5,
        ">100000": 2,
    },
    "activity_score": {
        "<30": 30,
        "30-60": 15,
        "60-80": 5,
        ">80": 2,
    },
    "weights": {
        "age": 1.2,
        "income": 1.5,
        "activity_score": 1.0,
    },
}


class AdvancedRiskEngine:
    def __init__(self, config_path: str | None = None):
        self.logger = get_logger("app.core.advanced_engine")
        self.config_path = config_path or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "config", "risk_config.json")
        )
        self.config = self._load_config(self.config_path)
        self.custom_rules: Dict[str, Callable[[Dict[str, Any]], float]] = {}

    def _load_config(self, path: str) -> Dict[str, Any]:
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    return cfg
        except Exception as e:
            self.logger.error(f"Failed to load config at {path}: {e}")
        return RISK_CONFIG_DEFAULT

    def update_config(self, new_config: Dict[str, Any]):
        self.config = new_config

    def _get_weight(self, key: str) -> float:
        return float(self.config.get("weights", {}).get(key, 1.0))

    def _score_from_buckets(self, value: float, buckets: Dict[str, int], feature_name: str) -> tuple[int, str]:
        for label, points in buckets.items():
            if "-" in label and label[0].isdigit():
                parts = label.split("-")
                low = float(parts[0])
                high = float(parts[1])
                if low <= float(value) <= high:
                    self.logger.debug(f"{feature_name}={value} matched {label} → {points}")
                    return int(points), label
            elif label.startswith("<"):
                threshold = float(label[1:])
                if float(value) < threshold:
                    self.logger.debug(f"{feature_name}={value} matched {label} → {points}")
                    return int(points), label
            elif label.startswith(">"):
                threshold = float(label[1:])
                if float(value) > threshold:
                    self.logger.debug(f"{feature_name}={value} matched {label} → {points}")
                    return int(points), label
        last_label = list(buckets.keys())[-1]
        last_points = buckets[last_label]
        self.logger.debug(f"{feature_name}={value} defaulted to {last_label} → {last_points}")
        return int(last_points), last_label

    def score_age(self, age: int) -> tuple[int, str]:
        points, label = self._score_from_buckets(age, self.config["age"], "age")
        return points, label

    def score_income(self, income: float) -> tuple[int, str]:
        points, label = self._score_from_buckets(income, self.config["income"], "income")
        return points, label

    def score_activity(self, activity_score: int) -> tuple[int, str]:
        points, label = self._score_from_buckets(activity_score, self.config["activity_score"], "activity_score")
        return points, label

    def calculate(self, age: int, income: float, activity_score: int) -> float:
        age_points, _ = self.score_age(age)
        income_points, _ = self.score_income(income)
        activity_points, _ = self.score_activity(activity_score)
        final = (
            age_points * self._get_weight("age")
            + income_points * self._get_weight("income")
            + activity_points * self._get_weight("activity_score")
        )
        return float(final)

    def explain(self, age: int, income: float, activity_score: int) -> Dict[str, Any]:
        age_points, age_label = self.score_age(age)
        income_points, income_label = self.score_income(income)
        activity_points, activity_label = self.score_activity(activity_score)
        w_age = self._get_weight("age")
        w_income = self._get_weight("income")
        w_activity = self._get_weight("activity_score")
        age_contrib = age_points * w_age
        income_contrib = income_points * w_income
        activity_contrib = activity_points * w_activity
        final = age_contrib + income_contrib + activity_contrib
        explanation = (
            f"Age bucket {age_label} contributed {age_contrib:.2f} after weighting. "
            f"Income bucket {income_label} contributed {income_contrib:.2f}. "
            f"Activity bucket {activity_label} contributed {activity_contrib:.2f}. "
            f"Final score = {final:.2f}."
        )
        return {
            "scores": {
                "age_score": age_points,
                "income_score": income_points,
                "activity_score": activity_points,
            },
            "weights": {
                "age": w_age,
                "income": w_income,
                "activity_score": w_activity,
            },
            "final_score": float(final),
            "explanation": explanation,
        }

    def calculate_with_explanation(self, inputs: Any) -> Dict[str, Any]:
        age = getattr(inputs, "age", None) if not isinstance(inputs, dict) else inputs.get("age")
        income = getattr(inputs, "income", None) if not isinstance(inputs, dict) else inputs.get("income")
        activity_score = getattr(inputs, "activity_score", None) if not isinstance(inputs, dict) else inputs.get("activity_score")
        result = self.explain(age, income, activity_score)
        custom = self.apply_custom_rules({"age": age, "income": income, "activity_score": activity_score})
        if custom:
            self.logger.debug(f"Custom rules evaluated: {custom}")
        return result

    def add_custom_rule(self, rule_name: str, func: Callable[[Dict[str, Any]], float]):
        """Allow plugging in custom scoring functions."""
        self.custom_rules[rule_name] = func

    def apply_custom_rules(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate custom rules if provided."""
        results: Dict[str, float] = {}
        for name, func in self.custom_rules.items():
            try:
                results[name] = float(func(data))
            except Exception as e:
                self.logger.error(f"Custom rule {name} failed: {e}")
        return results


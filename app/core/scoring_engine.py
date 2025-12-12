class RiskScoringEngine:
    def calculate_score(self, age: int, income: float, activity_score: int) -> int:
        age_points = 20 if age < 25 else 10 if age < 40 else 5 if age < 60 else 15
        income_points = 25 if income < 20000 else 15 if income < 50000 else 5 if income < 100000 else 2
        activity_points = 30 if activity_score < 30 else 15 if activity_score < 60 else 5 if activity_score < 80 else 2
        return age_points + income_points + activity_points

    def explain(self, age: int, income: float, activity_score: int) -> str:
        age_points = 20 if age < 25 else 10 if age < 40 else 5 if age < 60 else 15
        income_points = 25 if income < 20000 else 15 if income < 50000 else 5 if income < 100000 else 2
        activity_points = 30 if activity_score < 30 else 15 if activity_score < 60 else 5 if activity_score < 80 else 2

        age_desc = "high risk" if age < 25 else "moderate risk" if age < 40 else "low risk" if age < 60 else "elevated risk"
        income_desc = "very low income" if income < 20000 else "low income" if income < 50000 else "stable income" if income < 100000 else "high income"
        activity_desc = "very low activity" if activity_score < 30 else "moderate activity" if activity_score < 60 else "high activity" if activity_score < 80 else "very high activity"

        final_score = age_points + income_points + activity_points
        return (
            f"Age contributed {age_points} points ({age_desc}). "
            f"Income added {income_points} points ({income_desc}). "
            f"Activity score added {activity_points} points ({activity_desc}). "
            f"Final score = {final_score}."
        )

    def calculate_with_explanation(self, inputs):
        age = getattr(inputs, "age", None) if not isinstance(inputs, dict) else inputs.get("age")
        income = getattr(inputs, "income", None) if not isinstance(inputs, dict) else inputs.get("income")
        activity_score = getattr(inputs, "activity_score", None) if not isinstance(inputs, dict) else inputs.get("activity_score")

        final_score = self.calculate_score(age, income, activity_score)
        explanation = self.explain(age, income, activity_score)
        return {"final_score": final_score, "explanation": explanation}


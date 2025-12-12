from app.core.scoring_engine import RiskScoringEngine

engine = RiskScoringEngine()

def test_low_income_high_risk():
    result = engine.calculate_score(age=22, income=10000, activity_score=20)
    assert result > 50

def test_age_scoring_bands():
    assert engine.calculate_score(age=22, income=100000, activity_score=80) == 20 + 2 + 2
    assert engine.calculate_score(age=30, income=100000, activity_score=80) == 10 + 2 + 2
    assert engine.calculate_score(age=50, income=100000, activity_score=80) == 5 + 2 + 2
    assert engine.calculate_score(age=65, income=100000, activity_score=80) == 15 + 2 + 2

def test_income_scoring_bands():
    assert engine.calculate_score(age=40, income=10000, activity_score=80) == 5 + 25 + 2
    assert engine.calculate_score(age=40, income=30000, activity_score=80) == 5 + 15 + 2
    assert engine.calculate_score(age=40, income=70000, activity_score=80) == 5 + 5 + 2
    assert engine.calculate_score(age=40, income=150000, activity_score=80) == 5 + 2 + 2

def test_activity_scoring_bands():
    assert engine.calculate_score(age=40, income=100000, activity_score=20) == 5 + 2 + 30
    assert engine.calculate_score(age=40, income=100000, activity_score=50) == 5 + 2 + 15
    assert engine.calculate_score(age=40, income=100000, activity_score=70) == 5 + 2 + 5
    assert engine.calculate_score(age=40, income=100000, activity_score=85) == 5 + 2 + 2

def test_final_weighted_sum():
    score = engine.calculate_score(age=35, income=45000, activity_score=55)
    assert score == 10 + 15 + 15

def test_explanation_contains_final_score_text():
    age, income, activity = 35, 45000.0, 55
    score = engine.calculate_score(age=age, income=income, activity_score=activity)
    text = engine.explain(age=age, income=income, activity_score=activity)
    assert f"Final score = {score}." in text
    assert "Age contributed" in text


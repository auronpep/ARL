from pathlib import Path

from arl.compare import compare_scores
from arl.select_questions import select_questions
from arl.scoring import score_run


ROOT = Path(__file__).resolve().parents[1]


def test_score_run_rewards_correct_traced_answers():
    summary = score_run(
        ROOT / "tests" / "fixtures" / "conlaw_questions.jsonl",
        ROOT / "tests" / "fixtures" / "conlaw_answers_good.jsonl",
        ROOT / "study" / "mechanics_pack.yaml",
    )
    metrics = summary["metrics"]
    assert metrics["accuracy"] == 1.0
    assert metrics["dominant_trap_rejection_rate"] == 1.0
    assert metrics["mechanic_trace_coverage"] == 1.0
    assert metrics["hidden_doctrine_count"] == 0


def test_compare_scores_uses_lexicographic_promotion_order():
    before = {"metrics": {"accuracy": 1.0, "dominant_trap_rejection_rate": 0.5}}
    after_worse_accuracy = {"metrics": {"accuracy": 0.99, "dominant_trap_rejection_rate": 1.0}}
    assert compare_scores(before, after_worse_accuracy, gate="promotion")["keep"] is False

    after_better_trap = {"metrics": {"accuracy": 1.0, "dominant_trap_rejection_rate": 0.75}}
    assert compare_scores(before, after_better_trap, gate="promotion")["keep"] is True


def test_select_next_questions_prioritizes_high_confidence_miss():
    selected = select_questions(
        ROOT / "tests" / "fixtures" / "conlaw_questions.jsonl",
        ROOT / "tests" / "fixtures" / "attempt_history.jsonl",
        limit=1,
    )
    assert selected[0]["id"] == "Q-CONLAW-001"
    assert selected[0]["selection_score"] >= 100

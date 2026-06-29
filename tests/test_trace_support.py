from pathlib import Path

from arl.trace import audit_trace_support


ROOT = Path(__file__).resolve().parents[1]


def test_trace_audit_marks_good_answers_child_usable():
    report = audit_trace_support(
        ROOT / "tests" / "fixtures" / "conlaw_questions.jsonl",
        ROOT / "tests" / "fixtures" / "conlaw_answers_good.jsonl",
        ROOT / "study" / "mechanics_pack.yaml",
    )
    assert report["summary"]["child_usable_trace_rate"] == 1.0
    assert report["summary"]["hidden_doctrine_count"] == 0


def test_trace_audit_flags_right_answer_without_pack_support():
    report = audit_trace_support(
        ROOT / "tests" / "fixtures" / "conlaw_questions.jsonl",
        ROOT / "tests" / "fixtures" / "conlaw_answers_bad_trace.jsonl",
        ROOT / "study" / "mechanics_pack.yaml",
    )
    first = report["items"][0]
    assert first["answer"] == "C"
    assert first["trace_complete"] is False
    assert first["child_usable"] is False
    assert first["hidden_doctrine_detected"] is True

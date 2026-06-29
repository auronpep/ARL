from pathlib import Path

from arl.loop import run_loop


ROOT = Path(__file__).resolve().parents[1]


def test_run_loop_completes_requested_iterations(tmp_path):
    summary = run_loop(
        ROOT / "tests" / "fixtures" / "conlaw_questions.jsonl",
        ROOT / "study" / "mechanics_pack.yaml",
        tmp_path,
        iterations=2,
    )

    assert summary["iterations_completed"] == 2
    assert (tmp_path / "answers.jsonl").exists()
    assert (tmp_path / "selected_questions.jsonl").exists()


def test_run_loop_can_use_model_answer_provider(tmp_path):
    def provider(prompt: str) -> str:
        assert "mechanics_pack" in prompt
        return '{"answer":"C","mechanic_ids_used":["CONLAW-SPENDING-POWER-01"],"eliminations":{}}'

    summary = run_loop(
        ROOT / "tests" / "fixtures" / "conlaw_questions.jsonl",
        ROOT / "study" / "mechanics_pack.yaml",
        tmp_path,
        iterations=1,
        answer_provider=provider,
    )

    assert summary["iterations_completed"] == 1
    assert summary["score"]["accuracy"] == 1.0

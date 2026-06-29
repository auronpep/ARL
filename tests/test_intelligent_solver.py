from pathlib import Path

from arl.intelligent_solver import build_solver_prompt, parse_answer_response, solve_question_with_provider
from arl.io import load_jsonl
from arl.pack import load_pack


ROOT = Path(__file__).resolve().parents[1]


def test_solver_prompt_excludes_answer_key_and_private_explanations():
    question = load_jsonl(ROOT / "tests" / "fixtures" / "conlaw_questions.jsonl")[0]
    question["private_notes"] = {
        "answer_explanation": "SECRET_CORRECT_EXPLANATION",
        "wrong_answer_explanation": "SECRET_WRONG_EXPLANATION",
    }
    pack = load_pack(ROOT / "study" / "mechanics_pack.yaml")

    prompt = build_solver_prompt(question, pack)

    assert "SECRET_CORRECT_EXPLANATION" not in prompt
    assert "SECRET_WRONG_EXPLANATION" not in prompt
    assert "dominant_trap_choice" not in prompt
    assert "expected_mechanic_ids" not in prompt


def test_parse_answer_response_accepts_markdown_wrapped_json():
    text = """Here is the answer:

```json
{"question_id":"Q-CONLAW-001","answer":"C","confidence":0.8,"phase_used":"CUT","mechanic_ids_used":["CONLAW-SPENDING-POWER-01"],"eliminations":{"A":{"filter":"NOT_TRUE","reason":"Federal police power is bait."}},"dominant_trap_rejected":true,"dominant_trap_rejection_reason":"Federal police power is bait.","deciding_fact":"Federal funds.","student_script":"Federal money statute: spend power, not police power.","answer_steps":[{"mechanic_id":"CONLAW-SPENDING-POWER-01","text":"Federal money routes to spending power."}]}
```
"""

    parsed = parse_answer_response(text)

    assert parsed["answer"] == "C"
    assert parsed["mechanic_ids_used"] == ["CONLAW-SPENDING-POWER-01"]


def test_solve_question_with_provider_normalizes_required_fields():
    question = load_jsonl(ROOT / "tests" / "fixtures" / "conlaw_questions.jsonl")[0]
    pack = load_pack(ROOT / "study" / "mechanics_pack.yaml")

    def provider(prompt: str) -> str:
        assert "Correct Answer" not in prompt
        return '{"answer":"C","mechanic_ids_used":["CONLAW-SPENDING-POWER-01"],"eliminations":{}}'

    answer = solve_question_with_provider(question, pack, provider)

    assert answer["question_id"] == question["id"]
    assert answer["answer"] == "C"
    assert answer["phase_used"] == "CALL"
    assert answer["confidence"] == 0.5

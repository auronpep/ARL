from __future__ import annotations

from pathlib import Path
from typing import Any

from arl.io import load_jsonl, write_json, write_jsonl
from arl.pack import load_pack
from arl.scoring import score_run
from arl.select_questions import select_questions
from arl.solver import solve_question
from arl.trace import audit_trace_support


def run_loop(
    questions_path: str | Path,
    pack_path: str | Path,
    out_dir: str | Path,
    iterations: int = 50,
) -> dict[str, Any]:
    questions_path = Path(questions_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    questions = {q["id"]: q for q in load_jsonl(questions_path)}
    pack = load_pack(pack_path)
    history: list[dict[str, Any]] = []
    answers: list[dict[str, Any]] = []
    selected_questions: list[dict[str, Any]] = []
    seen: set[str] = set()

    history_path = out_dir / "attempt_history.jsonl"
    write_jsonl(history_path, history)

    for iteration in range(1, iterations + 1):
        candidates = [q for q in select_questions(questions_path, history_path, limit=len(questions)) if q["id"] not in seen]
        if not candidates:
            break
        selected = candidates[0]
        question = questions[selected["id"]]
        answer = solve_question(question, pack)

        is_correct = answer["answer"] == question.get("answer")
        selected_questions.append({**selected, "iteration": iteration})
        answers.append(answer)
        history.append(
            {
                "iteration": iteration,
                "question_id": question["id"],
                "correct": is_correct,
                "confidence": answer["confidence"],
                "dominant_trap_rejected": answer["dominant_trap_rejected"],
                "hidden_doctrine_count": 0 if answer["mechanic_ids_used"] else 1,
                "trace_complete": bool(answer["mechanic_ids_used"]),
                "surface_cluster": question.get("surface_cluster", ""),
            }
        )
        seen.add(question["id"])
        write_jsonl(history_path, history)

    selected_path = out_dir / "selected_questions.jsonl"
    answers_path = out_dir / "answers.jsonl"
    write_jsonl(selected_path, selected_questions)
    write_jsonl(answers_path, answers)

    selected_question_rows = [questions[item["id"]] for item in selected_questions]
    selected_questions_path = out_dir / "selected_question_bank.jsonl"
    write_jsonl(selected_questions_path, selected_question_rows)

    score = score_run(selected_questions_path, answers_path, pack_path)
    trace = audit_trace_support(selected_questions_path, answers_path, pack_path)
    summary = {
        "iterations_requested": iterations,
        "iterations_completed": len(answers),
        "question_source": str(questions_path),
        "pack": str(pack_path),
        "out_dir": str(out_dir),
        "selected_questions": len(selected_question_rows),
        "score": score["metrics"],
        "trace": trace["summary"],
    }
    write_json(out_dir / "score.json", score)
    write_json(out_dir / "trace.json", trace)
    write_json(out_dir / "loop_summary.json", summary)
    return summary


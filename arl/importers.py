from __future__ import annotations

from pathlib import Path
from typing import Any

from arl.io import load_jsonl, write_jsonl


def import_barmatrix_conlaw(source_path: str | Path, out_dir: str | Path) -> dict[str, int]:
    rows = load_jsonl(source_path)
    questions: list[dict[str, Any]] = []
    choice_forensics: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []

    for row in rows:
        question_id = row.get("question_id") or row.get("id")
        if not question_id:
            raise ValueError("row missing question_id/id")
        choices = row.get("choices") or {}
        questions.append(
            {
                "id": question_id,
                "subject": row.get("subject", "CONSTITUTIONAL_LAW"),
                "topic": row.get("topic", ""),
                "subtopic": row.get("subtopic", ""),
                "outline_code": row.get("outline_code", ""),
                "call": row.get("call", ""),
                "stem": row.get("stem", ""),
                "choices": choices,
                "answer": row.get("answer", ""),
                "dominant_trap_choice": row.get("dominant_trap_choice", ""),
                "dominant_trap_mechanic": row.get("dominant_trap_mold", row.get("dominant_trap_mechanic", "")),
                "dominant_trap_pick_rate": row.get("dominant_trap_pick_rate", 0),
                "expected_phase": row.get("expected_phase", ""),
                "expected_axis": row.get("expected_axis", ""),
                "expected_dispositive_fact": row.get("expected_dispositive_fact", ""),
                "expected_mechanic_ids": row.get("expected_mechanic_ids", []),
                "question_shape": row.get("question_shape", ""),
            }
        )
        for choice, forensic in (row.get("choice_forensics") or {}).items():
            item = dict(forensic)
            item["question_id"] = question_id
            item["choice"] = choice
            choice_forensics.append(item)
        if row.get("attempt"):
            attempt = dict(row["attempt"])
            attempt["question_id"] = question_id
            attempts.append(attempt)

    out = Path(out_dir)
    write_jsonl(out / "questions_dev.jsonl", questions)
    write_jsonl(out / "choice_forensics.jsonl", choice_forensics)
    write_jsonl(out / "attempt_history.jsonl", attempts)
    return {"questions": len(questions), "choice_forensics": len(choice_forensics), "attempts": len(attempts)}


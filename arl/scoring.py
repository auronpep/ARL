from __future__ import annotations

from pathlib import Path
from statistics import mean
from typing import Any

from arl.io import load_jsonl
from arl.pack import load_pack


def _by_id(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {row[key]: row for row in rows}


def _round(value: float) -> float:
    return round(value, 6)


def _pack_stats(pack_path: str | Path | None) -> tuple[set[str], int, int]:
    if not pack_path:
        return set(), 0, 0
    path = Path(pack_path)
    pack = load_pack(path)
    token_count = len(path.read_text(encoding="utf-8").split())
    return {card.id for card in pack.cards}, len(pack.cards), token_count


def score_run(questions_path: str | Path, answers_path: str | Path, pack_path: str | Path | None = None) -> dict[str, Any]:
    questions = load_jsonl(questions_path)
    answers = _by_id(load_jsonl(answers_path), "question_id")
    known_mechanics, card_count, pack_token_count = _pack_stats(pack_path)

    total = len(questions)
    correct = 0
    transfer_total = 0
    transfer_correct = 0
    trap_total = 0
    trap_rejected = 0
    claimed_mechanics = 0
    supported_mechanics = 0
    child_usable = 0
    hidden_doctrine_count = 0
    confidence_scores: list[float] = []

    for question in questions:
        answer = answers.get(question["id"], {})
        is_correct = answer.get("answer") == question.get("answer")
        correct += int(is_correct)
        if question.get("difficulty_band") == "transfer":
            transfer_total += 1
            transfer_correct += int(is_correct)

        if question.get("dominant_trap_choice"):
            trap_total += 1
            rejected = bool(answer.get("dominant_trap_rejected")) and answer.get("answer") != question.get("dominant_trap_choice")
            trap_rejected += int(rejected)

        cited = answer.get("mechanic_ids_used") or []
        claimed_mechanics += len(cited)
        supported = [mechanic_id for mechanic_id in cited if mechanic_id in known_mechanics]
        supported_mechanics += len(supported)
        hidden = int(answer.get("hidden_doctrine_count") or 0)
        hidden += len([mechanic_id for mechanic_id in cited if mechanic_id not in known_mechanics])
        for step in answer.get("answer_steps") or []:
            if step.get("mechanic_id") not in known_mechanics:
                hidden += 1
        hidden_doctrine_count += hidden

        has_trace = bool(cited) and len(supported) == len(cited)
        has_elims = bool(answer.get("eliminations"))
        has_script = bool(answer.get("student_script"))
        has_fact = bool(answer.get("deciding_fact"))
        child_usable += int(has_trace and has_elims and has_script and has_fact and hidden == 0)

        confidence = float(answer.get("confidence") if answer.get("confidence") is not None else 0.5)
        confidence_scores.append(1 - abs(confidence - (1.0 if is_correct else 0.0)))

    accuracy = correct / total if total else 0.0
    transfer_accuracy = transfer_correct / transfer_total if transfer_total else accuracy
    trace_coverage = supported_mechanics / claimed_mechanics if claimed_mechanics else 0.0

    metrics = {
        "accuracy": _round(accuracy),
        "dominant_trap_rejection_rate": _round(trap_rejected / trap_total if trap_total else 0.0),
        "mechanic_trace_coverage": _round(trace_coverage),
        "card_support_rate": _round(trace_coverage),
        "child_usable_trace_rate": _round(child_usable / total if total else 0.0),
        "hidden_doctrine_count": hidden_doctrine_count,
        "confidence_calibration": _round(mean(confidence_scores) if confidence_scores else 0.0),
        "questions_to_mastery": total,
        "transfer_accuracy": _round(transfer_accuracy),
        "card_count": card_count,
        "pack_token_count": pack_token_count,
    }
    return {"question_count": total, "metrics": metrics}


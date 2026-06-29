from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from arl.io import load_jsonl


def _latest_history(history: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in history:
        latest[row["question_id"]] = row
    return latest


def select_questions(questions_path: str | Path, history_path: str | Path, limit: int = 5) -> list[dict[str, Any]]:
    questions = load_jsonl(questions_path)
    history = load_jsonl(history_path) if Path(history_path).exists() else []
    latest = _latest_history(history)
    recent_surfaces = Counter(row.get("surface_cluster") for row in history[-5:] if row.get("surface_cluster"))

    selected: list[dict[str, Any]] = []
    for question in questions:
        row = latest.get(question["id"], {})
        score = 0
        reasons: list[str] = []

        if question.get("dominant_trap_choice") and (not row or row.get("dominant_trap_rejected") is False):
            score += 100
            reasons.append("unresolved_dominant_trap")
        if row.get("correct") is False and float(row.get("confidence") or 0) >= 0.75:
            score += 90
            reasons.append("high_confidence_miss")
        if row.get("correct") is True and (row.get("hidden_doctrine_count", 0) > 0 or row.get("trace_complete") is False):
            score += 80
            reasons.append("hidden_doctrine_or_zero_trace")
        if question.get("needs_transfer"):
            score += 70
            reasons.append("transfer_needed_for_recent_card")
        if question.get("ablation_candidate"):
            score += 60
            reasons.append("ablation_needed")
        if question.get("spaced_review_due"):
            score += 50
            reasons.append("spaced_review_due")
        if question.get("weak_shape"):
            score += 40
            reasons.append("weak_shape")
        if not row:
            score += 30
            reasons.append("coverage_gap")
        if recent_surfaces[question.get("surface_cluster")] > 0:
            score -= 20
            reasons.append("recent_surface_penalty")

        item = dict(question)
        item["selection_score"] = score
        item["selection_reasons"] = reasons
        selected.append(item)

    selected.sort(key=lambda item: (-item["selection_score"], item["id"]))
    return selected[:limit]


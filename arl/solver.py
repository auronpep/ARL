from __future__ import annotations

from typing import Any

from arl.models import MechanicsPack


def _visible_text(question: dict[str, Any]) -> str:
    choices = question.get("choices") or {}
    return " ".join(
        [
            str(question.get("call", "")),
            str(question.get("stem", "")),
            " ".join(str(v) for v in choices.values()),
        ]
    )


def solve_question(question: dict[str, Any], pack: MechanicsPack) -> dict[str, Any]:
    text = _visible_text(question)
    text_lower = text.lower()
    choices = question.get("choices") or {}
    cited = []
    answer_steps = []
    eliminations: dict[str, dict[str, str]] = {}

    for card in pack.cards:
        signal = card.visible_signal.exact_signal.lower()
        if signal and signal in text_lower:
            cited.append(card.id)
            answer_steps.append({"mechanic_id": card.id, "text": card.move})
            for letter, choice in choices.items():
                choice_lower = str(choice).lower()
                for pattern in card.distractor_patterns:
                    if pattern.lower() in choice_lower:
                        eliminations.setdefault(
                            letter,
                            {"filter": "NOT_TRUE_OR_NOT_RESPONSIVE", "reason": card.student_script},
                        )

    survivors = [letter for letter in sorted(choices) if letter not in eliminations]
    answer = survivors[0] if survivors else (sorted(choices)[0] if choices else "")
    dominant_trap_rejected = bool(eliminations)
    script = ""
    if cited:
        first = next(card for card in pack.cards if card.id == cited[0])
        script = first.student_script

    return {
        "question_id": question["id"],
        "answer": answer,
        "confidence": 0.62 if cited else 0.25,
        "phase_used": "CUT" if eliminations else "CALL",
        "mechanic_ids_used": cited,
        "eliminations": eliminations,
        "dominant_trap_rejected": dominant_trap_rejected,
        "dominant_trap_rejection_reason": "Eliminated a listed distractor pattern." if dominant_trap_rejected else "",
        "deciding_fact": "Visible mechanics signal found in question text." if cited else "",
        "student_script": script,
        "answer_steps": answer_steps,
    }


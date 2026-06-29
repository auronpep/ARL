from __future__ import annotations

import json
from typing import Any, Callable

from arl.models import MechanicsPack


PUBLIC_QUESTION_FIELDS = ("id", "subject", "call", "stem", "choices")


def public_question(question: dict[str, Any]) -> dict[str, Any]:
    return {key: question.get(key, "" if key != "choices" else {}) for key in PUBLIC_QUESTION_FIELDS}


def _pack_for_prompt(pack: MechanicsPack) -> list[dict[str, Any]]:
    cards = []
    for card in pack.cards:
        cards.append(
            {
                "id": card.id,
                "type": card.mechanic_type,
                "trigger": card.trigger,
                "visible_signal": card.visible_signal.model_dump(mode="json"),
                "move": card.move,
                "distractor_patterns": card.distractor_patterns,
                "contraindications": card.contraindications,
                "role": card.cut_clash_call_role,
                "student_script": card.student_script,
            }
        )
    return cards


def build_solver_prompt(question: dict[str, Any], pack: MechanicsPack) -> str:
    payload = {
        "question": public_question(question),
        "mechanics_pack": _pack_for_prompt(pack),
        "output_schema": {
            "question_id": "string",
            "answer": "A|B|C|D",
            "confidence": "number 0..1",
            "phase_used": "CUT|CLASH|CALL|ANCHOR",
            "mechanic_ids_used": ["card ids from mechanics_pack"],
            "eliminations": {"A": {"filter": "NOT_TRUE|NOT_RESPONSIVE|OTHER", "reason": "pack-supported reason"}},
            "dominant_trap_rejected": "boolean",
            "dominant_trap_rejection_reason": "string",
            "deciding_fact": "string",
            "student_script": "string",
            "answer_steps": [{"mechanic_id": "card id", "text": "step supported by pack"}],
            "hidden_doctrine_count": "integer",
        },
    }
    return (
        "Solve this Con Law MBE-style question using only the mechanics pack. "
        "Do not use answer keys, explanations, case memory, fairness, policy, or uncited doctrine. "
        "If a step is not supported by a card, increment hidden_doctrine_count. "
        "Return one JSON object only, no markdown.\n\n"
        + json.dumps(payload, indent=2, sort_keys=True)
    )


def parse_answer_response(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise ValueError("model response did not contain a JSON object")


def normalize_answer(raw: dict[str, Any], question: dict[str, Any], pack: MechanicsPack) -> dict[str, Any]:
    choices = set((question.get("choices") or {}).keys())
    known = {card.id for card in pack.cards}
    answer = str(raw.get("answer", "")).strip().upper()
    if answer not in choices:
        answer = sorted(choices)[0] if choices else ""
    mechanic_ids = [str(item) for item in raw.get("mechanic_ids_used", []) if str(item) in known]
    eliminations = raw.get("eliminations") if isinstance(raw.get("eliminations"), dict) else {}
    confidence = raw.get("confidence", 0.5)
    try:
        confidence = min(1.0, max(0.0, float(confidence)))
    except (TypeError, ValueError):
        confidence = 0.5
    hidden = raw.get("hidden_doctrine_count", 0)
    try:
        hidden = max(0, int(hidden))
    except (TypeError, ValueError):
        hidden = 0
    answer_steps = raw.get("answer_steps") if isinstance(raw.get("answer_steps"), list) else []
    if not answer_steps:
        answer_steps = [{"mechanic_id": mechanic_id, "text": "Used cited mechanic."} for mechanic_id in mechanic_ids]

    return {
        "question_id": question["id"],
        "answer": answer,
        "confidence": confidence,
        "phase_used": str(raw.get("phase_used") or ("CUT" if eliminations else "CALL")),
        "mechanic_ids_used": mechanic_ids,
        "eliminations": eliminations,
        "dominant_trap_rejected": bool(raw.get("dominant_trap_rejected", bool(eliminations))),
        "dominant_trap_rejection_reason": str(raw.get("dominant_trap_rejection_reason", "")),
        "deciding_fact": str(raw.get("deciding_fact", "")),
        "student_script": str(raw.get("student_script", "")),
        "answer_steps": answer_steps,
        "hidden_doctrine_count": hidden,
    }


def solve_question_with_provider(question: dict[str, Any], pack: MechanicsPack, provider: Callable[[str], str]) -> dict[str, Any]:
    prompt = build_solver_prompt(question, pack)
    raw = parse_answer_response(provider(prompt))
    return normalize_answer(raw, question, pack)


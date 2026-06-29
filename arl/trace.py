from __future__ import annotations

from pathlib import Path
from typing import Any

from arl.io import load_jsonl
from arl.pack import load_pack


def _question_text(question: dict[str, Any]) -> str:
    choices = question.get("choices") or {}
    return " ".join(
        [
            str(question.get("call", "")),
            str(question.get("stem", "")),
            " ".join(str(value) for value in choices.values()),
        ]
    ).lower()


def audit_trace_support(questions_path: str | Path, answers_path: str | Path, pack_path: str | Path) -> dict[str, Any]:
    questions = {q["id"]: q for q in load_jsonl(questions_path)}
    answers = load_jsonl(answers_path)
    pack = load_pack(pack_path)
    cards = {card.id: card for card in pack.cards}

    items = []
    child_usable_count = 0
    hidden_count = 0
    support_scores: list[float] = []

    for answer in answers:
        question = questions.get(answer["question_id"], {})
        text = _question_text(question)
        cited = answer.get("mechanic_ids_used") or []
        unknown = [mechanic_id for mechanic_id in cited if mechanic_id not in cards]
        visible_triggers = []
        for mechanic_id in cited:
            card = cards.get(mechanic_id)
            if not card:
                continue
            signal = card.visible_signal.exact_signal.lower()
            if signal and signal in text:
                visible_triggers.append(
                    {
                        "mechanic_id": mechanic_id,
                        "trigger_text": card.visible_signal.exact_signal,
                        "location": card.visible_signal.location,
                    }
                )

        unsupported_steps = []
        for step in answer.get("answer_steps") or []:
            mechanic_id = step.get("mechanic_id")
            if not mechanic_id or mechanic_id not in cards:
                unsupported_steps.append(step.get("text", "uncited step"))

        hidden = bool(answer.get("hidden_doctrine_count")) or bool(unknown) or bool(unsupported_steps)
        trace_complete = bool(cited) and not unknown and bool(answer.get("eliminations")) and bool(answer.get("deciding_fact")) and bool(answer.get("student_script"))
        all_visible = len(visible_triggers) == len(cited) if cited else False
        child_usable = trace_complete and all_visible and not hidden
        support_score = 1.0 if child_usable else (len(visible_triggers) / len(cited) if cited else 0.0)

        child_usable_count += int(child_usable)
        hidden_count += int(hidden)
        support_scores.append(support_score)
        items.append(
            {
                "question_id": answer["question_id"],
                "answer": answer.get("answer"),
                "trace_complete": trace_complete,
                "child_usable": child_usable,
                "hidden_doctrine_detected": hidden,
                "unsupported_steps": unsupported_steps,
                "unknown_mechanic_ids": unknown,
                "visible_triggers": visible_triggers,
                "pack_support_score": round(support_score, 6),
            }
        )

    total = len(items)
    return {
        "items": items,
        "summary": {
            "question_count": total,
            "child_usable_trace_rate": round(child_usable_count / total if total else 0.0, 6),
            "hidden_doctrine_count": hidden_count,
            "average_pack_support_score": round(sum(support_scores) / total if total else 0.0, 6),
        },
    }


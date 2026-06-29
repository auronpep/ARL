from __future__ import annotations

from typing import Any


PROMOTION_ORDER = [
    ("accuracy", "higher"),
    ("dominant_trap_rejection_rate", "higher"),
    ("child_usable_trace_rate", "higher"),
    ("hidden_doctrine_count", "lower"),
    ("transfer_accuracy", "higher"),
    ("questions_to_mastery", "lower"),
    ("card_count", "lower"),
    ("pack_token_count", "lower"),
]


def _metrics(summary: dict[str, Any]) -> dict[str, Any]:
    return summary.get("metrics", summary)


def compare_scores(before: dict[str, Any], after: dict[str, Any], gate: str = "promotion") -> dict[str, Any]:
    b = _metrics(before)
    a = _metrics(after)
    if gate == "candidate":
        target_ok = a.get("dominant_trap_rejection_rate", 0) >= b.get("dominant_trap_rejection_rate", 0)
        hidden_ok = a.get("hidden_doctrine_count", 0) <= b.get("hidden_doctrine_count", 0)
        sentinel_ok = a.get("sentinel_breaks", 0) == 0
        return {
            "gate": gate,
            "keep": bool(target_ok and hidden_ok and sentinel_ok),
            "reason": "candidate patch gate passed" if target_ok and hidden_ok and sentinel_ok else "candidate patch gate failed",
        }

    for name, direction in PROMOTION_ORDER:
        if name not in b and name not in a:
            continue
        before_value = b.get(name, 0)
        after_value = a.get(name, 0)
        if direction == "higher":
            if after_value > before_value:
                return {"gate": gate, "keep": True, "reason": f"{name} improved"}
            if after_value < before_value:
                return {"gate": gate, "keep": False, "reason": f"{name} regressed"}
        else:
            if after_value < before_value:
                return {"gate": gate, "keep": True, "reason": f"{name} improved"}
            if after_value > before_value:
                return {"gate": gate, "keep": False, "reason": f"{name} regressed"}
    return {"gate": gate, "keep": False, "reason": "total tie"}


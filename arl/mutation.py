from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from arl.io import load_json, write_yaml
from arl.models import CARD_FIELDS, MechanicsPack, Mutation
from arl.pack import load_pack


def _find_card(cards: list[dict[str, Any]], card_id: str) -> dict[str, Any]:
    for card in cards:
        if card.get("id") == card_id:
            return card
    raise ValueError(f"card not found: {card_id}")


def _append_unique(items: list[Any], value: Any) -> None:
    if value not in items:
        items.append(value)


def apply_mutation_data(pack: MechanicsPack, mutation: Mutation) -> MechanicsPack:
    data = copy.deepcopy(pack.model_dump(mode="json"))
    cards = data["cards"]

    if mutation.operation == "add_card":
        cards.append(mutation.value)
    elif mutation.operation == "update_card_field":
        if not mutation.card_id or not mutation.field:
            raise ValueError("update_card_field requires card_id and field")
        if mutation.field not in CARD_FIELDS:
            raise ValueError(f"unsupported card field: {mutation.field}")
        _find_card(cards, mutation.card_id)[mutation.field] = mutation.value
    elif mutation.operation == "add_contraindication":
        if not mutation.card_id:
            raise ValueError("add_contraindication requires card_id")
        card = _find_card(cards, mutation.card_id)
        _append_unique(card["contraindications"], mutation.value)
    elif mutation.operation == "add_example":
        if not mutation.card_id or not mutation.field:
            raise ValueError("add_example requires card_id and field")
        if mutation.field not in {"positive_examples", "negative_examples"}:
            raise ValueError("add_example field must be positive_examples or negative_examples")
        _append_unique(_find_card(cards, mutation.card_id)[mutation.field], mutation.value)
    elif mutation.operation == "shorten_student_script":
        if not mutation.card_id:
            raise ValueError("shorten_student_script requires card_id")
        _find_card(cards, mutation.card_id)["student_script"] = mutation.value
    elif mutation.operation == "promote_card":
        if not mutation.card_id:
            raise ValueError("promote_card requires card_id")
        _find_card(cards, mutation.card_id)["status"] = "promoted"
    elif mutation.operation == "retire_card":
        if not mutation.card_id:
            raise ValueError("retire_card requires card_id")
        _find_card(cards, mutation.card_id)["status"] = "retired"
    elif mutation.operation == "split_card":
        if not mutation.card_id or not isinstance(mutation.value, list):
            raise ValueError("split_card requires card_id and value list of replacement cards")
        _find_card(cards, mutation.card_id)["status"] = "retired"
        cards.extend(mutation.value)
    elif mutation.operation == "merge_cards":
        source_ids = (mutation.value or {}).get("source_card_ids", [])
        new_card = (mutation.value or {}).get("new_card")
        if not source_ids or not new_card:
            raise ValueError("merge_cards requires source_card_ids and new_card")
        for source_id in source_ids:
            _find_card(cards, source_id)["status"] = "merged"
        cards.append(new_card)
    else:
        raise ValueError(f"unsupported operation: {mutation.operation}")

    return MechanicsPack.model_validate(data)


def apply_mutation_file(pack_path: str | Path, mutation_path: str | Path, dry_run: bool = False) -> MechanicsPack:
    pack = load_pack(pack_path)
    mutation = Mutation.model_validate(load_json(mutation_path))
    updated = apply_mutation_data(pack, mutation)
    if not dry_run:
        write_yaml(pack_path, updated.model_dump(mode="json"))
    return updated


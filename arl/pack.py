from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from arl.io import load_yaml
from arl.models import MechanicsPack


def load_pack(path: str | Path) -> MechanicsPack:
    data = load_yaml(path)
    if data is None:
        raise ValueError(f"empty mechanics pack: {path}")
    return MechanicsPack.model_validate(data)


def validate_pack_file(path: str | Path) -> MechanicsPack:
    try:
        return load_pack(path)
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc


def card_map(pack: MechanicsPack):
    return {card.id: card for card in pack.cards}


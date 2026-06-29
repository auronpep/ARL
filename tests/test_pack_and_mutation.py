from pathlib import Path

from arl.io import load_yaml
from arl.mutation import apply_mutation_file
from arl.pack import validate_pack_file


ROOT = Path(__file__).resolve().parents[1]


def test_seed_pack_validates():
    pack = validate_pack_file(ROOT / "study" / "mechanics_pack.yaml")
    assert len(pack.cards) >= 12


def test_apply_mutation_dry_run_updates_one_field_without_writing():
    pack_path = ROOT / "study" / "mechanics_pack.yaml"
    before = load_yaml(pack_path)
    updated = apply_mutation_file(
        pack_path,
        ROOT / "tests" / "fixtures" / "mutations" / "update_card_field.json",
        dry_run=True,
    )

    target = next(c for c in updated.cards if c.id == "CONLAW-SPENDING-POWER-01")
    assert target.student_script == "Federal money condition: spending power, not police power."
    assert load_yaml(pack_path) == before

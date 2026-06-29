from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


Subject = Literal["CONSTITUTIONAL_LAW"]
SignalLocation = Literal["call", "stem", "answer_choice", "answer_array"]
CardStatus = Literal["candidate", "patch_pending", "promoted", "frozen", "merged", "retired"]
MutationOperation = Literal[
    "add_card",
    "update_card_field",
    "split_card",
    "merge_cards",
    "retire_card",
    "promote_card",
    "add_example",
    "add_contraindication",
    "shorten_student_script",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class VisibleSignal(StrictModel):
    location: SignalLocation
    exact_signal: str


class ExampleRef(StrictModel):
    qid: str
    note: str = ""


class Unlocks(StrictModel):
    traps: list[str] = Field(default_factory=list)
    question_shapes: list[str] = Field(default_factory=list)


class Evidence(StrictModel):
    fixes_misses: list[dict[str, Any]] = Field(default_factory=list)
    dominant_trap_rejections: list[dict[str, Any]] = Field(default_factory=list)
    transfer_passes: list[dict[str, Any]] = Field(default_factory=list)
    negative_examples: list[dict[str, Any]] = Field(default_factory=list)
    ablation: dict[str, Any] = Field(default_factory=dict)


class MechanicCard(StrictModel):
    id: str
    subject: Subject
    group: str
    mechanic_type: str
    trigger: str
    visible_signal: VisibleSignal
    move: str
    contraindications: list[str]
    distractor_patterns: list[str]
    cut_clash_call_role: Literal["CUT", "CLASH", "CALL", "ANCHOR"]
    student_script: str
    ten_year_old_check: str
    positive_examples: list[ExampleRef]
    negative_examples: list[ExampleRef]
    unlocks: Unlocks
    status: CardStatus
    evidence: Evidence
    failure_modes: list[str]
    compression_status: Literal["keep", "merge_candidate", "retire_candidate", "frozen"]


class MechanicsPack(StrictModel):
    version: str = "0.1"
    subject: Subject = "CONSTITUTIONAL_LAW"
    cards: list[MechanicCard]

    @model_validator(mode="after")
    def unique_ids(self) -> "MechanicsPack":
        ids = [card.id for card in self.cards]
        duplicates = sorted({card_id for card_id in ids if ids.count(card_id) > 1})
        if duplicates:
            raise ValueError(f"duplicate card ids: {', '.join(duplicates)}")
        return self


class Mutation(StrictModel):
    mutation_id: str
    hypothesis: str
    target_metric: str
    operation: MutationOperation
    card_id: str | None = None
    field: str | None = None
    value: Any = None
    expected_fix: dict[str, Any] = Field(default_factory=dict)
    rollback: str


CARD_FIELDS = set(MechanicCard.model_fields)


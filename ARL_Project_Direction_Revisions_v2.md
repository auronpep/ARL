## Synthesis

The best combined plan is:

> **Use Codex’s V0 as the build spine, Gemini’s second reply as the engineering hardening layer, and Gemini’s first reply as the later optimization roadmap.**

Codex’s **Pilot Implement v2** has the right immediate scope: Con Law only, fixed scorer, real private Con Law data, mutable `mechanics_pack.yaml`, active question selection, baseline/ablation/holdout runs, and child-usable traces. That is the correct V0. 

Gemini’s first reply is useful, but mostly for **V1/V2**, not V0. TextGrad, DSPy/GEPA, OpenClaw, local open-weights routing, and NotebookLM-style extraction can help later, but adding them now would make the first build too framework-heavy. The one V0 item to take from that reply is **structured generation/validation with Pydantic or equivalent**, because the mechanics pack is the core mutable artifact and malformed cards will poison the loop. 

Gemini’s second reply adds the right hardening ideas: lexicographic comparison, JSON-delta mutations instead of raw YAML rewrites, information-gain question selection, and a stronger 10-year-old verifier. Those should be added, with one refinement: use strict lexicographic comparison for **promotion**, but allow a looser **candidate patch evaluation** stage so the system can test targeted trap repairs without stagnating. 

The existing C3 and BarMatrix architecture already gives the governing grammar. C3 says the system should run **CUT → CLASH → CALL**, use subject FIT overlays, escalate to tiny anchors only after structure stalls, and never call doctrine knowledge pure structure.  The Con Law overlay says this subject’s FIT is **claim categorization + tier/burden consistency**, with the mantra “Claim home first. Burden follows tier. Threshold beats merits.”  The QBank v2 architecture already separates `QBank_Core`, `Choice_Forensics`, `Attempt_Log`, `RedZone_Map`, and `Drill_Queue`, which is exactly the relational structure this loop needs. 

---

# Refined ARL Plan

## 1. Keep V0 deliberately narrow

V0 should prove one thing:

```text
Can a compact Con Law mechanics pack beat no-pack performance,
reject dominant traps,
produce child-usable traces,
and close red zones with fewer targeted questions?
```

Do **not** build the full multi-agent orchestration system yet.

### V0 stack

```text
Python
Pydantic models
ruamel.yaml or safe structured YAML writer
JSONL datasets
pytest fixtures
simple prompt generation
deterministic scoring
manual approval of pack mutations
```

### Defer

```text
TextGrad
DSPy / GEPA
OpenClaw orchestration
local model routing
automated book-wide extraction
full multi-subject expansion
```

Those become useful after the first Con Law loop produces evidence.

---

# 2. Strengthen the architecture with a mutation protocol

The most important engineering change: **the model should never rewrite `mechanics_pack.yaml` directly.**

Use this flow:

```text
LLM proposes mutation JSON
        ↓
tools/apply_mutation.py validates target card and field
        ↓
Pydantic validates the complete card object
        ↓
YAML writer updates the file
        ↓
tools/validate_pack.py runs
        ↓
eval runs
        ↓
keep/reject
```

## Add this file

```text
tools/apply_mutation.py
```

## Mutation schema

```yaml
mutation_id: "MUT-CONLAW-0007"
hypothesis: "Splitting P&I 14th bait from Article IV P&I will reduce wrong-actor clause misses."
target_metric: "dominant_trap_rejection_rate"
operation: "update_card_field"
card_id: "CONLAW-PI14-BAIT-01"
field: "contraindications"
value:
  - "Do not apply this card when the question is about Article IV Privileges and Immunities."
expected_fix:
  trap: "P&I 14th chosen as strongest invalidation basis"
  question_ids:
    - "14240"
rollback: "Restore previous contraindications list."
```

## Allowed operations

```text
add_card
update_card_field
split_card
merge_cards
retire_card
promote_card
add_example
add_contraindication
shorten_student_script
```

No operation should be “rewrite pack.”

---

# 3. Use two keep/reject gates, not one

Gemini’s lexicographic comparison is right for promotion, but too rigid for exploratory repair. A targeted mutation may need to be tested on a small red-zone batch before it earns full promotion.

Use two gates.

## Gate A — candidate patch gate

This gate answers:

```text
Did this mutation fix the specific trap it was designed to fix?
```

A candidate may survive temporarily if:

```text
targeted trap improves
no sentinel question breaks
hidden doctrine decreases or stays flat
trace quality improves or stays flat
```

This does **not** promote the card. It just allows the system to test it further.

## Gate B — promotion gate

This gate uses strict lexicographic comparison:

```text
1. accuracy
2. dominant_trap_rejection_rate
3. child_usable_trace_rate
4. hidden_doctrine_count, lower is better
5. transfer_accuracy
6. questions_to_mastery, lower is better
7. card_count, lower is better
8. pack_token_count, lower is better
```

Promotion vector:

```yaml
promotion_vector:
  accuracy: 0.86
  dominant_trap_rejection_rate: 0.79
  child_usable_trace_rate: 0.74
  hidden_doctrine_count_inverse: -3
  transfer_accuracy: 0.72
  questions_to_mastery_inverse: -18
  card_count_inverse: -31
  pack_token_count_inverse: -8400
```

Rule:

```text
A lower-priority gain cannot excuse a higher-priority loss.
```

But:

```text
Targeted patch survival is not promotion.
```

This avoids stagnation while preserving the “never sacrifice accuracy for compression” principle.

---

# 4. Define `questions_to_mastery` concretely

This metric should not be vague.

Use:

```text
questions_to_mastery =
number of targeted questions consumed from red-zone opening
until the mechanic passes:
  1 near example
  1 far example
  1 negative example
  1 mixed/intersection example
```

A mechanic is not mastered merely because it answered one question.

## Red-zone state machine

```text
open
  ↓
patched
  ↓
transfer_pending
  ↓
closed
  ↓
spaced_review
  ↓
stable
```

## Closure rule

A red zone closes only when:

```text
same trap rejected on a near example
same trap rejected on a far example
card not over-applied to a negative example
trace is child-usable
no hidden-doctrine step is needed
```

This directly serves your goal: **fewer questions, but each question must prove something.**

---

# 5. Refine active question selection

Codex already added `select_next_questions.py`; Gemini correctly emphasized information-value density. The next improvement is to make selection stateful and measurable.

## Add these fields to question JSONL

```yaml
question_shape: "tier_burden_matrix"
dominant_trap_choice: "B"
dominant_trap_mechanic: "burden_tier_mismatch"
expected_axis: "government burden vs challenger burden"
expected_dispositive_fact: "gender classification"
expected_mechanic_ids:
  - "CONLAW-CUT-BURDEN-TIER-01"
  - "CONLAW-CLASH-TIER-BURDEN-01"
surface_cluster: "school_policy"
transfer_cluster: "gender_classification"
difficulty_band: "dev"
```

## Selection priority

```text
1. unresolved dominant trap
2. high-confidence miss
3. correct answer with zero usable trace
4. recently mutated card needing transfer proof
5. ablation candidate needing uniqueness proof
6. spaced-review due item
7. weak Con Law question shape
8. untouched outline/trap intersection
```

## Scoring formula for selection

```text
selection_score =
  100 * unresolved_dominant_trap
+  90  * high_confidence_miss
+  80  * hidden_doctrine_or_zero_trace
+  70  * transfer_needed_for_recent_card
+  60  * ablation_needed
+  50  * spaced_review_due
+  40  * weak_shape
+  30  * coverage_gap
-  20  * recently_seen_surface_cluster
```

This makes the system choose the next question because it is likely to expose or verify a mechanic, not because it is next in a list.

---

# 6. Upgrade the 10-year-old verifier

Gemini’s “zero-knowledge barrier” is directionally right, but an LLM cannot truly erase its latent legal training by prompt. Treat this as a **proxy test**, not literal proof.

The better test is:

```text
Could the answer trace be reconstructed from the pack alone?
```

## Add `tools/audit_trace_support.py`

This tool checks each solver step against the pack.

For every answer explanation, it asks:

```text
Is this step supported by a cited mechanic?
Is the trigger visible in the stem, call, or answer choice?
Is the dispositive fact named?
Is the eliminated choice killed by a listed distractor pattern?
Is there an uncited legal claim?
Could the student script tell the child what to do?
```

## Verifier output

```yaml
question_id: "14241"
answer: "D"
trace_complete: true
child_usable: true
hidden_doctrine_detected: false
unsupported_steps: []
visible_triggers:
  - mechanic_id: "CONLAW-CUT-BURDEN-TIER-01"
    trigger_text: "school must demonstrate"
    location: "answer_choice"
  - mechanic_id: "CONLAW-CLASSIFICATION-GENDER-01"
    trigger_text: "girls only / boys excluded"
    location: "stem"
pack_support_score: 1.0
```

## Add three solver modes

```text
baseline_no_pack
pack_allowed
pack_only_trace_required
```

The key comparison is not just:

```text
Did the model get it right?
```

It is:

```text
Did the mechanics pack make the answer path visible?
```

---

# 7. Integrate directly with BarMatrix/QBank v2

Do not let ARL become a separate system with separate truth. It should be a private experimental loop over the same architecture.

The QBank v2 design already says `Choice_Forensics` is the diagnostic heart of the bank, one row per answer choice, with filter, mold, bait architecture, why attractive, breaker, method class, and lawyer confirmation.  It also uses `Attempt_Log` for performance and miss forensics, including confidence, phase used, error mold, missed trigger fact, misread call, and recovery sentence. 

## Add importer/exporter tools

```text
tools/import_barmatrix_conlaw.py
tools/export_attempts_to_qbank.py
tools/export_cards_to_qbank.py
```

## ARL private JSONL should mirror QBank

```text
data/private/conlaw/questions_dev.jsonl
data/private/conlaw/questions_holdout.jsonl
data/private/conlaw/choice_forensics.jsonl
data/private/conlaw/attempt_history.jsonl
```

## Minimum viable import fields

```yaml
question_id:
subject:
topic:
subtopic:
outline_code:
call:
stem:
choices:
answer:
dominant_trap_choice:
dominant_trap_mold:
dominant_trap_pick_rate:
expected_phase:
expected_axis:
expected_dispositive_fact:
expected_mechanic_ids:
choice_forensics:
  A:
    filter_broken:
    mold_code:
    why_attractive:
    breaker_student:
  B:
    ...
```

This avoids re-inventing the bank while giving ARL the clean JSONL files it needs.

---

# 8. Refine the Con Law card deck spine

Pilot v2 correctly seeds Con Law around:

```text
actor/source-of-power routing
clause-home routing
classification/EP routing
tier × burden matrix
threshold before merits
high-frequency distractor anchors
```

That lines up with the existing Con Law overlay: answer arrays are categorization engines, and the first move is to classify claim, tier, burden, actor, and threshold rather than debate policy strength. 

## Initial Con Law pack should be grouped like this

```text
A. Actor/source-of-power cards
B. Clause-home cards
C. Classification cards
D. Tier/burden cards
E. Threshold cards
F. High-frequency bait cards
G. Tiny anchors
```

## Example card groups

```yaml
group: "A_actor_source_power"
cards:
  - "CONLAW-ACTOR-FIRST-01"
  - "CONLAW-FEDERAL-ENUMERATED-POWER-01"
  - "CONLAW-FEDERAL-POLICE-POWER-BAIT-01"
  - "CONLAW-SPENDING-POWER-01"

group: "C_classification"
cards:
  - "CONLAW-CLASSIFICATION-FIRST-01"
  - "CONLAW-FEDERAL-EP-ANALOGUE-01"
  - "CONLAW-GENDER-INTERMEDIATE-01"
  - "CONLAW-ALIENAGE-STATE-FUNCTION-01"

group: "D_tier_burden"
cards:
  - "CONLAW-BURDEN-TIER-MISMATCH-01"
  - "CONLAW-DEFAULT-RATIONAL-BASIS-01"
  - "CONLAW-STRICT-TRIGGER-REQUIRED-01"

group: "E_threshold"
cards:
  - "CONLAW-STATE-ACTION-FIRST-01"
  - "CONLAW-PROPERTY-INTEREST-TRIGGER-01"
  - "CONLAW-STANDING-CASE-CONTROVERSY-01"

group: "F_bait"
cards:
  - "CONLAW-PI14-BAIT-01"
  - "CONLAW-PUBLIC-IMPORTANCE-BAIT-01"
  - "CONLAW-DUE-PROCESS-WHEN-EP-CLASSIFICATION-BAIT-01"
```

---

# 9. Add a card lifecycle

Pilot v2 already includes `status`, `evidence`, and `failure_modes`. Make that operational.

## Status values

```text
candidate
patch_pending
promoted
frozen
merged
retired
```

## Evidence block

```yaml
evidence:
  fixes_misses:
    - question_id: "14241"
      prior_wrong_choice: "C"
      after_correct: true
  dominant_trap_rejections:
    - question_id: "14241"
      trap_choice: "C"
      rejected: true
  transfer_passes:
    - question_id: "14264"
      surface_cluster: "different"
      result: "pass"
  negative_examples:
    - question_id: "14235"
      avoided_overapplication: true
  ablation:
    tested: true
    removed_card_accuracy_delta: -0.04
    removed_card_trap_delta: -0.11
```

## Promotion rule

A card promotes only if it has:

```text
at least one fixed miss
at least one trap rejection
at least one transfer pass
no serious overapplication
child-usable trace support
```

## Retirement rule

A card retires if:

```text
no evidence after N runs
merged into broader card
causes overapplication
duplicates a stronger card
reduces trace clarity
```

---

# 10. Add a “Mechanics Inbox” before full extraction

Gemini’s NotebookLM suggestion is useful as a manual intake layer, not as the source of truth. Use it to surface candidate mechanics, then put them in a controlled inbox.

## File

```text
study/extraction_inbox.yaml
```

## Schema

```yaml
- inbox_id: "INBOX-CONLAW-0003"
  source_type: "strategy_book"
  source_ref: "Con Law strategy chapter, validity of statutes section"
  raw_strategy_note: "When validity of a law is asked, identify federal vs state actor first."
  candidate_trigger: "Call asks whether a statute is valid."
  candidate_move: "Identify actor first."
  candidate_trap: "Federal police power / wrong amendment against wrong actor."
  candidate_student_script: "Validity question: actor first."
  proposed_card_type: "routing_mechanic"
  merge_candidate: "CONLAW-ACTOR-FIRST-01"
  promote_to_pack: false
  notes: "Needs proof from 3+ Con Law questions."
```

This keeps extraction from becoming automatic bloat.

---

# 11. Define real proof versus tool proof

Codex already says synthetic fixtures prove tooling only and real proof requires private Con Law questions. Keep that. 

## Proof ladder

```text
Level 0 — tooling proof
Synthetic fixtures pass.

Level 1 — baseline proof
No-pack baseline vs seeded-pack run on 20 real Con Law dev questions.

Level 2 — trap proof
Dominant trap rejection improves on real Con Law questions.

Level 3 — trace proof
Correct answers are supported by cited mechanics.

Level 4 — transfer proof
Promoted mechanics work on unseen surface-different questions.

Level 5 — compression proof
Pack shrinks or stays small without losing accuracy or trap rejection.

Level 6 — holdout proof
No edits during sealed holdout; pack beats baseline.
```

## V0 success definition

Use this:

```text
V0 succeeds when the Con Law mechanics pack:
1. beats a no-pack baseline on real private Con Law questions;
2. rejects dominant traps more often;
3. produces child-usable traces;
4. closes red zones with fewer targeted questions;
5. transfers to unseen Con Law questions;
6. does not grow into an outline.
```

That is already essentially Codex’s final success definition; keep it. 

---

# 12. Revised build order

## Sprint 0 — repo and schemas

Deliver:

```text
pyproject.toml
AGENTS.md
README.md
schemas/
tools/validate_pack.py
tools/apply_mutation.py
tests/fixtures/
```

Dependencies:

```text
pydantic
ruamel.yaml
jsonschema
pytest
```

Optional:

```text
tiktoken or token counter
```

## Sprint 1 — seed Con Law mechanics

Deliver:

```text
study/mechanics_pack.yaml
study/tiny_anchors.yaml
study/subject_overlays/constitutional_law.yaml
study/exam_day_scripts/conlaw_script.md
study/extraction_inbox.yaml
```

Seed cards should begin as `candidate`.

## Sprint 2 — import real Con Law data

Deliver:

```text
tools/import_barmatrix_conlaw.py
data/private/conlaw/questions_dev.jsonl
data/private/conlaw/questions_holdout.jsonl
data/private/conlaw/choice_forensics.jsonl
```

Use real private Con Law questions with keys, dominant traps, and expected mechanics.

## Sprint 3 — solver/scorer/verifier

Deliver:

```text
tools/run_solver.py
tools/score_run.py
tools/audit_trace_support.py
tools/run_ten_year_old_test.py
tools/compare_runs.py
```

Run modes:

```text
baseline_no_pack
pack_eval
pack_only_trace_required
ablation_eval
transfer_eval
holdout_eval
```

## Sprint 4 — active learning

Deliver:

```text
tools/select_next_questions.py
reports/conlaw_red_zone_report.md
reports/conlaw_baseline_report.md
```

Selection should prioritize trap repair, high-confidence misses, zero-trace anomalies, transfer checks, and ablation targets.

## Sprint 5 — first promotion cycle

Deliver:

```text
runs/results.tsv
reports/conlaw_holdout_report.md
reports/ten_year_old_verification_report.md
```

First promotion cycle:

```text
1. baseline no-pack run
2. seeded-pack run
3. identify top 3 red zones
4. mutate one card
5. targeted patch run
6. full dev promotion run
7. ablation run
8. holdout only after promotion
```

---

# Final revised instruction to Codex

Use this as the tightened tasking block:

```text
Refine Pilot Implement v2 into a Con Law-only V0 of the MBE Mechanics Autoresearch Lab.

Mission:
Build a private mechanics optimization loop whose objective is near-perfect MBE performance with the fewest practiced questions and the smallest child-usable mechanics pack. This is not a rule-outline project.

Keep:
- Con Law only for V0.
- Fixed scorer.
- Real private Con Law eval data.
- Mutable mechanics pack.
- Active question selection.
- Baseline, ablation, transfer, and holdout runs.
- Child-usable answer traces.

Add these refinements:

1. Structured mutation protocol
- Add tools/apply_mutation.py.
- The model may not rewrite mechanics_pack.yaml directly.
- Mutations must be JSON payloads: add_card, update_card_field, split_card, merge_cards, retire_card, promote_card, add_example, add_contraindication, shorten_student_script.
- Apply mutations programmatically, validate with Pydantic, write YAML only after validation.

2. Two-stage keep/reject
- Candidate patch gate: targeted trap improvement with no sentinel break.
- Promotion gate: strict lexicographic comparison.
- Promotion priority:
  1 accuracy
  2 dominant_trap_rejection_rate
  3 child_usable_trace_rate
  4 hidden_doctrine_count lower
  5 transfer_accuracy
  6 questions_to_mastery lower
  7 card_count lower
  8 pack_token_count lower

3. Questions-to-mastery definition
- Measure number of targeted questions consumed from red-zone opening until the mechanic passes near, far, negative, and mixed/intersection examples.
- Add red-zone states: open, patched, transfer_pending, closed, spaced_review, stable.

4. Trace support audit
- Add tools/audit_trace_support.py.
- Check every solver step against cited mechanic IDs.
- Penalize unsupported legal claims.
- Output pack_support_score, unsupported_steps, hidden_doctrine_detected, child_usable.

5. Active question selection
- tools/select_next_questions.py should prioritize:
  unresolved dominant traps;
  high-confidence misses;
  correct answers with zero usable trace;
  recently mutated cards needing transfer proof;
  ablation candidates;
  spaced-review due items;
  weak Con Law shapes;
  untouched outline/trap intersections.

6. QBank v2 alignment
- Do not create a separate truth system.
- Add tools/import_barmatrix_conlaw.py.
- Mirror QBank_Core, Choice_Forensics, Attempt_Log, RedZone_Map, and Drill_Queue concepts in private JSONL.
- Use choice-forensics data for dominant trap and expected mechanic scoring.

7. Card lifecycle
- Add status values: candidate, patch_pending, promoted, frozen, merged, retired.
- Add evidence fields: fixes_misses, dominant_trap_rejections, transfer_passes, negative_examples, ablation.
- Promote only when a card fixes a miss, rejects a trap, passes transfer, avoids overapplication, and has child-usable trace support.

8. Tooling discipline
- V0 dependencies: Python, Pydantic, ruamel.yaml, jsonschema, pytest.
- Defer TextGrad, DSPy/GEPA, OpenClaw, local model routing, and automated book-wide extraction until after V0 proof.

9. Proof ladder
- Synthetic fixtures prove tools only.
- Real proof requires private Con Law questions.
- Required V0 runs:
  baseline_no_pack;
  seeded_pack;
  targeted_patch;
  full_dev_promotion;
  ablation;
  transfer;
  sealed_holdout.

V0 succeeds when:
The Con Law mechanics pack beats no-pack baseline on real private Con Law questions, rejects dominant traps more often, produces child-usable traces, needs fewer targeted questions to close red zones, transfers to unseen questions, and does not grow into an outline.
```

## Bottom line

The refined plan should be:

```text
Codex V2 spine
+ Gemini math hardening
+ JSON-delta mutation safety
+ information-gain question selection
+ trace-support auditing
+ QBank v2 integration
- premature framework complexity
```

That gives you the fastest route to the real goal: a compact, tested, child-usable MBE mechanics machine that improves toward perfect performance with the fewest questions and the fewest mechanics.

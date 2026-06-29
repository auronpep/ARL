The plan is strong enough to start. It has the right V0 scope: **Con Law only, fixed scorer, mutable mechanics pack, synthetic tests only for tooling, no GPU/autoresearch code dependency**. I would approve it with these targeted changes.

## Highest-value feedback

### 1. Make “fewest questions” a first-class metric

The plan scores accuracy, trap rejection, trace, calibration, and pack size. Add one more core metric:

```text
questions_to_mastery
```

That is central to your goal. The lab should not merely ask, “Does the pack improve accuracy?” It should ask:

```text
How many questions did it take to expose, fix, and verify this mechanic?
```

Add this to `score_run.py` and `compare_runs.py`:

```text
prefer a pack that reaches the same accuracy with fewer practiced questions
prefer a pack that closes the same red zone with fewer targeted questions
prefer a card that transfers after 2–3 questions over a card that needs 10 examples
```

This matches the existing QBank daily-use idea: pick one active red zone, do a small targeted set, log confidence, write one recovery sentence, and update the drill queue rather than doing raw volume. 

### 2. Add `tools/select_next_questions.py` to V0

This is the main missing tool. The plan lists scoring and comparison, but not active question selection.

Add it now, even if simple.

```text
tools/select_next_questions.py
```

It should select the next question by highest expected information value:

```text
1. dominant trap not yet defeated
2. high-confidence prior miss
3. expected mechanic gap
4. weak Con Law sub-shape
5. due spaced-review item
6. unseen transfer item for a recently learned card
```

The existing red-zone model already points this way: red zones should change the next question assigned, with trap red zones drilling the exact mold, C3-component red zones drilling the failed component, and tension-axis red zones using matched-pair or 2x2 drills. 

### 3. Upgrade the 10-year-old verifier from “format check” to “usability check”

The current verifier checks whether the answer cites mechanics, includes eliminations, names a deciding fact, and uses a student script. That is necessary but not enough.

Add a second layer:

```text
10-year-old usability score
```

For each cited mechanic, verify:

```text
trigger words were visible in the stem/call/choice
the mechanic text itself contains the move needed
the student script would actually tell the child what to do
the answer did not rely on uncited doctrine
the same card works on at least one surface-different transfer item
```

The verifier should return:

```yaml
trace_complete: true
child_usable: true
hidden_doctrine_detected: false
transfer_required: false
```

This aligns with the C3 rule that doctrine knowledge must not be mislabeled as pure structure; if a move requires doctrine, it should be marked anchor-assisted or pure anchor. 

### 4. Use Con Law’s existing overlay as the pilot spine

The seed list is good, but the pilot should be explicitly organized around the established Con Law FIT:

```text
Constitutional Law = claim categorization + tier/burden consistency.
Student mantra: Claim home first. Burden follows tier. Threshold beats merits.
```

The plan should group the 12 seed mechanics under these buckets:

```text
A. Actor / source-of-power routing
B. Clause-home routing
C. Classification / Equal Protection routing
D. Tier × burden matrix
E. Threshold before merits
F. High-frequency distractor anchors
```

Con Law is already framed as answer-array categorization, not policy debate: classify claim, tier, burden, actor, and threshold before arguing merits. 

### 5. Treat synthetic tests as tool tests only

The synthetic fixtures are useful for proving scripts work. They should not be allowed to prove that the study system works.

Add this line to the plan:

```text
Synthetic fixtures prove tooling. Real proof requires private Con Law questions with keys, dominant traps, and expected mechanics.
```

Suggested V0 evaluation ladder:

```text
Level 0: synthetic self-test passes
Level 1: 20 real Con Law questions, dev only
Level 2: 40–60 real Con Law questions, stratified by question shape
Level 3: sealed holdout, no pack edits during run
Level 4: transfer set using surface-different questions
```

### 6. Add baseline and ablation runs

To know whether the mechanics pack is doing real work, require three runs:

```text
A. no-pack baseline
B. current mechanics pack
C. ablated pack with one card removed
```

A card earns its place only if it does at least one of these:

```text
improves accuracy
kills a dominant trap
improves trace quality
reduces questions-to-mastery
improves transfer
reduces hidden-law reasoning
```

This prevents the pack from growing into a disguised outline.

### 7. Add a card lifecycle

Right now the plan seeds cards, validates the pack, and mutates the pack. Add status fields so the loop can promote and retire cards cleanly.

```yaml
status: candidate | promoted | frozen | merged | retired
evidence:
  fixes_misses: []
  transfer_passes: []
  ablation_result: null
failure_modes:
  - overapplies_to
  - needs_anchor
  - unclear_trigger
```

This gives the compressor objective evidence for deletion instead of relying on taste.

### 8. Tighten the mechanic schema

The proposed schema is good. Add these fields:

```yaml
visible_signal:
  location: call | stem | answer_choice | answer_array
  exact_signal: ""
contraindications:
  - "Do not use this when..."
positive_examples:
  - qid: ""
negative_examples:
  - qid: ""
unlocks:
  traps:
    - ""
  question_shapes:
    - ""
```

The most important additions are `contraindications` and `negative_examples`. They stop a useful mechanic from becoming an over-applied reflex.

### 9. Score “dominant trap rejection” more explicitly

Do not just score whether the final answer is correct. For every question with pick-rate data or an analytically obvious trap, score whether the solver killed the trap.

Add:

```yaml
dominant_trap_choice: "B"
dominant_trap_mechanic: "federal police power trap"
dominant_trap_rejected: true
dominant_trap_rejection_reason: "wrong actor/power source"
```

This fits the `Choice_Forensics` model, where each answer choice carries filter, mold, why attractive, breaker, and repair signal. 

### 10. Add “pack trace coverage”

A right answer with no trace should not fully pass. The plan already says this. Make it numeric:

```text
trace_coverage = cited_mechanics_that_exist / all_mechanics_claimed
card_support_rate = answer_steps_supported_by_pack / total_answer_steps
hidden_doctrine_count = legal claims not found in pack
```

Then compare:

```text
accuracy_with_trace
accuracy_without_trace
```

The goal is not merely a model that answers correctly. The goal is a note pack that explains the answer path.

### 11. Keep Codex execution optional for longer

The `run_solver.py` idea is good: default prompt generation first, optional execution later.

For V0, keep the solver interface model-agnostic:

```text
input: questions.jsonl + mechanics_pack.yaml
output: answers.jsonl
```

Then Codex, ChatGPT, Claude, or a local script can be swapped in without changing the scorer.

The frozen part should be the **contract**, not the specific model.

### 12. Add a “mechanics extraction intake” file, but not a full extraction engine yet

Since the books are a major source of strategy mechanics, add a lightweight intake artifact now:

```text
study/extraction_inbox.yaml
```

Schema:

```yaml
source_ref: ""
raw_strategy_note: ""
candidate_trigger: ""
candidate_move: ""
candidate_trap: ""
candidate_student_script: ""
merge_candidate: ""
promote_to_pack: false
```

This lets you capture book insights immediately without building the full extractor role in V0.

### 13. Add a weekly sealed-holdout rule

The loop can accidentally overfit to the dev batch. Add:

```text
Do not run holdout after every mutation.
Run holdout only after a promoted pack version.
No edits during holdout run.
Record holdout score separately from dev score.
```

This makes the loop test transfer, not memorization.

### 14. Add pack compression as a scheduled step, not a constant step

Compression should happen after evidence accumulates. Otherwise Codex may shorten useful cards before they have transfer proof.

Add:

```text
Every 5 kept mutations:
  run duplicate detection
  merge overlapping cards
  retire no-evidence cards
  shorten scripts
  rerun dev batch
```

### 15. Put private-input language only in repo setup, not in the model’s research instructions

The plan’s private-input handling is fine as engineering. Keep it in `.gitignore`, `README`, and `AGENTS.md`.

In the model prompts, avoid long warnings. Use simple operational language:

```text
Use the provided private study materials as source input.
Extract mechanics only.
Do not alter questions, keys, or scorer.
```

That keeps the model focused on the study objective.

---

## Concrete additions I would ask them to make

Add these files to V0:

```text
tools/select_next_questions.py
study/extraction_inbox.yaml
reports/conlaw_baseline_report.md
reports/conlaw_holdout_report.md
tests/fixtures/pack_ablation/
```

Add these fields to mechanics cards:

```yaml
visible_signal:
contraindications:
positive_examples:
negative_examples:
unlocks:
status:
evidence:
```

Add these metrics to `score_run.py`:

```text
questions_to_mastery
transfer_accuracy
dominant_trap_rejection_rate
mechanic_trace_coverage
hidden_doctrine_count
card_count
pack_token_count
```

Add these run modes:

```text
baseline_no_pack
pack_eval
ablation_eval
holdout_eval
transfer_eval
```

---

## Revised V0 success definition

Replace their final assumption with this:

```text
The first useful proof is not merely that the scorer rewards traced answers.
The first useful proof is that the Con Law mechanics pack beats a no-pack baseline on real private Con Law questions, rejects the dominant traps more often, uses fewer mechanics than an outline, and transfers to unseen questions with child-usable traces.
```

That sentence keeps the project pointed at your two goals: near-perfect MBE performance, with the fewest questions and the smallest usable mechanics pack.

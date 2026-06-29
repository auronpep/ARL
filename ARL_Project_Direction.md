## Rewritten project direction

This subproject is **not** a rule-memorization project.

It is a private **MBE Mechanics Autoresearch Lab**.

The goal is to distill the books, strategy notes, question bank, wrong-answer data, and C3 method into the smallest working set of **mechanics, strategies, routing moves, trap detectors, tiny anchors, and exam-day procedures** that can produce near-perfect or perfect performance on the California Bar MBE-style multiple-choice questions.

The C3 foundation already fits this: the credited answer is the one that is both **true** and **responsive**, and the distractors are engineered to fail one of those filters.  The operational method is **CUT → CLASH → CALL**, with the Ear catching not-true answers and Issue-Sense catching true-but-not-responsive answers.  The subject overlays are also already framed correctly: universal C3 core → subject FIT overlay → card drills → tiny-anchor escalation → calibrated confidence, not a conventional law outline. 

---

# ARL Project Brief

## North Star

Build the smallest private study system that can make the MBE mechanically solvable.

The final output should be an **exam machine**, not an outline:

```text
trigger → routing move → answer-array pattern → distractor kill → clash axis → resolving fact → tiny anchor if needed
```

The system should learn:

* what facts matter;
* what calls are really asking;
* what answer choices are usually bait;
* what distractors recur by subject;
* which legal phrases are almost always wrong;
* which two-answer clashes repeat;
* which tiny anchors unlock whole clusters of questions;
* how to solve more questions after doing fewer questions.

---

# Ultimate Goals

## Goal 1 — Perfect or near-perfect MBE mastery with minimum input

The system should optimize for:

```text
maximum correct answers
minimum questions practiced
minimum mechanics learned
minimum notes carried
minimum time per question
maximum transfer to unseen questions
```

The desired end state:

```text
Given the private California Bar / MBE-style question universe,
the study program finds the smallest mechanics pack that lets me answer all or nearly all of them correctly.
```

The loop should not reward long outlines. It should reward compact mechanics that repeatedly kill real traps.

## Goal 2 — The Smart 10-Year-Old Verification Test

Assume a smart 10-year-old child has:

```text
no law school
limited legal background
the private C3 study program
the mechanics pack
the tiny-anchor notes
open-note access during the verification exam
```

The verification question is:

```text
Can the child use only these notes and mechanics to get a strong passing score, ideally near perfect, on the MBE portion?
```

This test keeps the project honest.

A card fails if it secretly requires law-school intuition. A card passes if a smart child can apply it mechanically:

```text
see trigger → run move → reject trap → choose survivor
```

This is the core standard for the entire project.

---

# What the system is extracting

Not this:

```text
Congress has the power to tax and spend for the general welfare.
```

But this:

```yaml
id: CONLAW-FEDERAL-POWER-SPEND-01
type: tiny_anchor
trigger: "Federal statute conditions or distributes money."
move: "Look for taxing/spending power before police power."
distractor_patterns:
  - "Federal police power"
  - "General welfare as free-standing legislative power"
student_script: "Federal money statute: spend power, not police power."
ten_year_old_test: "Can the student spot that federal + police power is a trap?"
```

Not this:

```text
Equal Protection applies to the states through the Fourteenth Amendment.
```

But this:

```yaml
id: CONLAW-EP-CLASSIFICATION-01
type: routing_mechanic
trigger: "The law divides people into groups."
move: "Classification usually routes to Equal Protection."
actor_check:
  state_actor: "Fourteenth Amendment Equal Protection"
  federal_actor: "Fifth Amendment Due Process as EP-equivalent"
distractor_patterns:
  - "Due process answer when classification is the obvious feature"
  - "Fourteenth Amendment Equal Protection against federal actor"
student_script: "Classification first. Then actor."
```

Not this:

```text
Privileges or Immunities Clause is narrowly construed.
```

But this:

```yaml
id: CONLAW-PI14-DISTRACTOR-01
type: distractor_frequency_card
trigger: "Answer choice uses Fourteenth Amendment Privileges or Immunities to invalidate a state law."
move: "Treat as a weak MBE answer unless the facts specifically involve narrow national-citizenship rights."
distractor_patterns:
  - "P&I 14th offered when Due Process or Equal Protection is stronger"
student_script: "P&I 14th is usually bait."
```

---

# Core artifact: the Mechanics Pack

Replace `study/knowledge.md` with:

```text
study/mechanics_pack.yaml
study/tiny_anchors.yaml
study/subject_overlays/
study/exam_day_scripts/
study/red_zone_cards.yaml
```

The main file is not a rule outline. It is a compressed operating manual.

## Mechanic schema

```yaml
id: CONLAW-ACTOR-FIRST-01
subject: CONSTITUTIONAL_LAW
mechanic_type: routing_mechanic
trigger: "Question asks whether a statute or government action is valid."
first_move: "Identify actor before doctrine."
steps:
  - "Federal actor: look for enumerated power or valid spending/commerce hook."
  - "State actor: look for constitutional limit, right, classification, burden, or threshold."
distractor_patterns:
  - "Federal police power"
  - "Wrong amendment against wrong actor"
  - "Clause that sounds constitutional but does not own this claim"
cut_clash_call_role: CUT
student_script: "Actor first. Federal needs power. State needs limit."
ten_year_old_check: "Can the student identify the actor and eliminate the wrong-actor answer?"
compression_status: keep
```

Every card needs:

```text
trigger
move
distractor pattern
exam-day script
proof examples
10-year-old usability check
```

No card should exist merely because it is legally true.

---

# Autoresearch-style loop

Use the autoresearch idea as the operating model:

```text
fixed private source corpus
fixed scorer
fixed evaluation batches
one mutable mechanics pack
agent proposes one improvement
run evaluation
keep only if it improves the target
```

For this project, the mutable artifact is not code. It is the study machine:

```text
mechanics_pack.yaml
tiny_anchors.yaml
subject_overlay cards
exam_day_scripts
```

## Loop

```text
1. Extract candidate mechanics from books and explanations.
2. Normalize them into cards.
3. Test the current pack on a small question batch.
4. Record answer, trap rejected, mechanism used, confidence, and miss type.
5. Mutate one thing in the pack.
6. Re-test.
7. Keep the change only if it improves mastery, compression, or transfer.
8. Repeat until the smallest reliable pack remains.
```

The BarMatrix v2 architecture already supports this loop: `QBank_Core` tracks routing and validation, `Choice_Forensics` stores one row per answer choice and its trap mechanics, `Attempt_Log` stores performance evidence, and `RedZone_Map` / `Drill_Queue` convert misses into the smallest next repair set. 

---

# Scoring objective

Use a lexicographic score, not a simple word-count score.

## Priority order

```text
1. Correct answer rate
2. Dominant-trap rejection
3. Correct mechanism used
4. Transfer to unseen questions
5. Fewer questions required to reach mastery
6. Smaller mechanics pack
7. Faster exam-day execution
```

Accuracy comes first. Compression comes after accuracy.

## Suggested run score

```text
RunScore =
  10000 * accuracy
+  2000  * dominant_trap_rejection_rate
+  1000  * mechanism_trace_accuracy
+  500   * confidence_calibration
-  25    * questions_needed_to_reach_mastery
-  5     * number_of_mechanics_cards
-  0.05  * mechanics_pack_tokens
-  100   * unexplained_legal_intuition_uses
```

The last penalty means: if the solver gets the answer right but cannot trace it to a card, the pack did not teach the move yet.

---

# The 10-year-old verification harness

Create a separate evaluator called:

```text
tools/run_ten_year_old_test.py
```

The solver receives only:

```text
question stem
answer choices
call of the question
mechanics_pack.yaml
tiny_anchors.yaml
exam_day_script.md
```

The solver must output:

```yaml
answer: "C"
confidence: 0.85
phase_used: "CLASH"
mechanic_ids_used:
  - CONLAW-EP-CLASSIFICATION-01
  - CONLAW-FEDERAL-ACTOR-01
eliminations:
  A:
    filter: "NOT_RESPONSIVE"
    reason: "Answers state action instead of actor power."
  B:
    filter: "NOT_TRUE"
    reason: "Wrong actor clause."
  D:
    filter: "NOT_RESPONSIVE"
    reason: "Policy argument, not constitutional hook."
deciding_fact: "The statute is federal."
student_script: "Federal actor first. No federal police power."
```

A correct answer without a usable trace does not fully pass.

The verifier asks:

```text
Could the child have found this move from the notes?
Could the child have rejected the dominant trap?
Could the child explain why the credited answer survives?
Could the child repeat the move on a surface-different question?
```

---

# Question-minimization strategy

The goal is not to grind thousands of questions. The goal is to extract maximum information from the fewest questions.

## Each question must produce one of five things

```text
1. A reusable mechanic
2. A tiny anchor
3. A red-zone diagnosis
4. A proof that an existing card transfers
5. A proof that no new study is needed
```

If a question produces none of those, it was low-value practice.

## Active question selection

The system should choose the next question by asking:

```text
Which unanswered or previously missed question is most likely to expose a missing mechanic?
```

Priority:

```text
1. Questions with high dominant-trap selection rates
2. Questions missed with high confidence
3. Questions where the solver used legal intuition not found in the pack
4. Questions from weak outline/trap intersections
5. Questions that test whether a card transfers to a new surface story
```

## Stop rule for a mechanic

A mechanic is provisionally mastered when the solver can apply it across:

```text
near example
far example
surface-disguised example
mixed-subject or adjacent-doctrine example, when applicable
```

Then stop drilling that mechanic except for spaced verification.

---

# Subject overlay format

Each subject needs a FIT, not a mini-outline.

The existing overlay style is correct: Civil Procedure is framed as “procedural posture + structural prerequisite,” and Constitutional Law as “claim categorization + tier/burden consistency.” 

Use this template for every subject:

```yaml
subject: CONSTITUTIONAL_LAW
fit: "Constitutional Law = claim categorization + tier/burden consistency."
student_mantra: "Claim home first. Burden follows tier. Threshold beats merits."
dominant_question_shapes:
  - "validity of statute"
  - "best argument for upholding/invalidating statute"
  - "actor/right/classification/tier/burden arrays"
dominant_cut_patterns:
  - "wrong actor"
  - "burden-tier mismatch"
  - "fundamental-right inflation"
  - "doctrine-home outlier"
dominant_clash_patterns:
  - "tier × burden matrix"
  - "doctrine-home array"
  - "state action threshold pair"
dominant_call_patterns:
  - "threshold before merits"
  - "burden-tier consistency"
  - "default tier unless trigger appears"
tiny_anchors:
  - "federal police power is bait"
  - "P&I 14th is usually weak/bait"
  - "federal EP analogue routes through Fifth Amendment Due Process"
```

---

# The extraction prompt for books

Use this prompt against strategy-book passages:

```text
Extract only MBE operating mechanics.

Do not summarize doctrine.
Do not write a rule outline.
Do not preserve long prose.

For each useful item, produce a card with:

1. Trigger: what the student sees in the call, stem, or answer choice.
2. Move: what to do immediately.
3. Trap: what wrong answer this defeats.
4. Frequency signal: whether the book implies this is common, rare, or a named MBE habit.
5. Student script: a short sentence usable under exam time.
6. Card type:
   - routing_mechanic
   - cut_mechanic
   - clash_axis
   - call_tiebreaker
   - tiny_anchor
   - distractor_frequency_card
   - red_zone_warning
7. Ten-year-old test:
   - Can a smart child apply this from notes?
   - What exact words or facts would trigger it?
8. Compression:
   - Can this merge with an existing mechanic?
   - Is it narrower than an outline rule?
```

Example extracted item:

```yaml
id: CONLAW-VALIDITY-ACTOR-FIRST-01
type: routing_mechanic
trigger: "Call asks whether a statute is valid."
move: "First identify whether the statute is federal or state."
trap: "Choosing a power or clause that applies to the wrong actor."
student_script: "Validity question: actor first."
```

---

# Agent roles

## 1. Extractor

Reads strategy books and explanations.

Output:

```text
candidate mechanics
candidate tiny anchors
candidate distractor-frequency rules
```

## 2. Normalizer

Turns messy notes into schema-clean cards.

Output:

```text
valid mechanics_pack.yaml entries
merged duplicates
short student scripts
```

## 3. Solver

Answers questions using only the current mechanics pack.

Output:

```text
answer
confidence
mechanic trace
eliminations
dominant trap handling
```

## 4. Scorer

Compares solver output against the key and against expected mechanics.

Output:

```text
accuracy
dominant trap rejection
mechanic trace score
confidence calibration
questions-to-mastery estimate
```

## 5. Compressor

Deletes, merges, tightens, and ranks cards.

Output:

```text
smaller mechanics pack
same or better score
cleaner exam-day script
```

## 6. Teacher

Turns mastered mechanics into study materials.

Output:

```text
one-page subject scripts
microdrills
red-zone drills
tiny-anchor cards
```

---

# What mutations are allowed

The loop may change the mechanics pack only in ways that improve the study machine.

Allowed:

```text
add one mechanic
delete one weak card
merge duplicates
tighten a trigger
split an overbroad card
add a distractor signature
add a tiny anchor
rewrite a student script to be shorter
downgrade a fake structural move into anchor-assisted
promote a repeated anchor into the core pack
```

Not useful:

```text
cosmetic rewrites
longer doctrine summaries
new cards that do not fix misses
changes that improve wording but not performance
changes that make the pack feel complete without increasing transfer
```

Every change must answer:

```text
Which miss does this fix?
Which trap does this kill?
Which question count does this reduce?
Which child-usable move does this clarify?
```

---

# Data structure

```text
ARL/
  AGENTS.md
  program.md
  README.md

  data/
    private/
      books/
      questions/
      answer_keys/
      explanations/
    processed/
      eval_dev.jsonl
      eval_holdout.jsonl
      mechanic_examples.jsonl

  study/
    mechanics_pack.yaml
    tiny_anchors.yaml
    subject_overlays/
      constitutional_law.yaml
      civil_procedure.yaml
      evidence.yaml
      contracts.yaml
      torts.yaml
      criminal.yaml
      real_property.yaml
    exam_day_scripts/
      global_30_second_workflow.md
      conlaw_script.md
      civpro_script.md
    red_zone_cards.yaml

  prompts/
    extract_mechanics.md
    normalize_cards.md
    answer_with_pack.md
    compress_pack.md
    ten_year_old_verifier.md

  tools/
    run_solver.py
    score_run.py
    compare_runs.py
    select_next_questions.py
    extract_book_mechanics.py
    run_ten_year_old_test.py
    build_red_zone_map.py

  runs/
    results.tsv
    run_logs/

  reports/
    mechanics_pack_report.md
    red_zone_report.md
    ten_year_old_verification_report.md
```

---

# First pilot: Constitutional Law

Start with Constitutional Law because the strategy-book examples are already mechanical.

## Seed mechanics to extract first

```text
1. Validity question → actor first.
2. Federal statute → enumerated power or spending/commerce hook.
3. Federal police power → trap.
4. Welfare Clause name is misleading → tax/spend scope.
5. State statute with classification → Equal Protection route.
6. Federal classification → Fifth Amendment Due Process as EP analogue.
7. P&I 14th → usually weak/distractor unless narrow national-citizenship right.
8. State action threshold before merits.
9. Public employment property interest → look for tenure, contract, for-cause limit.
10. Speech permit → narrow standards limiting official discretion.
11. Same-sex marriage disadvantage → EP violation anchor.
12. Contracts Clause issue → first check whether contract predates statute.
```

## Pilot benchmark

Use:

```text
20–30 extracted Con Law mechanics
50–100 Con Law questions
one dev set
one holdout set
one red-zone drill queue
```

## Pilot deliverables

```text
study/subject_overlays/constitutional_law.yaml
study/tiny_anchors.yaml
study/exam_day_scripts/conlaw_script.md
reports/conlaw_mechanics_report.md
reports/conlaw_red_zone_report.md
reports/ten_year_old_verification_report.md
```

---

# Exam-day script target

The final scripts should look like Lesson 14’s compressed workflow: frame the call, cut not-true and not-responsive choices, clash the last two on one axis, call only if needed, then calibrate and commit. 

Example global script:

```text
1. Read the call.
2. Name the task.
3. Predict the issue before choices.
4. Run CUT:
   - false?
   - overclaim?
   - wrong actor?
   - wrong purpose?
   - true but off-question?
5. If one survives, confirm call + key fact, then commit.
6. If two survive, name the axis.
7. Find the splitting fact.
8. If no fact resolves it, use a tiny anchor or flag.
9. Record the miss as a red-zone mechanic, not as vague review.
```

---

# Codex instruction block

Use this as the revised instruction:

```text
Create ARL as a private MBE Mechanics Autoresearch Lab.

Mission:
Distill the smallest reliable set of MBE mechanics, strategies, methodologies, trap detectors, answer-array patterns, and tiny anchors that can produce perfect or near-perfect performance on the California Bar MBE-style multiple-choice questions.

This is not a rule-memorization project.
Do not optimize for a shorter legal outline.
Optimize for the smallest working exam machine.

Ultimate goals:
1. Maximize correct answers while minimizing questions practiced, mechanics learned, notes carried, and time spent.
2. Verify the pack using the Smart 10-Year-Old Test: a smart child with limited legal background, the private study program, and open-note access should be able to use the mechanics to get a strong passing score, ideally near perfect.

Core artifact:
Replace study/knowledge.md with study/mechanics_pack.yaml.

Each mechanic card must include:
- id
- subject
- mechanic_type
- trigger
- move
- distractor_patterns
- CUT/CLASH/CALL role
- student_script
- tiny_anchor link if needed
- ten_year_old_check
- proof_examples
- compression_status

The mutable artifact is the mechanics pack, not the question bank.

Loop:
1. Extract candidate mechanics from private books, explanations, wrong-answer notes, and C3 analysis.
2. Normalize them into compact cards.
3. Run the solver on a small question batch using only the mechanics pack.
4. Score answer accuracy, dominant-trap rejection, mechanism trace, confidence calibration, transfer, and compression.
5. Make one small mutation to the pack.
6. Keep the mutation only if it improves accuracy, trap rejection, transfer, compression, or questions-to-mastery.
7. Revert changes that are cosmetic or do not improve performance.
8. Repeat until the smallest reliable pack remains.

Scoring priority:
1. Accuracy
2. Dominant-trap rejection
3. Correct mechanism trace
4. Transfer to unseen questions
5. Fewer questions needed
6. Fewer mechanics
7. Shorter notes
8. Faster execution

Required tools:
- tools/run_solver.py
- tools/score_run.py
- tools/compare_runs.py
- tools/select_next_questions.py
- tools/extract_book_mechanics.py
- tools/run_ten_year_old_test.py
- tools/build_red_zone_map.py

Required data:
- private question JSONL
- answer key JSONL
- strategy-book extraction notes
- attempt logs
- mechanics pack
- red-zone map

Answerer protocol:
The answerer may see only:
- stem
- call
- choices
- mechanics_pack.yaml
- tiny_anchors.yaml
- exam_day_script.md

The answerer must output:
- answer
- confidence
- CUT/CLASH/CALL phase
- mechanic IDs used
- eliminated choices with filters
- dominant trap
- deciding fact
- student script

A right answer with no trace does not fully pass.
A card that cannot be used by the Smart 10-Year-Old verifier must be rewritten, split, or converted into a tiny anchor.

First pilot:
Subject = Constitutional Law.
Start by extracting actor-first, classification-first, federal/state distinction, P&I 14th distractor, federal police-power trap, tax/spend anchor, state-action threshold, property-interest trigger, speech-permit discretion, and Contracts Clause preexisting-contract trigger.

Deliverables:
- study/mechanics_pack.yaml
- study/tiny_anchors.yaml
- study/subject_overlays/constitutional_law.yaml
- study/exam_day_scripts/conlaw_script.md
- reports/conlaw_mechanics_report.md
- reports/red_zone_report.md
- reports/ten_year_old_verification_report.md

Project rule:
No change for change's sake.
Every change must improve correctness, reduce questions needed, compress the pack, clarify a child-usable move, or kill a recurring trap.
```

---

# Bottom line

Build a private loop that asks one question over and over:

```text
What is the smallest mechanical note that would let a smart non-lawyer reject this trap and pick the right answer next time?
```

That is the project.

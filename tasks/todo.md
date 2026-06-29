# ARL Implementation Ledger

## Plan

- [x] Create project scaffold and tracked proof files.
- [x] Add schemas, seed mechanics, and fixtures.
- [x] Implement validation, mutation, scoring, comparison, selection, and trace tools.
- [x] Initialize private GitHub repo safely.
- [x] Run verification suite and record proof.

## Review

Implemented V0 as a Con Law-only mechanics pilot.

Artifacts:

- Private GitHub repo: `https://github.com/auronpep/ARL`
- Initial commit: `99894bd Initial ARL Con Law mechanics pilot`
- Core pack: `study/mechanics_pack.yaml` with 12 seed cards
- Tool package: `arl/`
- CLI wrappers: `tools/`
- Synthetic fixtures: `tests/fixtures/`
- Private data ignored under `data/private/`

Verification:

- `uv sync` passed.
- `uv run pytest` passed: 7 tests.
- `uv run python tools\validate_pack.py study\mechanics_pack.yaml` passed: 12 cards.
- `uv run python tools\apply_mutation.py --pack study\mechanics_pack.yaml --mutation tests\fixtures\mutations\update_card_field.json --dry-run` passed.
- `uv run python tools\score_run.py --questions tests\fixtures\conlaw_questions.jsonl --answers tests\fixtures\conlaw_answers_good.jsonl --out runs\selftest\score.json` passed with accuracy `1.0`, trap rejection `1.0`, trace coverage `1.0`, hidden doctrine `0`.
- `uv run python tools\audit_trace_support.py --questions tests\fixtures\conlaw_questions.jsonl --answers tests\fixtures\conlaw_answers_good.jsonl --pack study\mechanics_pack.yaml --out runs\selftest\trace.json` passed with child-usable trace rate `1.0`.
- `uv run python tools\run_ten_year_old_test.py --questions tests\fixtures\conlaw_questions.jsonl --answers tests\fixtures\conlaw_answers_good.jsonl --pack study\mechanics_pack.yaml --out runs\selftest\ten_year_old.json` passed.
- `uv run python tools\compare_runs.py --before tests\fixtures\score_before.json --after tests\fixtures\score_after_better.json` passed: keep due to improved dominant trap rejection.
- `uv run python tools\select_next_questions.py --questions tests\fixtures\conlaw_questions.jsonl --history tests\fixtures\attempt_history.jsonl --out runs\selftest\next_questions.jsonl` passed.
- `git check-ignore -v data/private/conlaw/questions_dev.jsonl` proved private question files are ignored.
- `gh repo view auronpep/ARL --json nameWithOwner,visibility,url` proved visibility `PRIVATE`.

Boundary:

- Synthetic fixtures prove tooling only.
- Real proof still requires importing private Con Law questions with keys, dominant traps, expected mechanics, and sealed holdout data.

## 2026-06-29 Private Con Law Set 1 Import

- [x] Copy `ConLaw_Set1.xlsx` and `Con_Law_Study_Tactics.md` into ignored private source storage.
- [x] Add a repeatable XLSX/strategy import tool.
- [x] Generate private Con Law question JSONL and strategy mechanics candidates.
- [x] Verify row counts, answer distribution, ignored private outputs, and tests.

Review:

- Private source copies:
  - `data/private/conlaw/source/ConLaw_Set1.xlsx`
  - `data/private/conlaw/source/Con_Law_Study_Tactics.md`
- Private generated outputs:
  - `data/private/conlaw/questions_set1.jsonl`
  - `data/private/conlaw/questions_dev.jsonl`
  - `data/private/conlaw/questions_holdout.jsonl`
  - `data/private/conlaw/answer_key_set1.jsonl`
  - `data/private/conlaw/choice_forensics_set1.jsonl`
  - `data/private/conlaw/strategy_mechanics_candidates.yaml`
- Public proof summary: `data/processed/conlaw_set1_import_summary.json`
- Import summary: 146 total questions, 117 dev, 29 holdout, 584 choice-forensics rows, answer counts A=33/B=37/C=33/D=43.
- Initial strategy tagging: 105 questions with expected mechanics/dominant-trap mechanic, 41 unclassified for follow-up review.
- Shape counts: actor/source-power 30, classification/equal-protection 40, threshold 34, clause-home 1, unclassified 41.
- Markdown strategy extraction produced 10 private candidate mechanics signals.
- `git check-ignore -v` confirmed private source and generated question files are ignored by `.gitignore`.
- `uv run pytest` passed: 9 tests.

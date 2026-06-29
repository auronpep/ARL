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

## ARL Mission

This project is a private MBE Mechanics Autoresearch Lab. It is not a rule-outline or rule-memorization project.

The V0 scope is Constitutional Law only. Optimize for the smallest child-usable mechanics pack that improves real MBE-style performance, dominant-trap rejection, transfer, and questions-to-mastery.

## Operating Rules

- Treat `study/mechanics_pack.yaml` as structured data, not prose.
- Do not rewrite `study/mechanics_pack.yaml` directly. Use `tools/apply_mutation.py` with a JSON mutation payload.
- Do not alter private questions, answer keys, scorer logic, or holdout data during an evaluation run.
- Synthetic fixtures prove tooling only. Real proof requires private Con Law questions with answer keys and choice forensics.
- Holdout runs happen only after a promoted pack version; no pack edits during holdout.
- Keep private inputs under `data/private/`; they are ignored by Git.

## V0 Gates

Promotion uses strict lexicographic comparison:

1. accuracy
2. dominant_trap_rejection_rate
3. child_usable_trace_rate
4. hidden_doctrine_count lower
5. transfer_accuracy
6. questions_to_mastery lower
7. card_count lower
8. pack_token_count lower

A lower-priority gain cannot excuse a higher-priority loss.

## Global Safety

Never push to public repositories. Before any push, verify the target remote and repository visibility. This repo should have only the private `origin` remote for `auronpep/ARL`.

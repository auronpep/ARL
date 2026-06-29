from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.mutation import apply_mutation_file


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", required=True)
    parser.add_argument("--mutation", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    updated = apply_mutation_file(args.pack, args.mutation, dry_run=args.dry_run)
    print(f"mutation valid: {len(updated.cards)} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


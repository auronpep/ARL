from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.io import write_jsonl
from arl.select_questions import select_questions


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--history", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    selected = select_questions(args.questions, args.history, limit=args.limit)
    write_jsonl(args.out, selected)
    print(f"selected {len(selected)} questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


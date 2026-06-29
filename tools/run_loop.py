from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.io import write_json
from arl.loop import run_loop


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", default="data/private/conlaw/questions_dev.jsonl")
    parser.add_argument("--pack", default="study/mechanics_pack.yaml")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--summary-out")
    args = parser.parse_args()

    summary = run_loop(args.questions, args.pack, args.out_dir, iterations=args.iterations)
    if args.summary_out:
        write_json(args.summary_out, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["iterations_completed"] == args.iterations else 1


if __name__ == "__main__":
    raise SystemExit(main())


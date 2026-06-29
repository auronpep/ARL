from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.io import write_json
from arl.scoring import score_run


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--answers", required=True)
    parser.add_argument("--pack", default="study/mechanics_pack.yaml")
    parser.add_argument("--out")
    args = parser.parse_args()
    summary = score_run(args.questions, args.answers, args.pack)
    if args.out:
        write_json(args.out, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


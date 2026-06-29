from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.compare import compare_scores
from arl.io import load_json


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    parser.add_argument("--gate", choices=["candidate", "promotion"], default="promotion")
    args = parser.parse_args()
    result = compare_scores(load_json(args.before), load_json(args.after), gate=args.gate)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


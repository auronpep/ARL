from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.io import write_json
from arl.trace import audit_trace_support


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--answers", required=True)
    parser.add_argument("--pack", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    report = audit_trace_support(args.questions, args.answers, args.pack)
    if args.out:
        write_json(args.out, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


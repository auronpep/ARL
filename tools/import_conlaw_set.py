from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.conlaw_import import import_conlaw_set
from arl.io import write_json


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx", required=True)
    parser.add_argument("--strategy-md", required=True)
    parser.add_argument("--out-dir", default="data/private/conlaw")
    parser.add_argument("--summary-out")
    args = parser.parse_args()

    summary = import_conlaw_set(args.xlsx, args.strategy_md, args.out_dir)
    if args.summary_out:
        write_json(args.summary_out, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


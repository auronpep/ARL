from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.io import write_json
from arl.lm_studio import chat
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
    parser.add_argument("--solver", choices=["deterministic", "lm-studio"], default="deterministic")
    parser.add_argument("--lm-studio-base-url", default="http://127.0.0.1:5962")
    parser.add_argument("--model")
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--timeout-sec", type=int, default=600)
    args = parser.parse_args()

    provider = None
    if args.solver == "lm-studio":
        provider = lambda prompt: chat(  # noqa: E731
            prompt,
            args.lm_studio_base_url,
            model=args.model,
            max_tokens=args.max_tokens,
            timeout_sec=args.timeout_sec,
        )[0]
    summary = run_loop(args.questions, args.pack, args.out_dir, iterations=args.iterations, answer_provider=provider)
    if args.summary_out:
        write_json(args.summary_out, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["iterations_completed"] == args.iterations else 1


if __name__ == "__main__":
    raise SystemExit(main())

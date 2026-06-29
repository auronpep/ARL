from pathlib import Path
import os
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.lm_studio import chat as lm_studio_chat, normalize_base_url


def build_prompt(questions: str, pack: str, tiny_anchors: str, script: str) -> str:
    return "\n\n".join(
        [
            "You are solving Con Law MBE-style questions using only the provided mechanics pack.",
            "Output JSONL with question_id, answer, confidence, phase_used, mechanic_ids_used, eliminations, dominant_trap_rejected, dominant_trap_rejection_reason, deciding_fact, student_script, and answer_steps.",
            "# Questions\n" + Path(questions).read_text(encoding="utf-8"),
            "# Mechanics Pack\n" + Path(pack).read_text(encoding="utf-8"),
            "# Tiny Anchors\n" + Path(tiny_anchors).read_text(encoding="utf-8"),
            "# Exam Script\n" + Path(script).read_text(encoding="utf-8"),
        ]
    )


def normalize_lm_studio_base_url(base_url: str) -> str:
    return normalize_base_url(base_url)


def extract_chat_content(response: dict) -> str:
    return response["choices"][0]["message"].get("content", "")


def run_lm_studio(prompt: str, base_url: str, model: str | None, max_tokens: int, timeout_sec: int) -> tuple[str, str]:
    return lm_studio_chat(prompt, base_url, model=model, max_tokens=max_tokens, timeout_sec=timeout_sec)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--pack", default="study/mechanics_pack.yaml")
    parser.add_argument("--tiny-anchors", default="study/tiny_anchors.yaml")
    parser.add_argument("--script", default="study/exam_day_scripts/conlaw_script.md")
    parser.add_argument("--out", required=True)
    parser.add_argument("--execute-codex", action="store_true")
    parser.add_argument("--execute-lm-studio", action="store_true")
    parser.add_argument("--lm-studio-base-url", default=os.environ.get("LM_STUDIO_BASE_URL", "http://127.0.0.1:5962"))
    parser.add_argument("--model", default=os.environ.get("LM_STUDIO_MODEL"))
    parser.add_argument("--max-tokens", type=int, default=int(os.environ.get("LM_STUDIO_MAX_TOKENS", "4096")))
    parser.add_argument("--timeout-sec", type=int, default=600)
    args = parser.parse_args()
    if args.execute_codex and args.execute_lm_studio:
        parser.error("choose only one execution backend")

    prompt = build_prompt(args.questions, args.pack, args.tiny_anchors, args.script)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.execute_codex:
        result = subprocess.run(["codex", "exec", "-C", str(Path.cwd()), prompt], text=True, capture_output=True, check=False)
        out.write_text(result.stdout, encoding="utf-8")
        return result.returncode
    if args.execute_lm_studio:
        content, model = run_lm_studio(prompt, args.lm_studio_base_url, args.model, args.max_tokens, args.timeout_sec)
        out.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"wrote LM Studio output: {out} ({model})")
        return 0
    out.write_text(prompt, encoding="utf-8")
    print(f"wrote prompt: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

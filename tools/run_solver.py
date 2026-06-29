from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


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


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--pack", default="study/mechanics_pack.yaml")
    parser.add_argument("--tiny-anchors", default="study/tiny_anchors.yaml")
    parser.add_argument("--script", default="study/exam_day_scripts/conlaw_script.md")
    parser.add_argument("--out", required=True)
    parser.add_argument("--execute-codex", action="store_true")
    args = parser.parse_args()
    prompt = build_prompt(args.questions, args.pack, args.tiny_anchors, args.script)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.execute_codex:
        result = subprocess.run(["codex", "exec", "-C", str(Path.cwd()), prompt], text=True, capture_output=True, check=False)
        out.write_text(result.stdout, encoding="utf-8")
        return result.returncode
    out.write_text(prompt, encoding="utf-8")
    print(f"wrote prompt: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


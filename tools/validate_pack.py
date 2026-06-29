from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arl.pack import validate_pack_file


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pack")
    args = parser.parse_args()
    pack = validate_pack_file(args.pack)
    print(f"valid pack: {len(pack.cards)} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


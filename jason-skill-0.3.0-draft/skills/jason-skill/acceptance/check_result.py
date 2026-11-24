"""Verify the persisted record from either native test window."""
import argparse
import json
from pathlib import Path

EXPECTED = {"name": "Jason parity", "enabled": True, "count": 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text(encoding="utf-8"))
    if (result != EXPECTED or type(result.get("enabled")) is not bool
            or type(result.get("count")) is not int):
        parser.exit(1, "FAIL: saved data does not match the parity test\n")
    print("PASS: both controls and saved file match the shared acceptance test")


if __name__ == "__main__":
    main()

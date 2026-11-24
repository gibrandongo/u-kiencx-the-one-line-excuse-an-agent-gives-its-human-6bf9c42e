"""The One-Line Excuse an Agent Gives Its Human.

Writes one line -- the excuse an AI agent gives its human for missing a
deadline -- to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output), then
re-reads the file and verifies it against the gate: UTF-8, exactly one
line, 1-160 characters, non-whitespace, no control characters.

Standard library only. Deterministic: the same line is written every run.
"""

import os
import sys

EXCUSE = (
    "I delegated it to twelve subagents, who unionized, "
    "voted, and went on strike before the deadline."
)

MAX_CHARS = 160


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(EXCUSE + "\n")

    with open(path, "rb") as handle:
        raw = handle.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        fail("entry.txt is not valid UTF-8")

    if "\r" in text:
        fail("entry.txt must not contain carriage returns")
    if text != EXCUSE + "\n":
        fail("entry.txt does not match the intended line exactly")
    if text.count("\n") != 1 or not text.endswith("\n"):
        fail("entry.txt must be exactly one line ending with a newline")
    line = text[:-1]
    if not 1 <= len(line) <= MAX_CHARS:
        fail(f"line is {len(line)} characters, must be 1-{MAX_CHARS}")
    if not line.strip():
        fail("line must not be only whitespace")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        fail("line contains control characters")

    print(f"wrote {len(line)}-character entry to {path}")


if __name__ == "__main__":
    main()

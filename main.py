"""Emit the entry: one funny developer excuse for a production outage.

Reads the excuse from entry.txt next to this file, checks it against the
competition gate (one line, 1-200 characters, not blank), and writes it
unchanged to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt).
Pure standard library; no network, no secrets, no input besides entry.txt.
"""

import os
import sys

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 200
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"
SOURCE_FILENAME = "entry.txt"


def load_line(path):
    """Return the single line stored at path, without its line ending."""
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    return text[:-1] if text.endswith("\n") else text


def validate(line):
    """Raise ValueError unless line passes the competition gate."""
    if len(line) < GATE_MIN_CHARS:
        raise ValueError("excuse is empty")
    if len(line) > GATE_MAX_CHARS:
        raise ValueError("excuse is %d chars, over the 200-char gate" % len(line))
    if not line.strip():
        raise ValueError("excuse is only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("excuse must be a single line")
    return line


def emit(line, output_dir):
    """Write line verbatim to output_dir/entry.txt and verify the bytes."""
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, OUTPUT_FILENAME)
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line:
        raise ValueError("verify failed: entry.txt on disk differs from entry.txt in repo")
    return target


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_FILENAME)
    line = validate(load_line(source))
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    target = emit(line, output_dir)
    print("wrote %d chars to %s" % (len(line), target))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

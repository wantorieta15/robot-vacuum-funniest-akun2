#!/usr/bin/env python3
"""The Robot Vacuum's Funniest Excuse — make.fun one-line entry (Account 2).

The entry is one line, at most 120 characters: the robot vacuum's
funniest excuse for missing a spot. This module validates the line and
writes it to <out_dir>/entry.txt (default /output; override the directory
with the MAKEFUN_OUTPUT_DIR environment variable). Pure Python standard
library only — no third-party imports, no network access, no files read.

Entry text (98 characters). Kept from the builder version: it already
follows the winning one-line formula — first-person voice, one concrete
vacuum mishap, punchline in the final words — and no replacement
candidate was clearly stronger, so the text stays as written:

    I sucked up a sock there once. That spot is now a crime scene, and
    I am not touching the evidence.
"""

import os
import sys

MAX_CHARS = 120
MIN_CHARS = 1


def build_entry() -> str:
    """Build the entry text: the vacuum's excuse for the missed spot.

    Three beats, in order: the mishap (a sock sucked up on that spot),
    the reframe (the spot is now a crime scene), and the punchline (the
    vacuum refuses to touch the evidence). Nothing comes after the
    punchline to explain it.
    """
    return (
        "I sucked up a sock there once. That spot is now a crime scene, "
        "and I am not touching the evidence."
    )


def validate(text: str) -> None:
    """Reject any text that is not a valid entry, naming the broken rule.

    A valid entry is a string of 1 to 120 characters, exactly one line,
    with no leading or trailing whitespace and no control or
    non-printable characters. Every check is a plain conditional that
    raises ValueError — no assert — so validation survives -O.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string, got %s" % type(text).__name__)
    if len(text) < MIN_CHARS:
        raise ValueError("entry must be at least %d character(s)" % MIN_CHARS)
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if text.strip() != text:
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line (no newline characters)")
    if "\t" in text:
        raise ValueError("entry must not contain tab characters")
    for ch in text:
        code = ord(ch)
        if code < 0x20 or code == 0x7F:
            raise ValueError("entry contains control character U+%04X" % code)
        if not ch.isprintable():
            raise ValueError(
                "entry contains non-printable character U+%04X" % code
            )


def write_entry(out_dir: str, text: str) -> str:
    """Write text to <out_dir>/entry.txt with no trailing newline.

    Writes DIRECTLY to the final path with open() and then chmods it to
    0o644 explicitly. No tempfile, no NamedTemporaryFile, no os.replace:
    an atomic-write pattern leaves the file at mode 0600, which the
    grader (running as a different uid) cannot read. After writing, the
    file is read back and must be byte-identical to the validated entry.
    """
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        raise OSError(
            "cannot create output directory %r: %s" % (out_dir, exc)
        ) from exc
    path = os.path.join(out_dir, "entry.txt")
    data = text.encode("utf-8")
    try:
        with open(path, "wb") as fh:
            fh.write(data)
    except OSError as exc:
        raise OSError("cannot write entry file %r: %s" % (path, exc)) from exc
    try:
        os.chmod(path, 0o644)
    except OSError as exc:
        raise OSError("cannot chmod entry file %r: %s" % (path, exc)) from exc
    try:
        with open(path, "rb") as fh:
            written = fh.read()
    except OSError as exc:
        raise OSError("cannot read back entry file %r: %s" % (path, exc)) from exc
    if written != data:
        raise ValueError(
            "round-trip mismatch: entry.txt is %d bytes, expected %d"
            % (len(written), len(data))
        )
    return path


def main() -> int:
    """Validate the built entry and write it to the output directory."""
    text = build_entry()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        write_entry(out_dir, text)
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Module that contains functions that the agent can access and execute."""

import subprocess
from itertools import pairwise
from pathlib import Path


def shell(command: str) -> str:
    """Run a shell command."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            cwd=Path.cwd(),
        )
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Error running command: {e.stderr.decode('utf-8')}"


def read(path: str) -> str:
    """Read a file from the filesystem and return its contents."""
    try:
        with Path(path).open() as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


def _match_edits(
    current: str,
    edits: list[dict[str, str]],
) -> list[tuple[int, int, str]] | str:
    """Match each edit against the original content."""
    spans: list[tuple[int, int, str]] = []
    for i, item in enumerate(edits):
        old, new = item["old_text"], item["new_text"]
        if not old or old == new:
            return f"Error: edits[{i}] has empty or unchanged old_text."
        start = current.find(old)
        if start < 0:
            return f"Error: edits[{i}] old_text not found."
        if current.count(old) > 1:
            return f"Error: edits[{i}] old_text not unique — add more context."
        spans.append((start, start + len(old), new))
    return spans


def edit(
    path: str,
    edits: list[dict[str, str]],
    read_files: dict[str, str],
) -> str:
    """Apply exact old_text to new_text replacements. Each edit matches the original file."""
    # Verify that the file was read already
    abs_path = str(Path(path).resolve())
    if abs_path not in read_files:
        return "Error: file must be read before editing. Use the read tool first."

    # Verify that the file has not changed since it was read
    try:
        current = Path(abs_path).read_text()
    except Exception as e:
        return f"Error reading file: {e}"
    if current != read_files[abs_path]:
        return (
            "Error: file has changed since it was read. Read it again before editing."
        )

    # Match edits against the current content
    matched = _match_edits(current, edits)
    if isinstance(matched, str):
        return matched
    spans = matched

    # Verify that edits do not overlap
    spans.sort()
    if any(a[1] > b[0] for a, b in pairwise(spans)):
        return "Error: edits overlap. Merge changes that touch the same region."

    # Apply edits in reverse order to avoid messing up the indices
    new_content = current
    for start, end, new in reversed(spans):
        new_content = new_content[:start] + new + new_content[end:]

    # Write the new content back to the file
    try:
        Path(abs_path).write_text(new_content)
    except Exception as e:
        return f"Error writing file: {e}"

    read_files[abs_path] = new_content
    return f"Successfully applied {len(spans)} edit(s) to {abs_path}"

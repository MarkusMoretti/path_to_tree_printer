"""Render a list of file paths as an ASCII tree.

We split on `/` only. That decision is documented in the README.
"""

from __future__ import annotations


def _build_tree(paths):
    """Build a nested dict of {segment: child-dict-or-None}.

    A leaf node maps to an empty dict so that files and directories look
    identical in the output. The caller cannot tell a file from a directory
    from a path string alone (`a/b` could be a file `b` in dir `a`, or dir
    `b` in dir `a`), so we don't try.
    """
    root = {}
    for path in paths:
        if path == "":
            continue
        parts = path.split("/")
        node = root
        for part in parts:
            if part == "":
                # Trailing slash or empty segment from `//`. Skip it; the
                # parent directory is still recorded as a node.
                continue
            node = node.setdefault(part, {})
    return root


def _render(node, prefix):
    """Render a tree node to a list of lines.

    `prefix` is the string to prepend to every entry at this level, *without*
    the branch character — we add that here because whether it's the last item
    in the parent affects which character to draw.
    """
    lines = []
    # Sort deterministically by segment name. Case-sensitive sort: `Foo`
    # sorts before `bar`. This is a deliberate choice (see README).
    items = sorted(node.items(), key=lambda kv: kv[0])
    total = len(items)
    for i, (segment, children) in enumerate(items):
        is_last = i == total - 1
        branch = "└── " if is_last else "├── "
        lines.append(f"{prefix}{branch}{segment}")
        child_prefix = prefix + ("    " if is_last else "│   ")
        lines.extend(_render(children, child_prefix))
    return lines


def render_tree(paths):
    """Render a list of path strings as an ASCII tree.

    Args:
        paths: Iterable of path strings using `/` as the separator.

    Returns:
        A single string with lines joined by ``\n``. No trailing newline.
        Returns an empty string if no paths are provided.

    Each segment of each path becomes a node. Empty strings and empty
    segments (from trailing slashes or `//`) are skipped, not rendered as
    blank nodes. Children are sorted alphabetically (case-sensitive).
    """
    root = _build_tree(paths)
    lines = _render(root, "")
    return "\n".join(lines)

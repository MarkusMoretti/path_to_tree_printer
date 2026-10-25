# path_to_tree_printer

Takes a list of `/`-separated path strings and renders them as an ASCII tree, indented by directory hierarchy.

## Usage

```python
from path_to_tree_printer import render_tree

print(render_tree(["src/app/main.py", "src/app/util.py", "README.md"]))
```

Output:

```
├── README.md
└── src
    └── app
        ├── main.py
        └── util.py
```

## Why

Useful for summarising the layout of a set of files (a build manifest, a diff, a list of assets) in a terminal-readable form. The trade-off: we only split on `/`, so Windows-style backslash paths won't work without normalising them first. We also sort children alphabetically (case-sensitive), so `Zebra` sorts before `apple` — predictable, but not always what a human expects.

## Edges

- Trailing slashes (`a/b/`) and double slashes (`a//b`) are collapsed: empty segments are skipped, not rendered as blank nodes.
- A path string can't tell a file from a directory, so we render every segment identically.
- Empty strings and empty input produce empty output.
- Duplicate paths are merged into a single node.

## API

- `render_tree(paths)` — `paths` is an iterable of path strings. Returns a string with lines joined by `\n`, no trailing newline.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.


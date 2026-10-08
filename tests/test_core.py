import unittest

from path_to_tree_printer import render_tree


class TestRenderTree(unittest.TestCase):

    def test_empty_input(self):
        self.assertEqual(render_tree([]), "")

    def test_single_path(self):
        self.assertEqual(render_tree(["a"]), "└── a")

    def test_multiple_top_level(self):
        result = render_tree(["a", "b"])
        self.assertEqual(result, "├── a\n└── b")

    def test_nested_single(self):
        result = render_tree(["a/b/c"])
        self.assertEqual(result, "└── a\n    └── b\n        └── c")

    def test_shared_prefix(self):
        result = render_tree(["a/b", "a/c"])
        self.assertEqual(result, "└── a\n    ├── b\n    └── c")

    def test_branch_and_leaf_mixed(self):
        result = render_tree(["a/b", "c"])
        self.assertEqual(result, "├── a\n│   └── b\n└── c")

    def test_trailing_slash_skipped(self):
        result = render_tree(["a/b/"])
        self.assertEqual(result, "└── a\n    └── b")

    def test_double_slash_skipped(self):
        result = render_tree(["a//b"])
        self.assertEqual(result, "└── a\n    └── b")

    def test_empty_string_path_skipped(self):
        self.assertEqual(render_tree([""]), "")

    def test_children_sorted_alphabetically_case_sensitive(self):
        result = render_tree(["a/z", "a/B", "a/m"])
        self.assertEqual(
            result,
            "└── a\n    ├── B\n    ├── m\n    └── z",
        )

    def test_deduplicates_identical_paths(self):
        result = render_tree(["a/b", "a/b"])
        self.assertEqual(result, "└── a\n    └── b")

    def test_deeply_nested(self):
        result = render_tree(["a/b/c/d"])
        self.assertEqual(
            result,
            "└── a\n    └── b\n        └── c\n            └── d",
        )


if __name__ == "__main__":
    unittest.main()

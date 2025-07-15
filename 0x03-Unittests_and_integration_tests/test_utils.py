#!/usr/bin/env python3
"""Unit tests for access_nested_map function from utils module."""
from utils import access_nested_map
from parameterized import parameterized
import unittest


class TestAccessNestedMap(unittest.TestCase):
    """Test case for access_nested_map function from utils module."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: dict,
        path: tuple,
        expected: object
    ) -> None:
        """
        Test that access_nested_map returns expected result for the given path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()

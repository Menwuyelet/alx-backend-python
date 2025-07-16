#!/usr/bin/env python3
"""Unit tests for access_nested_map function from utils module."""
from utils import access_nested_map, get_json
from parameterized import parameterized
import unittest
from unittest import mock


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

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: dict,
        path: tuple,
        expected: object
    ) -> None:
        """
        Test that access_nested_map raises "KeyError" for the unavailable paths
        """
        self.assertRaises(expected, access_nested_map, nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test case for get_json function from utils module."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        url: str,
        expected: dict
    ) -> None:
        """
        Test that get_json method returns expected result for the given urls
        with out calling the actual http calls.
        """
        with mock.patch('utils.requests.get') as mocked:
            mock_response = mock.Mock()
            mock_response.json.return_value = expected
            mocked.return_value = mock_response

            result = get_json(url)
            mocked.assert_called_once_with(url)
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

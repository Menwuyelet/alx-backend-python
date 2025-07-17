#!/usr/bin/env python3
"""Unit tests for
access_nested_map,
get_json,
and memoize functions from utils module.
"""
from utils import access_nested_map, get_json, memoize
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
        expected: int
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
        expected: int
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
        without calling the actual http calls.
        """
        with mock.patch('utils.requests.get') as mocked:
            mock_response = mock.Mock()
            mock_response.json.return_value = expected
            mocked.return_value = mock_response

            result = get_json(url)
            mocked.assert_called_once_with(url)
            self.assertEqual(result, expected)


class TestMemoize(unittest.TestCase):
    """Test case for memoize function from utils module."""
    def test_memoize(self):
        """
        Test that memoize method returns expected result by calling
        the a_method only once.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with mock.patch.object(
            TestClass,
            'a_method',
            return_value=42
        ) as mock_method:
            instance = TestClass()

            result1 = instance.a_property
            result2 = instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()

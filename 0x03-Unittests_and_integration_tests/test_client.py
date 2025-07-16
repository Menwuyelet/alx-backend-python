#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest import mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @mock.patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""

        expected_payload = {"login": org_name, "id": 1234}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        ORG_URL = "https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(
            ORG_URL.format(org_name=org_name)
        )

        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()

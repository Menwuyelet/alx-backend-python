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
    def test_org(self, org_name: str, mock_get_json):
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

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org"""

        mock_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        with mock.patch.object(
            GithubOrgClient,
            'org',
            new_callable=mock.PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_payload
            client = GithubOrgClient("testorg")

            self.assertEqual(
                client._public_repos_url,
                mock_payload["repos_url"]
            )
            mock_org.assert_called_once()

    @mock.patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method"""

        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_repos_payload

        with mock.patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=mock.PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )
            mock_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()

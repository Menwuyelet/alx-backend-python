#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from parameterized import parameterized_class
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
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

        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_payload
            client = GithubOrgClient("testorg")

            self.assertEqual(
                client._public_repos_url,
                mock_payload["repos_url"]
            )
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Tests the public_repos method by mocking client.get_json method"""

        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Tests the has_license static method with various inputs by using
        the above parameterized inputs.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org,
        "repos_payload": repos,
        "expected_repos": expected,
        "apache2_repos": apache2
    }
    for org, repos, expected, apache2 in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class using real fixture payload to test public_repos
    """

    @classmethod
    def setUpClass(cls):
        """Starts patching requests.get"""
        cls.get_patcher = patch("requests.get")
        mocked_get = cls.get_patcher.start()

        # Side effect to mock requests.get().json()
        def side_effect(url):
            mock_resp = MagicMock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        mocked_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stops patching"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Tests the GithubOrgClient.public_repos returns expected repo names
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Tests the GithubOrgClient.public_repos filters by 'apache-2.0' license
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(
                license="apache-2.0"
            ),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()

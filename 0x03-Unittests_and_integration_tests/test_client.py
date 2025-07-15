#!/usr/bin/env python3
"""Test for the github org client
"""

import unittest

from client import GithubOrgClient

from unittest.mock import patch, PropertyMock

from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        method should test that GithubOrgClient.org returns the correct value.
        :param org_name: string of the organization
        :param mock_get: mock of the get_json localized in the client module
        :return:
        """
        github = GithubOrgClient(org_name)
        github.org
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        method to unit-test GithubOrgClient._public_repos_url.
        :return:
        """
        expected_url = "https://api.github.com/orgs/a_repo"
        with patch.object(
                GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            github = GithubOrgClient("a_repo")
            self.assertEqual(github._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Method to unit-test GithubOrgClient.public_repos
        :param mock_get_json: patch of get_json() method
        :return:
        """
        expected_payload = [
            {"name": "alx_backend_python", "license": {"key": "MIT"}},
            {"name": "alx_travel_app"},
            {"name": "alx_airbnb_database", "license": {"key": "ISC"}}
        ]
        mock_get_json.return_value = expected_payload
        with patch.object(
                GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_public_repos_url:
            expected_url = "https://api.github.com/orgs/alx"
            mock_public_repos_url.return_value = expected_url
            github = GithubOrgClient('alx')
            result = github.public_repos()
            self.assertEqual(
                result,
                ["alx_backend_python", "alx_travel_app", "alx_airbnb_database"]
            )
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

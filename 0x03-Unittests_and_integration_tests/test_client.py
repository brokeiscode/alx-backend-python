#!/usr/bin/env python3
"""Test for the github org client
"""

import unittest

from client import GithubOrgClient

from unittest.mock import patch, PropertyMock, Mock

from parameterized import parameterized, parameterized_class

from fixtures import TEST_PAYLOAD


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
        expected_url = "https://api.github.com/orgs/alx/repos"
        with patch.object(
                GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            github = GithubOrgClient("alx")
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
            expected_url = "https://api.github.com/orgs/alx/repos"
            mock_public_repos_url.return_value = expected_url
            github = GithubOrgClient('alx')
            result = github.public_repos()
            self.assertEqual(
                result,
                ["alx_backend_python", "alx_travel_app", "alx_airbnb_database"]
            )
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Method to unit-test GithubOrgClient.has_license.
        :param repo: repo dict
        :param license_key: license key str
        :param expected: expected return value
        :return:
        """
        github = GithubOrgClient('alx')
        result = github.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": payload[0],
        "repos_payload": payload[1],
        "expected_repos": payload[2],
        "apache2_repos": payload[3]
    } for payload in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos.
    Mocks external HTTP requests.
    """

    @classmethod
    def setUpClass(cls):
        """
        Sets up the class by mocking requests.get.
        Use patch to start a patcher named get_patcher
        """

        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """
            Function will return different Mock objects based on the URL
            :param url:
            :return:
            """
            mock_response = Mock()
            if url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = cls.org_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stops the patcher after all tests in the class have run.
        """

        cls.get_patcher.stop()

#!/usr/bin/env python3
"""Test for the github org client
"""

import unittest

from client import GithubOrgClient

from unittest.mock import patch

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

#!/usr/bin/env python3
"""Testing the classes in the Utils modules
"""

import unittest

from parameterized import parameterized

from utils import access_nested_map, get_json

from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """TestCase for the Function access_nested_map
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test nested_map with the keys in path provided
        :param nested_map: a nested dictionary.
        :param path: tuple of the nested keys.
        :param expected: the expected result values.
        :return:
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Using Assert to raise and exception for the accesss_nested_map
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """TestCase for GET Json from url
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_requests):
        """
        Using Mock and Patch to simulate a GET request and response
        :param test_url: mock url to GET
        :param test_payload: mock json response for the GET
        :param mock_requests: mock object for request.get
        :return:
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_requests.return_value = mock_response

        tested_get = get_json(test_url)
        mock_requests.assert_called_once_with(test_url)
        self.assertEqual(tested_get, test_payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)

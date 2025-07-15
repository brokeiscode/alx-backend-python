#!/usr/bin/env python3
"""Testing the classes in the Utils modules
"""

import unittest

from parameterized import parameterized

from utils import access_nested_map


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

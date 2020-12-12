from unittest import TestCase

from iubeo import ConfigError, boolean, comma_separated_list
from iubeo.utils import raise_config_error_instead


class IubeoCastersTestCase(TestCase):
    comma_separated_list_tests = [
        "a,b,c",
        "a,,b,,c",
        ",a,b,c",
        ",a,b,c,",
    ]

    comma_separated_list_test_results = [
        ["a", "b", "c"],
        ["a", "", "b", "", "c"],
        ["", "a", "b", "c"],
        ["", "a", "b", "c", ""],
    ]

    boolean_tests = [
        "False",
        "false",
        "0",
        "True",
        "true",
        "1",
    ]

    boolean_test_results = [
        False,
        False,
        False,
        True,
        True,
        True,
    ]

    def test_raise_config_instead(self):
        @raise_config_error_instead
        def faulty_function(value):
            raise Exception("test_raise_config_instead")

        with self.assertRaises(ConfigError):
            faulty_function(None)

    def test_comma_separated_list(self):
        for _in, _out in zip(self.comma_separated_list_tests, self.comma_separated_list_test_results):
            self.assertEqual(comma_separated_list(_in), _out)

    def test_boolean(self):
        for _in, _out in zip(self.boolean_tests, self.boolean_test_results):
            self.assertEqual(boolean(_in), _out)

        with self.assertRaises(ConfigError):
            boolean("incorrect")

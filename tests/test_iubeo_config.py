import os
from unittest import TestCase

from iubeo import ConfigError, boolean, caster, comma_separated_int_list, comma_separated_list, config, integer, string


def custom_callable(value):
    return "CUSTOM_CALLABLE"


class IubeoConfigTestCase(TestCase):
    test_1 = {
        "N0": custom_callable,
        "N1": {
            "N10": str,
            "N11": {
                "N110": int,
            },
        },
        "N2": {
            "N20": {
                "N201": {
                    "N2010": float,
                }
            },
            "N21": {
                "N210": str,
            },
        },
        "N3": comma_separated_list(),
        "N4": comma_separated_list(missing_default=["1", "2", "3"]),
        "N5": boolean(error_default=True),
        "N6": comma_separated_int_list(missing_default=[1, 2, 3]),
    }

    def setupTest1(self, prefix=None, sep=None):
        prefix = prefix or ""
        sep = sep or "__"
        expected_variables = {
            sep.join([i for i in [prefix, "N0"] if i]): custom_callable(None),
            sep.join([i for i in [prefix, "N1", "N10"] if i]): "Test1",
            sep.join([i for i in [prefix, "N1", "N11", "N110"] if i]): "1",
            sep.join([i for i in [prefix, "N2", "N20", "N201", "N2010"] if i]): "0.1",
            sep.join([i for i in [prefix, "N2", "N21", "N210"] if i]): "Test2",
            sep.join([i for i in [prefix, "N3"] if i]): "1,2,3",
            sep.join([i for i in [prefix, "N5"] if i]): "no",
        }
        for key, value in expected_variables.items():
            os.environ.setdefault(key, value)

        def teardown():
            for k in expected_variables.keys():
                os.environ.pop(k)

        return teardown

    def setUp(self):
        self.test_key = "KEY"

    def tearDown(self):
        os.environ.pop(self.test_key, None)

    def assertTest1(self, test_config):
        assert test_config.N0 == "CUSTOM_CALLABLE"
        assert test_config.N1.N10 == "Test1"
        assert test_config.N1.N11.N110 == 1
        assert test_config.N2.N20.N201.N2010 == 0.1
        assert test_config.N2.N21.N210 == "Test2"
        assert test_config.N3 == ["1", "2", "3"]
        assert test_config.N4 == ["1", "2", "3"]
        assert test_config.N5 == True
        assert test_config.N6 == [1, 2, 3]

    def test_config_created_successfully(self):
        teardown = self.setupTest1()
        test_config = config(self.test_1)

        self.assertTest1(test_config)
        teardown()

    def test_config_separator(self):
        teardown = self.setupTest1(sep=".")
        test_config = config(self.test_1, sep=".")

        self.assertTest1(test_config)
        teardown()

    def test_config_prefix(self):
        teardown = self.setupTest1(prefix="PREFIX")
        test_config = config(self.test_1, prefix="PREFIX")

        self.assertTest1(test_config)
        teardown()

    def test_config_prefix_and_separator(self):
        teardown = self.setupTest1(prefix="PREFIX", sep=".")
        test_config = config(self.test_1, prefix="PREFIX", sep=".")

        self.assertTest1(test_config)
        teardown()

    def test_caster__boolean__success(self):
        os.environ.setdefault(self.test_key, "True")
        test_config = config({self.test_key: boolean()})
        assert test_config.KEY == True

    def test_caster__boolean__cant_parse(self):
        os.environ.setdefault(self.test_key, "no")
        with self.assertRaises(ConfigError):
            config({self.test_key: boolean()})
        test_config = config({self.test_key: boolean(error_default=True)})
        assert test_config.KEY == True

    def test_caster__boolean__missing(self):
        with self.assertRaises(ConfigError):
            config({self.test_key: boolean()})
        test_config = config({self.test_key: boolean(missing_default=True)})
        assert test_config.KEY == True

    def test_caster__comma_separated_list__success(self):
        os.environ.setdefault(self.test_key, "1,2,3")
        test_config = config({self.test_key: comma_separated_list()})
        assert test_config.KEY == ["1", "2", "3"]

    def test_caster__comma_separated_list__missing(self):
        with self.assertRaises(ConfigError):
            config({self.test_key: comma_separated_list()})
        test_config = config({self.test_key: comma_separated_list(missing_default=["1", "2", "3"])})
        assert test_config.KEY == ["1", "2", "3"]

    def test_caster__comma_separated_int_list__success(self):
        os.environ.setdefault(self.test_key, "1,2,3")
        test_config = config({self.test_key: comma_separated_int_list()})
        assert test_config.KEY == [1, 2, 3]

    def test_caster__comma_separated_int_list__cant_parse(self):
        os.environ.setdefault(self.test_key, "1,2,no")
        with self.assertRaises(ConfigError):
            config({self.test_key: comma_separated_int_list()})
        test_config = config({self.test_key: comma_separated_int_list(error_default=[1, 2, 3])})
        assert test_config.KEY == [1, 2, 3]

    def test_caster__comma_separated_int_list__missing(self):
        with self.assertRaises(ConfigError):
            config({self.test_key: comma_separated_int_list()})
        test_config = config({self.test_key: comma_separated_int_list(missing_default=[1, 2, 3])})
        assert test_config.KEY == [1, 2, 3]

    def test_caster__string__success(self):
        os.environ.setdefault(self.test_key, "Test")
        test_config = config({self.test_key: string()})
        assert test_config.KEY == "Test"

    def test_caster__string__missing(self):
        with self.assertRaises(ConfigError):
            config({self.test_key: string()})
        test_config = config({self.test_key: string(missing_default="Test")})
        assert test_config.KEY == "Test"

    def test_caster__integer__success(self):
        os.environ.setdefault(self.test_key, "1")
        test_config = config({self.test_key: integer()})
        assert test_config.KEY == 1

    def test_caster__integer__cant_parse(self):
        os.environ.setdefault(self.test_key, "no")
        with self.assertRaises(ConfigError):
            config({self.test_key: integer()})
        test_config = config({self.test_key: integer(error_default=1)})
        assert test_config.KEY == 1

    def test_caster__integer__missing(self):
        with self.assertRaises(ConfigError):
            config({self.test_key: integer()})
        test_config = config({self.test_key: integer(missing_default=1)})
        assert test_config.KEY == 1

    def test_caster__custom_callable__success(self):
        os.environ.setdefault(self.test_key, "Test")
        test_config = config({self.test_key: custom_callable})
        assert test_config.KEY == "CUSTOM_CALLABLE"

    def test_caster__custom_callable__missing(self):
        with self.assertRaises(ConfigError):
            config({self.test_key: caster(custom_callable)})
        test_config = config({self.test_key: caster(custom_callable)(missing_default="CUSTOM_CALLABLE")})
        assert test_config.KEY == "CUSTOM_CALLABLE"

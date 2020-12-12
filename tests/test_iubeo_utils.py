from unittest import TestCase

from iubeo.utils import raise_config_error_instead


@raise_config_error_instead
def custom_callable(value):
    return "CUSTOM_CALLABLE"


class IubeoUtilsTestCase(TestCase):
    def test_raises_config_error(self):
        self.assertTrue(hasattr(custom_callable, "_raises_config_error") and custom_callable._raises_config_error)

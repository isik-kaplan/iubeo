from unittest import TestCase

from iubeo import config


def custom_callable(arg):
    return "CUSTOM_CALLABLE"


class IubeoTestCase(TestCase):
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
    }

    test_1_node_types = {
        "N0": custom_callable,
        "N1__N10": str,
        "N1__N11__N110": int,
        "N2__N20__N201__N2010": float,
        "N2__N21__N210": str,
    }

    test_1_state = {
        "N0": ["N0", custom_callable],
        "N1": {
            "N10": ["N1__N00", str],
            "N11": {
                "N000": ["N1__N11__N000", int],
            },
        },
        "N2": {
            "N20": {
                "N201": {
                    "N2010": ["N2__N20__N201__N2010", float],
                }
            },
            "N21": {
                "N210": ["N2__N21__N210", str],
            },
        },
    }

    test_1_node_types_prefix = {
        "PREFIX__N0": custom_callable,
        "PREFIX__N1__N10": str,
        "PREFIX__N1__N11__N110": int,
        "PREFIX__N2__N20__N201__N2010": float,
        "PREFIX__N2__N21__N210": str,
    }

    test_1_state_prefix = {
        "N0": ["PREFIX__N0", custom_callable],
        "N1": {
            "N00": ["PREFIX__N1__N00", str],
            "N11": {
                "N000": ["PREFIX__N1__N11__N000", int],
            },
        },
        "N2": {
            "N20": {
                "N201": {
                    "N2010": ["PREFIX__N2__N20__N201__N2010", float],
                }
            },
            "N21": {
                "N210": ["PREFIX__N2__N21__N210", str],
            },
        },
    }

    test_1_node_types_sep = {
        "N0": custom_callable,
        "N1_sep_N10": str,
        "N1_sep_N11_sep_N110": int,
        "N2_sep_N20_sep_N201_sep_N2010": float,
        "N2_sep_N21_sep_N210": str,
    }

    test_1_state_sep = {
        "N0": ["N0", custom_callable],
        "N1": {
            "N00": ["N1_sep_N00", str],
            "N11": {
                "N000": ["N1_sep_N11_sep_N000", int],
            },
        },
        "N2": {
            "N20": {
                "N201": {
                    "N2010": ["N2_sep_N20_sep_N201_sep_N2010", float],
                }
            },
            "N21": {
                "N210": ["N2_sep_N21_sep_N210", str],
            },
        },
    }

    test_1_node_types_prefix_sep = {
        "PREFIX_sep_N0": custom_callable,
        "PREFIX_sep_N1_sep_N10": str,
        "PREFIX_sep_N1_sep_N11_sep_N110": int,
        "PREFIX_sep_N2_sep_N20_sep_N201_sep_N2010": float,
        "PREFIX_sep_N2_sep_N21_sep_N210": str,
    }

    test_1_state_prefix_sep = {
        "N0": ["PREFIX_sep_N0", custom_callable],
        "N1": {
            "N10": ["PREFIX_sep_N1_sep_N10", str],
            "N11": {
                "N000": ["PREFIX_sep_N1_sep_N11_sep_N000", int],
            },
        },
        "N2": {
            "N20": {
                "N201": {
                    "N2010": ["PREFIX_sep_N2_sep_N20_sep_N201_sep_N2010", float],
                }
            },
            "N21": {
                "N210": ["PREFIX_sep_N2_sep_N21_sep_N210", str],
            },
        },
    }

    def setUp(self) -> None:
        self.config = config(self.test_1)
        self.config_prefix = config(self.test_1, prefix="PREFIX")
        self.config_sep = config(self.test_1, sep="_sep_")
        self.config_prefix_sep = config(self.test_1, prefix="PREFIX", sep="_sep_")

    def test_creates_correct_node_names(self):
        self.assertEqual([*self.test_1_node_types.keys()], self.config.final_nodes)

    def test_creates_correct_node_names_with_prefix(self):
        self.assertEqual([*self.test_1_node_types_prefix.keys()], self.config_prefix.final_nodes)

    def test_create_correct_node_names_with_sep(self):
        self.assertEqual([*self.test_1_node_types_sep.keys()], self.config_sep.final_nodes)

    def test_create_correct_nodes_names_with_prefix_sep(self):
        self.assertEqual([*self.test_1_node_types_prefix_sep.keys()], self.config_prefix_sep.final_nodes)

    def test_casts_the_callable(self):
        self.assertEqual(self.config.N0, "CUSTOM_CALLABLE")

    def test_correctly_casts_the_values(self):
        self.assertEqual(self.config.N0, "CUSTOM_CALLABLE")

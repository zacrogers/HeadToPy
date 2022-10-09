import unittest
import logging

import head_to_py.head_to_py as h2p

logger = logging.getLogger()


class TestHeadToPy(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_pythonize_enum_name(self):
        c_enum_name = "enum_name_e"
        py_enum_name = "class EnumName(Enum):\n"

        self.assertEqual(py_enum_name, h2p._pythonize_enum_name(c_enum_name))

        c_enum_name = "enum_name"

        self.assertEqual(py_enum_name, h2p._pythonize_enum_name(c_enum_name))


    def test_remove_enum_val_type(self):
        vals = [f"({t})0x{i:02x}" for i, t in enumerate(h2p.VALID_C_INT)]

        for i, v in enumerate(vals):
            self.assertEqual(h2p._remove_enum_val_type(v), f"0x{i:02x}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-7.7s - %(funcName)10s()]  %(message)s",
        handlers=[logging.StreamHandler()]
    )

    unittest.main()
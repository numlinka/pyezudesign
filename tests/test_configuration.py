# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

# std
import os
import unittest

# tests
from ezudesign.configuration import *


class TestUtils (unittest.TestCase):
    def test_new_and_get(self):
        config = Configuration()
        config.ctrl.new("int_1", int)
        config.ctrl.new("int_2", int, 10086)
        config.ctrl.new("float_1", float)
        config.ctrl.new("float_2", float, 3.1415926)
        config.ctrl.new("str_1", str)
        config.ctrl.new("str_2", str, "default")

        self.assertEqual(config.ctrl.get("int_1"), 0)
        self.assertEqual(config.ctrl.get("int_2"), 10086)
        self.assertEqual(config.ctrl.get("float_1"), 0.0)
        self.assertEqual(config.ctrl.get("float_2"), 3.1415926)
        self.assertEqual(config.ctrl.get("str_1"), "")
        self.assertEqual(config.ctrl.get("str_2"), "default")

    def test_set_and_get(self):
        config = Configuration()

        config.ctrl.new("int", int)
        config.ctrl.new("float", float)
        config.ctrl.new("str", str)
        self.assertEqual(config.ctrl.get("int"), 0)
        self.assertEqual(config.ctrl.get("float"), 0.0)
        self.assertEqual(config.ctrl.get("str"), "")

        config.ctrl.set("int", 10086)
        self.assertEqual(config.ctrl.get("int"), 10086)

        config.ctrl.set("float", 3.1415926)
        self.assertEqual(config.ctrl.get("float"), 3.1415926)

        config.ctrl.set("str", "default")
        self.assertEqual(config.ctrl.get("str"), "default")

    def test_ranges(self):
        config = Configuration()
        config.ctrl.new("int_1", int, 1, range(1, 5))
        config.ctrl.new("int_2", int, 1, NumericalRange(1, 5))

        config.ctrl.set("int_1", 3)
        config.ctrl.set("int_2", 3)
        self.assertRaises(ConfigValueOutOfRange, config.ctrl.set, "int_1", 5)
        self.assertRaises(ConfigValueOutOfRange, config.ctrl.set, "int_2", 6)

    def test_get_ranges(self):
        config = Configuration()
        config.ctrl.new("int_1", int, 1, range(1, 5))
        config.ctrl.new("int_2", int, 1)
        config.ctrl.set_ranges("int_2", NumericalRange(1, 5))

        self.assertEqual(list(config.ctrl.get_ranges("int_1")), list(range(1, 5)))
        self.assertEqual(config.ctrl.get_ranges("int_2").min, 1)
        self.assertEqual(config.ctrl.get_ranges("int_2").max, 5)

    def test_overload(self):
        config = Configuration()
        config.ctrl.new("vint", int)
        self.assertEqual(config.vint, 0)
        config.vint = 10086
        self.assertEqual(config.vint, 10086)
        config.vint -= 10000
        self.assertEqual(config.vint, 86)
        self.assertEqual(config.vint.value, 86)
        self.assertIsNone(config.vint.ranges)
        config.ctrl.set_ranges("vint", NumericalRange(1, 100))
        self.assertEqual(config.vint.ranges.min, 1)
        self.assertEqual(config.vint.ranges.max, 100)

    def test_reinvention(self):
        class TestConfiguration (Configuration):
            vint = setting(int)
            vfloat = setting(float)
            vstr = setting(str)

        config = TestConfiguration()

        self.assertEqual(config.vint, 0)
        self.assertEqual(config.vfloat, 0.0)
        self.assertEqual(config.vstr, "")

    def test_save_and_load(self):
        config = Configuration()
        config.ctrl.new("vint", int)
        config.ctrl.new("vfloat", float)
        config.ctrl.new("vstr", str)

        config.vint = 10086
        config.vfloat = 3.1415926
        config.vstr = "default"

        self.assertEqual(config.vint, 10086)
        self.assertEqual(config.vfloat, 3.1415926)
        self.assertEqual(config.vstr, "default")

        config.ctrl.save_json("test-config-file")

        config.vint = 0
        config.vfloat = 0.0
        config.vstr = ""

        self.assertEqual(config.vint, 0)
        self.assertEqual(config.vfloat, 0.0)
        self.assertEqual(config.vstr, "")

        config.ctrl.load_json("test-config-file")

        self.assertEqual(config.vint, 10086)
        self.assertEqual(config.vfloat, 3.1415926)
        self.assertEqual(config.vstr, "default")

        os.remove("test-config-file")

    def test_save_and_load_base64(self):
        config = Configuration()
        config.ctrl.new("vint", int)
        config.ctrl.new("vfloat", float)
        config.ctrl.new("vstr", str)

        config.vint = 10086
        config.vfloat = 3.1415926
        config.vstr = "default"

        self.assertEqual(config.vint, 10086)
        self.assertEqual(config.vfloat, 3.1415926)
        self.assertEqual(config.vstr, "default")

        config.ctrl.save_json("test-config-file", base64=True)

        config.vint = 0
        config.vfloat = 0.0
        config.vstr = ""

        self.assertEqual(config.vint, 0)
        self.assertEqual(config.vfloat, 0.0)
        self.assertEqual(config.vstr, "")

        config.ctrl.load_json("test-config-file", base64=True)

        self.assertEqual(config.vint, 10086)
        self.assertEqual(config.vfloat, 3.1415926)
        self.assertEqual(config.vstr, "default")

        os.remove("test-config-file")

    def test_load_and_srt_invalid_item(self):
        config = Configuration()
        config.ctrl.load_dict({"vint": 0, "vfloat": 3.1415926})
        config.vint = 10086

        self.assertEqual(config.vint, 10086)
        self.assertEqual(config.vfloat, 3.1415926)

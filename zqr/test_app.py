from zqr.app import Template
from zqr.app import OffsetType
import unittest


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')


class TestTemplate(unittest.TestCase):

    def test_load_values(self):
        background_src = "background_src.png"
        ro_w = 10
        ro_h = 20
        # Importing OffsetType.Center is failing for some reason, possible the way I am running it.
        offset_type = 1  # OffsetType.Center

        template = Template.load_from_json(
            {"background_src": background_src, "raw_offset_width": ro_w, "raw_offset_height": ro_h, "offset_type": int(offset_type)})

        self.assertEqual(template.background_src, background_src)
        self.assertEqual(template.raw_offset, (ro_w, ro_h))
        #self.assertEqual(OffsetType(template.offset_type), offset_type)
        self.assertEqual(int(template.offset_type), offset_type)


if __name__ == '__main__':
    unittest.main()

from zqr.app import OffsetType
from zqr.app import Template
from zqr.app import TemplateController
import unittest
import mock
import random

TEST_TEMPLATE_DICT_1 = {"background_src": "background_src_1.png",
                          "raw_offset_width": 10,
                          "raw_offset_height": 11,
                          "offset_type": OffsetType.TOP_LEFT}
TEST_TEMPLATE_DICT_2 = {"background_src": "background_src_2.png",
                          "raw_offset_width": 20,
                          "raw_offset_height": 21,
                          "offset_type": OffsetType.TOP_LEFT}
TEST_TEMPLATE_DICT_DEFAULT = {"background_src": "",
                          "raw_offset_width": 0,
                          "raw_offset_height": 0,
                          "offset_type": OffsetType.CENTER}

class TestTemplate(unittest.TestCase):

    def test_template_load_values(self):
        template = Template.load_from_dict(TEST_TEMPLATE_DICT_1)

        self.assertEqual(template.background_src, "background_src_1.png")
        self.assertEqual(template.raw_offset, (10, 11))
        self.assertEqual(OffsetType(template.offset_type), OffsetType.TOP_LEFT)

    def test_template_load_default_values(self):
        template = Template.load_from_dict({})

        self.assertEqual(template.to_dict(), TEST_TEMPLATE_DICT_DEFAULT)

class TestTemplateController(unittest.TestCase):
    
    @mock.patch('builtins.open')
    @mock.patch('json.load')
    @mock.patch('os.path')
    def test_load_templates(self, mock_path, mock_json, mock_open):
        template_controller = TemplateController(load_templates=False)
        
        mock_open.read_data = "read_data"
        mock_path.is_file.return_value = True
        mock_json.return_value = [TEST_TEMPLATE_DICT_1, TEST_TEMPLATE_DICT_DEFAULT, TEST_TEMPLATE_DICT_2]
        
        template_controller.load_templates()
        
        self.assertEqual(len(template_controller.templates), 3)
        
    def test_get_random_template(self):
        template_controller = TemplateController(load_templates=False)
        template_controller.templates = [TEST_TEMPLATE_DICT_1, TEST_TEMPLATE_DICT_DEFAULT, TEST_TEMPLATE_DICT_2]
        
        random.seed(900)
        self.assertEqual(TEST_TEMPLATE_DICT_2,template_controller.get_random_template())
        self.assertEqual(TEST_TEMPLATE_DICT_1,template_controller.get_random_template())
        self.assertEqual(TEST_TEMPLATE_DICT_DEFAULT,template_controller.get_random_template())
        

if __name__ == '__main__':
    unittest.main()

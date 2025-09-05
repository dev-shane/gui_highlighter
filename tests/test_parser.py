import unittest
import xml.etree.ElementTree as ET
import os
from src.parser import parse_bounds, extract_leaf_bounds, get_leaf_node_bounds

"""
Unit tests for the Android UI XML parser functions (`parse_bounds`, `extract_leaf_bounds`, `get_leaf_node_bounds`).

Tests included:
- parse_bounds: normal bounds, whitespace variations, negative coordinates, zero-width/height, malformed bounds, non-numeric input.
- extract_leaf_bounds: single leaf node, nested nodes to verify correct leaf extraction.
- get_leaf_node_bounds: file not found, empty XML, malformed XML, extra/misnested tags, plain text, HTML, binary, and a valid XML file.

Rationale:
- Covers both normal operation and expected failure modes to ensure robustness for typical Android UI dumps.
- Edge cases like missing or malformed bounds, negative coordinates, and unusual whitespace are handled.

Tests left out (optional, for very large or unusual XMLs):
- Extremely deep or very large hierarchies to test recursion limits or performance.
- Highly complex overlapping or repeated leaf nodes (unlikely given the small scope of screens in this assignment).
"""
class TestParserFunctions(unittest.TestCase):

    # -------- parse_bounds tests --------
    def test_parse_bounds_normal(self):
        bounds_str = "[0,96][224,320]"
        expected = [0, 96, 224, 320]
        self.assertEqual(parse_bounds(bounds_str), expected)

    def test_whitespace_in_bounds(self):
        bounds_str = "[0,  96][224,320]\t"
        expected = [0, 96, 224, 320]
        result = parse_bounds(bounds_str)
        self.assertEqual(result, expected)

        bounds_str2 = "[ 230 ,100][400,300 ]"
        expected2 = [230, 100, 400, 300]
        result2 = parse_bounds(bounds_str2)
        self.assertEqual(result2, expected2)

    def test_more_than_four_values(self):
        malformed_bounds = "[0,96,1][224,320,5]"
        with self.assertRaises(ValueError):
            parse_bounds(malformed_bounds)     

    def test_parse_bounds_invalid(self):
        bounds_str = "[0,96][224]"
        with self.assertRaises(ValueError):
            parse_bounds(bounds_str)

    def test_parse_bounds_non_numeric(self):
        bounds_str = "[a,b][c,d]"
        with self.assertRaises(ValueError):
            parse_bounds(bounds_str)

    def test_parse_bounds_non_numeric(self):
        bounds_str = "[a,b][c,d]"
        with self.assertRaises(ValueError):
            parse_bounds(bounds_str)

    def test_negative_coordinates(self):
        # Negative numbers (off-screen or special cases)
        bounds_str = "[-10,-20][50,100]"
        expected = [-10, -20, 50, 100]
        result = parse_bounds(bounds_str)
        self.assertEqual(result, expected)

    def test_zero_width_height(self):
        # Zero-width element
        bounds_str_width_zero = "[50,50][50,100]"
        expected_width_zero = [50, 50, 50, 100]
        self.assertEqual(parse_bounds(bounds_str_width_zero), expected_width_zero)

        # Zero-height element
        bounds_str_height_zero = "[20,20][80,20]"
        expected_height_zero = [20, 20, 80, 20]
        self.assertEqual(parse_bounds(bounds_str_height_zero), expected_height_zero)

    # -------- extract_leaf_bounds tests --------
    def test_extract_leaf_bounds_single_node(self):
        xml_data = """
        <hierarchy rotation="0">
            <node bounds='[0,0][100,100]'/>
        </hierarchy>
        """
        root = ET.fromstring(xml_data)
        bounds = []
        extract_leaf_bounds(root, bounds)
        self.assertEqual(bounds, [[0, 0, 100, 100]])

    def test_extract_leaf_bounds_nested_nodes(self):
        xml_data = """
        <hierarchy rotation="0">
            <node bounds='[0,0][500,500]'>
                <node bounds='[10,10][100,100]'></node>
                <node bounds='[150,150][300,300]'></node>
            </node>
        </hierarchy>
        """
        root = ET.fromstring(xml_data)
        bounds = []
        extract_leaf_bounds(root, bounds)
        self.assertEqual(bounds, [[10, 10, 100, 100], [150, 150, 300, 300]])

    # -------- get_leaf_node_bounds tests --------
    def test_get_leaf_node_bounds_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            get_leaf_node_bounds(os.path.join("tests","nonexistent.xml"))

    def test_get_leaf_node_bounds_malformed_xml(self):
        malformed_xml_path = os.path.join("tests","malformed.xml")
        with open(malformed_xml_path, "w", newline="") as f:
            f.write("<hierarchy rotation='0'><node><child></node></hierarchy>")  # Missing closing tag for child
        with self.assertRaises(ET.ParseError):
            get_leaf_node_bounds(malformed_xml_path)
        os.remove(malformed_xml_path)

    def test_extra_closing_tag(self):
        malformed_xml_path = os.path.join("tests","temp_extra_tag.xml")
        with open(malformed_xml_path, "w", newline="") as f:
            f.write("<hierarchy rotation='0'><node bounds='[0,0][100,100]'></node></node></hierarchy>")  # extra </node>
        with self.assertRaises(ET.ParseError):
            get_leaf_node_bounds(malformed_xml_path)
        os.remove(malformed_xml_path)

    def test_invalid_nesting(self):
        malformed_xml_path = os.path.join("tests","temp_invalid_nesting.xml")
        with open(malformed_xml_path, "w", newline="") as f:
            f.write("<hierarchy rotation='0'><node bounds='[0,0][100,100]'><child bounds='[10,10][50,50]'></node></child></hierarchy>")  # wrong order
        with self.assertRaises(ET.ParseError):
            get_leaf_node_bounds(malformed_xml_path)
        os.remove(malformed_xml_path)

    def test_empty_xml_file(self):
        empty_xml_path = os.path.join("tests","temp_empty.xml")
        with open(empty_xml_path, "w", newline="") as f:
            pass  # write nothing → empty file
        with self.assertRaises(ET.ParseError):
            get_leaf_node_bounds(empty_xml_path)
        os.remove(empty_xml_path)

    def test_plain_text_file(self):
        file_path = os.path.join("tests","temp_plain_text.xml")
        with open(file_path, "w", newline="") as f:
            f.write("This is not XML at all!")
        with self.assertRaises(ET.ParseError):
            get_leaf_node_bounds(file_path)
        os.remove(file_path)

    def test_html_file(self):
        file_path = os.path.join("tests","temp_html.xml")
        html_content = "<html><body><h1>Hello</h1></body></html>"
        with open(file_path, "w", newline="") as f:
            f.write(html_content)
        with self.assertRaises(ValueError):
            get_leaf_node_bounds(file_path)
        os.remove(file_path)

    def test_binary_file(self):
        file_path = os.path.join("tests","temp_binary.xml")
        with open(file_path, "wb") as f:
            f.write(b'\x00\xFF\xAB\xCD')  # some random bytes
        with self.assertRaises(ET.ParseError):
            get_leaf_node_bounds(file_path)
        os.remove(file_path)

    def test_get_leaf_node_bounds_valid_file(self):
        valid_xml_path = os.path.join("tests","temp_valid.xml")
        with open(valid_xml_path, "w", newline="") as f:
            f.write("<hierarchy rotation='0'><node bounds='[0,0][200,200]'><child bounds='[10,10][50,50]'></child></node></hierarchy>")
        bounds = get_leaf_node_bounds(valid_xml_path)
        self.assertEqual(bounds, [[10, 10, 50, 50]])
        os.remove(valid_xml_path)

if __name__ == "__main__":
    unittest.main()

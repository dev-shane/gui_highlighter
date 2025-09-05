import xml.etree.ElementTree as ET
import re

def get_leaf_node_bounds(xml_file_path: str) -> list:
    """
    Parse an Android UI XML file and return a list of leaf node bounds.

    This function reads an XML file captured using Android's UIAutomator
    framework, traverses the hierarchical UI tree, and collects the 
    bounds of all **leaf nodes** (nodes with no children). Each leaf 
    node's bounds are returned as a list of four integers: [x1, y1, x2, y2],
    representing the top-left and bottom-right coordinates of the element 
    on the screen.

    Args:
        xml_file_path (str): Path to the XML file representing a UI screen.

    Returns:
        bounds (list[list[int]]): A list where each element is a list of four integers 
        representing the bounds of a leaf node. Example:
            [[0, 96, 224, 320], [230, 100, 400, 300], ...]

    Raises:
        ET.ParseError: If the XML file is malformed.
        FileNotFoundError: If the XML file does not exist.
        ValueError: If there is an unexpected root tag (properly formatted html) or 
        there is an error in leaf bounds conversion.
    """
    bounds = []
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    if root.tag != 'hierarchy':
        raise ValueError(f"Unexpected root element: {root.tag}") 
    extract_leaf_bounds(root, bounds)
    return bounds

def extract_leaf_bounds(node: ET.Element, bounds: list[list[int]]) -> None:
    """
    Recursively traverse an XML node tree to collect the 'bounds' attributes 
    of all leaf nodes (nodes with no children). The results are accumulated in 
    the `bounds` list passed as a parameter.

    Args:
        node (ET.Element): The current XML node being processed.
        bounds (list[list[int]]): A list that will be populated with lists of four integers 
            [x1, y1, x2, y2] extracted from the 'bounds' attributes of leaf nodes.
    """
    children = list(node) # gives list of node's immediate children
    if not children:  # base case: no children → leaf node
        bounds_str = node.get('bounds')
        if bounds_str:   
            coords = parse_bounds(bounds_str) # <- converts "[0,96][224,320]" → [0,96,224,320]
            bounds.append(coords)
    else: # recursive case
        for child in children:
            extract_leaf_bounds(child, bounds)

def parse_bounds(bounds_str: str) -> list[int]:
    """
    Convert a bounds string from an Android UI XML element into a list of integers.

    The 'bounds' attribute in Android UIAutomator XML is typically formatted as:
        "[x1,y1][x2,y2]"
    where (x1, y1) represents the top-left corner and (x2, y2) represents the
    bottom-right corner of the UI element on the screen.

    This function extracts all numeric values from the string and returns them
    as a list of four integers: [x1, y1, x2, y2].

    Args:
        bounds_str (str): A bounds string in the format "[x1,y1][x2,y2]".

    Returns:
        coords (list[int]): A list of four integers representing the coordinates of
        the UI element. Example: [0, 96, 224, 320].

    Raises:
        ValueError: If the bounds string does not contain exactly four integers.
    """
    coords = list(map(int, re.findall(r"-?\d+", bounds_str))) # finds optional minus sign and numbers
    if len(coords) != 4:
        raise ValueError(f"Expected 4 coordinates, got {len(coords)} from {bounds_str}")
    return coords



import unittest
import os
from PIL import Image, UnidentifiedImageError
from src.drawer import draw_leaf_bounds

"""
Drawer Module Tests Summary:

These tests cover the draw_leaf_bounds function, which takes a list of leaf node bounds
and an image (input path) and draws rectangles on the image at the specified coordinates.

Tests performed:
- Single rectangle drawing: verifies that a simple rectangle is drawn correctly.
- Multiple rectangles: verifies that several rectangles are drawn simultaneously.
- Out-of-bounds rectangles: ensures rectangles partially or fully outside the image
  are drawn/clipped safely without errors.
- No bounds: verifies that passing an empty list leaves the image unchanged.
- Nonexistent input file: ensures proper FileNotFoundError is raised.
- Invalid image file: ensures that corrupted or non-image files raise PIL.UnidentifiedImageError.
- Default output path: verifies that if no output path is given, the function saves to the
  input image location correctly.
- Degenerate rectangles: ensures rectangles with zero width/height still draw minimally
  without errors.

Tests not included but could be added for more comprehensive coverage:
- Very large number of rectangles (stress test)
- Transparent images or different color modes
- Different rectangle line thicknesses
- Performance benchmarks on large images

Given the expected use case (relatively small UI screenshots), these tests cover the
most likely scenarios and edge cases relevant for the program.
"""

INPUT_PATH = os.path.join("tests", "test_inputs")
OUTPUT_PATH = os.path.join("tests", "test_outputs")
YELLOW = (255, 255, 0)

os.makedirs(INPUT_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)

class TestDrawer(unittest.TestCase):

    def _create_blank_image(self, name="blank.png", size=(200, 200), color="white"):
        # Helper to create a fresh blank image and return its path.
        img = Image.new("RGB", size, color=color)
        img_path = os.path.join(INPUT_PATH, name)
        img.save(img_path)
        return img_path

    def _load_pixels(self, path):
        # Helper to load pixel access from an image.
        return Image.open(path).load()

    def test_draw_single_rectangle(self):
        img_path = self._create_blank_image("single_rect.png")
        output_path = os.path.join(OUTPUT_PATH, "single_rect.png")

        bounds = [[20, 20, 100, 100]]
        draw_leaf_bounds(img_path, bounds, output_path)

        pixels = self._load_pixels(output_path)
        # Check corners are yellow
        self.assertEqual(pixels[20, 20], YELLOW)
        self.assertEqual(pixels[100, 20], YELLOW)
        self.assertEqual(pixels[20, 100], YELLOW)
        self.assertEqual(pixels[100, 100], YELLOW)

    def test_draw_multiple_rectangles(self):
        img_path = self._create_blank_image("multi_rect.png")
        output_path = os.path.join(OUTPUT_PATH, "multi_rect.png")

        bounds = [
            [10, 10, 50, 50],
            [60, 60, 120, 120],
            [130, 40, 180, 90],
        ]
        draw_leaf_bounds(img_path, bounds, output_path)

        pixels = self._load_pixels(output_path)
        # Spot check each rectangle
        self.assertEqual(pixels[10, 10], YELLOW)
        self.assertEqual(pixels[120, 120], YELLOW)
        self.assertEqual(pixels[180, 90], YELLOW)

    def test_out_of_bounds_rectangle(self):
        img_path = self._create_blank_image("outofbounds.png")
        output_path = os.path.join(OUTPUT_PATH, "outofbounds.png")

        bounds = [[-10, -10, 150, 150]]  # extends outside
        draw_leaf_bounds(img_path, bounds, output_path)

        pixels = self._load_pixels(output_path)
        # Corners inside valid range should still be drawn
        self.assertEqual(pixels[0, 150], YELLOW)
        self.assertEqual(pixels[150, 0], YELLOW)
        self.assertEqual(pixels[150, 150], YELLOW)

    def test_no_bounds(self):
        img_path = self._create_blank_image("nobounds.png")
        output_path = os.path.join(OUTPUT_PATH, "nobounds.png")

        bounds = []
        draw_leaf_bounds(img_path, bounds, output_path)

        pixels = self._load_pixels(output_path)
        # Should remain completely white at sample locations
        self.assertEqual(pixels[0, 0], (255, 255, 255))
        self.assertEqual(pixels[100, 100], (255, 255, 255))

    def test_nonexistent_input_file(self):
        output_path = os.path.join(OUTPUT_PATH, "nonexistent.png")
        with self.assertRaises(FileNotFoundError):
            draw_leaf_bounds(os.path.join("tests", "nonexistant.png"), [[0, 0, 10, 10]], output_path)

    def test_invalid_image_file(self):
        # Create a fake text file instead of PNG
        bad_path = os.path.join(INPUT_PATH, "not_an_image.png")
        with open(bad_path, "w") as f:
            f.write("This is not an image!")
        output_path = os.path.join(OUTPUT_PATH, "bad.png")

        with self.assertRaises(UnidentifiedImageError):
            draw_leaf_bounds(bad_path, [[0, 0, 10, 10]], output_path)

    def test_default_output_path(self):
        # If no output path is provided, should save next to input image.
        img_path = self._create_blank_image("default_output.png")
        bounds = [[30, 30, 80, 80]]

        # Call without output_path
        draw_leaf_bounds(img_path, bounds)

        # Expect file next to input with a modified name
        base, ext = os.path.splitext(img_path)
        output_path = f"{base}_annotated{ext}"
        self.assertTrue(os.path.exists(output_path))

        # Ensure drawing occurred (sample corner pixel should be yellow)
        pixels = self._load_pixels(output_path)
        self.assertEqual(pixels[30, 30], YELLOW)
        self.assertEqual(pixels[80, 80], YELLOW)

    def test_degenerate_rectangle(self):
        # Rectangles with zero width or height should not crash and should draw minimally.
        img_path = self._create_blank_image("degenerate.png")
        output_path = os.path.join(OUTPUT_PATH, "degenerate.png")

        bounds = [[50, 50, 50, 50]]  # single pixel rectangle
        draw_leaf_bounds(img_path, bounds, output_path)

        pixels = self._load_pixels(output_path)
        self.assertEqual(pixels[50, 50], YELLOW)  # should draw at least one pixel


if __name__ == "__main__":
    unittest.main()

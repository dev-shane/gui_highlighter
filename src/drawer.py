from PIL import Image, ImageDraw, UnidentifiedImageError
import os

def draw_leaf_bounds(input_image_path: str, bounds_list: list[list[int]], output_path: str = None, color=(255, 255, 0), line_width=5):
    """
    Draw rectangles on an image representing leaf bounds.

    Args:
        input_image_path (str): Path to the input PNG image.
        bounds_list (list[list[int]]): List of [x1, y1, x2, y2] coordinates.
        output_path (str, optional): Path to save the output image. Defaults to same folder as input.
        color (tuple, optional): RGB color of the rectangle. Defaults to yellow (255,0,255).
        line_width (int, optional): Width of the rectangle lines. Defaults to 5.

    Raises:
        FileNotFoundError: If the input image does not exist.
        UnidentifiedImageError: If the file cannot be opened as an image.
        PermissionError: If saving to output_path is not permitted.
    """
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Input file not found: {input_image_path}")

    try:
        img = Image.open(input_image_path)
    except UnidentifiedImageError:
        raise UnidentifiedImageError(f"Cannot open image: {input_image_path}")

    if output_path is None:
        # Save in same folder, optionally add suffix
        base, ext = os.path.splitext(input_image_path)
        output_path = f"{base}_annotated{ext}"

    draw = ImageDraw.Draw(img)

    for bound in bounds_list:
        x1, y1, x2, y2 = bound

        # Handle degenerate rectangles (zero width/height)
        if x1 == x2 and y1 == y2:
            draw.point((x1, y1), fill=color)
        elif x1 == x2:
            draw.line([(x1, y1), (x2, y2)], fill=color, width=line_width)
        elif y1 == y2:
            draw.line([(x1, y1), (x2, y2)], fill=color, width=line_width)
        else:
            draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)

    try:
        img.save(output_path)
    except PermissionError:
        raise PermissionError(f"Cannot save image to {output_path}")

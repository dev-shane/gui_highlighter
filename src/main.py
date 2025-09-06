import argparse, os
import xml.etree.ElementTree as ET
from PIL import UnidentifiedImageError
from src.parser import get_leaf_node_bounds
from src.drawer import draw_leaf_bounds
import logging

def create_logger(log_file="app.log", console_level=logging.WARNING, file_level=logging.DEBUG):
    """
    Create and configure a single logger for the application.

    Args:
        log_file (str): Path to the log file. Default is "app.log".
        console_level (int): Logging level for console output. Default is WARNING.
        file_level (int): Logging level for file output. Default is DEBUG.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Capture all messages

    # File handler
    file_handler = logging.FileHandler(log_file, mode="w")  # overwrite each run
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_formatter)

    # Add handlers if they haven't been added yet
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", default="output",
    help="Folder to save annotated images (default: output/)")
    return p.parse_args()

def main():
    args = parse_args()
    data_dir = "data"
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    logger = create_logger()

    # Find all xml files in data/
    for xml_file in os.listdir(data_dir):
        if not xml_file.endswith(".xml"):
            continue
        png_file = os.path.join(data_dir, xml_file.replace(".xml", ".png"))
        if not os.path.exists(png_file):
            logger.warning(f"Missing PNG for {xml_file}, skipping")
            continue
        
        try:
            # run parser + drawer
            bounds = get_leaf_node_bounds(os.path.join(data_dir, xml_file))
            out_path = os.path.join(output_dir, os.path.basename(png_file))
            draw_leaf_bounds(png_file, bounds, out_path)

            logger.info(f"Success: Output saved to {out_path}")

        except FileNotFoundError as e:
            logger.warning(f"FileNotFoundError: {e}")

        except ET.ParseError as e:
            logger.error(f"ParseError in {xml_file}: {e}")

        except ValueError as e:
            logger.error(f"ValueError in {xml_file}: {e}")

        except UnidentifiedImageError as e:
            logger.error(f"UnidentifiedImageError in {out_path}: {e}")

        except PermissionError as e:
            logger.error(f"PermissionError: {e}")

        except Exception as e:
            # Catch anything unexpected
            logger.critical(f"Unexpected error with {xml_file} or {out_path}: {e}")            

if __name__ == "__main__":
    main()

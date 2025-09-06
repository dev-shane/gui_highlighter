import argparse, os
import xml.etree.ElementTree as ET
from PIL import UnidentifiedImageError
from src.parser import get_leaf_node_bounds
from src.drawer import draw_leaf_bounds

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

    # Find all xml files in data/
    for xml_file in os.listdir(data_dir):
        if not xml_file.endswith(".xml"):
            continue
        png_file = os.path.join(data_dir, xml_file.replace(".xml", ".png"))
        if not os.path.exists(png_file):
            print(f"Missing PNG for {xml_file}, skipping")
            continue
        
        try:
            # run parser + drawer
            bounds = get_leaf_node_bounds(os.path.join(data_dir, xml_file))
            out_path = os.path.join(output_dir, os.path.basename(png_file))
            draw_leaf_bounds(png_file, bounds, out_path)

            print(f"✅ Success: Output saved to {out_path}")

        except FileNotFoundError as e:
            print(f"❌ FileNotFoundError: {e}")

        except ET.ParseError as e:
            print(f"❌ ParseError in {xml_file}: {e}")

        except ValueError as e:
            print(f"❌ ValueError in {xml_file}: {e}")

        except UnidentifiedImageError as e:
            print(f"❌ UnidentifiedImageError in {out_path}: {e}")

        except PermissionError as e:
            print(f"❌ PermissionError: {e}")

        except Exception as e:
            # Catch anything unexpected
            print(f"❌ Unexpected error with {xml_file} or {out_path}: {e}")            

if __name__ == "__main__":
    main()

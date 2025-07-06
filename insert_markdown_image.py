

import argparse
import os
import sys

def insert_image_tag(markdown_file: str, image_path_in_md: str, alt_text: str):
    """
    Inserts a Markdown image tag at the top of a specified file.

    Args:
        markdown_file: The absolute path to the markdown file.
        image_path_in_md: The relative path of the image for the markdown tag (e.g., './images/my_image.png').
        alt_text: The alt text for the image.
    """
    if not os.path.exists(markdown_file):
        print(f"Error: Markdown file not found at '{markdown_file}'", file=sys.stderr)
        sys.exit(1)

    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create the image tag
        image_tag = f"![{alt_text}]({image_path_in_md})\n\n"

        # Remove old image tag if it exists to avoid duplicates
        if content.startswith("!["):
            first_line_end = content.find('\n')
            content = content[first_line_end+1:]
            # Also remove the blank line after the image
            if content.startswith('\n'):
                content = content[1:]

        # Prepend the new image tag
        new_content = image_tag + content

        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Successfully inserted image tag for '{os.path.basename(image_path_in_md)}' into '{os.path.basename(markdown_file)}'")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Insert a Markdown image tag at the top of a file.')
    parser.add_argument('--markdown_file', type=str, required=True, help='Absolute path to the markdown file.')
    parser.add_argument('--image_path', type=str, required=True, help='Relative path for the image tag (e.g., ./images/pic.png).')
    parser.add_argument('--alt_text', type=str, required=True, help='Alt text for the image.')

    args = parser.parse_args()
    insert_image_tag(args.markdown_file, args.image_path, args.alt_text)




import argparse
import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import sys

def generate_and_insert_image(prompt: str, image_filename: str, markdown_file: str, alt_text: str):
    """
    Generates an image based on a prompt and inserts it into a markdown file,
    using the confirmed working API call structure.
    """
    try:
        # 1. Setup paths
        # The script assumes the markdown files are in a subdirectory, and the images folder should be inside that same subdirectory.
        markdown_dir = os.path.dirname(markdown_file)
        images_dir = os.path.join(markdown_dir, 'images')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        
        # Relative path for the markdown tag, relative to the markdown file itself
        image_path_for_md = os.path.join('./images', image_filename)
        # Absolute path for saving the image file
        image_path_for_save = os.path.join(images_dir, image_filename)
        
        markdown_image_tag = f"![{alt_text}]({image_path_for_md})\n\n"

        # 2. Generate Image
        print(f"Generating image for prompt: '{prompt}'...")
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
              response_modalities=['TEXT', 'IMAGE']
            )
        )

        # 3. Save Image
        image_saved = False
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO((part.inline_data.data)))
                    image.save(image_path_for_save)
                    image_saved = True
                    print(f"Image saved to {image_path_for_save}")
                    break
        
        if not image_saved:
            print("Error: Image generation failed. No image data received.", file=sys.stderr)
            if response.prompt_feedback:
                print(f"Prompt Feedback: {response.prompt_feedback}", file=sys.stderr)
            sys.exit(1)

        # 4. Insert into Markdown file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Remove old image tag if it exists to avoid duplicates
        if lines and lines[0].startswith('!['):
            lines.pop(0)
            if lines and lines[0].strip() == '':
                lines.pop(0)

        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_image_tag)
            f.writelines(lines)
            
        print(f"Image link inserted into {markdown_file}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate an image and insert it into a Markdown file.')
    parser.add_argument('--prompt', type=str, required=True, help='The prompt to generate the image from.')
    parser.add_argument('--image_filename', type=str, required=True, help='The filename for the output image.')
    parser.add_argument('--markdown_file', type=str, required=True, help='The path to the markdown file.')
    parser.add_argument('--alt_text', type=str, required=True, help='The alt text for the image.')
    args = parser.parse_args()
    generate_and_insert_image(args.prompt, args.image_filename, args.markdown_file, args.alt_text)

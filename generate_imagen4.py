
import argparse
import os
import sys
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

def generate_image_with_imagen4(prompt: str, output_path: str):
    """
    Generates a single image using the Imagen 4 model and saves it to the specified path.
    """
    try:
        print(f"Generating image for prompt: '{prompt}'...")
        client = genai.Client()
        response = client.models.generate_images(
            model='imagen-4.0-generate-preview-06-06',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,  # Generate one high-quality image
            )
        )
        
        if response.generated_images:
            # Save the first generated image
            generated_image = response.generated_images[0]
            generated_image.image.save(output_path)
            print(f"Image successfully saved to {output_path}")
            return True
        else:
            print("Error: Image generation failed. No images were returned.", file=sys.stderr)
            # You can add more detailed error logging here if needed, e.g., response.error
            return False

    except Exception as e:
        print(f"An error occurred during image generation: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate an image using Imagen 4.')
    parser.add_argument('--prompt', type=str, required=True, help='The prompt for the image generation.')
    parser.add_argument('--output_path', type=str, required=True, help='The full path to save the output image.')
    
    args = parser.parse_args()
    
    if not os.path.exists(os.path.dirname(args.output_path)):
        os.makedirs(os.path.dirname(args.output_path))

    generate_image_with_imagen4(args.prompt, args.output_path)

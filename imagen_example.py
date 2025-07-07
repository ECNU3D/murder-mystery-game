from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()

response = client.models.generate_images(
    model='imagen-4.0-generate-preview-06-06',
    prompt='Robot holding a red skateboard',
    config=types.GenerateImagesConfig(
        number_of_images= 4,
    )
)
for i, generated_image in enumerate(response.generated_images):
  generated_image.image.show()
  generated_image.image.save(f'generated_image_{i}.png')


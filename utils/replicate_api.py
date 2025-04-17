import requests
import os
import base64
import requests
from io import BytesIO
from utils.s3_upload import upload_to_s3
from PIL import Image

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

def remove_background(image_url):
    print(f"remove background input image_url: {image_url}")
    headers = {
        "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
        "Prefer": "wait"
    }
    data = {
        "version": "95fcc2a26d3899cd6c2691c900465aaeff466285a65c14638cc5f36f34befaf1",
        "input": {"image": image_url}
    }
    response = requests.post("https://api.replicate.com/v1/predictions", json=data, headers=headers)
    response.raise_for_status()
    return response.json()["output"]

def upscale_image(image_url):
    print(f"upscale input image image_url: {image_url}")
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
    headers = {
        "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
        "Prefer": "wait"
    }
    data = {
        "version": "f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa",
        "input": {"image": image_url, "scale": 2}
    }
    response = requests.post("https://api.replicate.com/v1/predictions", json=data, headers=headers)
    response.raise_for_status()
    return response.json()["output"]

def remove_bg_from_url(image_url: str, output_path: str = "output_124.png") -> str:
    """
    Downloads an image from a URL, removes its background using RGBKit API,
    and saves the result to the given output path.

    Args:
        image_url (str): URL of the image to process.
        output_path (str): Path to save the output image.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # 1. Download the image
        img_response = requests.get(image_url)
        if img_response.status_code != 200:
            print("❌ Failed to download image:", img_response.status_code)
            return False

        image_bytes = img_response.content

        # 2. Convert to base64 (for your reference, not strictly needed here)
        base64_string = base64.b64encode(image_bytes).decode("utf-8")

        # 3. Prepare image as file-like object for API
        image_file = BytesIO(base64.b64decode(base64_string))

        # 4. Call RGBKit API
        files = {
            "img": ("image.jpg", image_file, "image/jpeg")
        }
        response = requests.post("https://apis.rgbkit.com/v1/removebg", files=files)

        # 5. Save result
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Background removed image saved to: {output_path}")
        else:
            print("❌ API call failed:", response.status_code, response.text)

        add_white_background(output_path, "white_background_"+output_path)
        upload_to_s3("white_background_"+output_path, os.getenv("S3_BUCKET_NAME"), "agents/image_processor_agent/"+output_path)

        return "https://d2zl67esqcp9tl.cloudfront.net/agents/image_processor_agent/" + output_path
    except Exception as e:
        print("❌ Error:", str(e))
        return ""

def add_white_background(input_path: str, output_path: str):
    # Open the image with transparency (e.g., PNG with alpha channel)
    image = Image.open(input_path).convert("RGBA")

    # Create a white background image with the same size
    white_bg = Image.new("RGBA", image.size, (255, 255, 255, 255))  # white background

    # Paste the transparent image on top of the white background
    white_bg.paste(image, (0, 0), image)

    # Convert to RGB (removes alpha channel) and save
    final_image = white_bg.convert("RGB")
    final_image.save(output_path, "JPEG")
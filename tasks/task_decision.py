from crewai import Task
from PIL import Image
import requests
from io import BytesIO
import base64

from envs.njc.DLLs.pyexpat import features
import json, re

from utils.image_details import ImageDetails


def get_decision_task(agent, image_details: ImageDetails):
    image_features = image_details.features
    if features:
        print(f"success in getting image features: {image_features}")
    else:
        print("❌ Could not parse valid JSON.")


    print(f"Image features: {image_features}")
    # resolution = get_image_resolution_from_url(image_url)
    # print(f"Image resolution: {resolution[0]}x{resolution[1]}")

    commands = generate_command_pipeline(image_features)
    print(f"commands = {commands}")

    image_details.operations = commands

    return Task(
        description="Based on features, decide actions needed.",
        expected_output=str(commands),
        agent=agent
    )

def get_image_resolution_from_url(image_url: str) -> tuple:
    """
    Downloads image from URL and returns (width, height).
    """
    response = requests.get(image_url)
    response.raise_for_status()  # Raise error if download fails

    image = Image.open(BytesIO(response.content))
    return image.size  # (width, height)

def image_to_base64(path: str) -> str:
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def save_image_from_url(image_url, save_path):
    response = requests.get(image_url)
    response.raise_for_status()  # Raise error for bad status

    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"✅ Image saved to {save_path}")

def extract_json(text):
    if isinstance(text, dict):
        return text  # Already parsed
    if isinstance(text, str):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return None
    return None

def generate_command_pipeline(image_features:dict):
    commands = []
    # Step 2: Get image features
    resolution = image_features.get("resolution")
    width = resolution[0]
    height = resolution[1]
    laplacian_score = image_features.get("sharpness_score")
    background_color = image_features.get("background_color")

    print(f"🖼️ Resolution: {width}x{height}")
    print(f"🔍 Laplacian Score: {laplacian_score}")
    print(f"🎨 Background: {background_color}")

    # Rule 1: Reject very blurry and very small images
    if laplacian_score < 50 and (width < 72 or height < 72):
        print("❌ Skipped: Blurry and very small image.")
        return None

    # Rule 2: Image already has white background and is blurry — skip
    if background_color == "white" and laplacian_score < 50:
        print("⚪ Skipped: White background but blurry.")
        return None

    # Rule 3: Image is clear but background is not white — clean it
    if laplacian_score > 50:
        print("✂️ Removing background...")
        commands.append("remove_background")

    # Rule 4: Upscale if resolution is low
    if width < 200 or height < 200:
        print("📈 Upscaling image...")
        commands.append("upscale")

    print("✅ commands processed successfully.")
    return commands




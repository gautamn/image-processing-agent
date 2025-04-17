from crewai import Task
import requests

from utils.image_details import ImageDetails


def get_loader_task(agent, image_details: ImageDetails):
    image_url = image_details.image_url #get_current_image_url()
    print(f"\n🔁 Loading image from URL: {image_url}")

    # Check if image exists and is accessible
    try:
        response = requests.head(image_url, timeout=5)
        if response.status_code != 200 or 'image' not in response.headers.get('Content-Type', ''):
            raise ValueError(f"Image not found or not valid at URL: {image_url}")
    except requests.RequestException as e:
        raise ValueError(f"Failed to load image from URL: {image_url}. Error: {e}")

    return Task(
        description="Load the image from a URL and return its link.",
        expected_output=image_url,
        agent=agent
    )

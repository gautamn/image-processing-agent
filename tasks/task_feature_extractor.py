from crewai import Task
from openai import OpenAI
import json, re
from utils.image_details import ImageDetails

def get_feature_extraction_task(agent, image_details: ImageDetails):

    image_url = image_details.image_url
    #gpt_output = get_image_features(image_url)
    gpt_output = {
        "resolution": [768, 1020],
        "sharpness_score": 80,
        "background_color": "white"
    }
    features = extract_json(gpt_output)
    if features:
        print(f"success in getting image features: {features}")
    else:
        print("❌ Could not parse valid JSON.")

    print(f"Image features: {features}")

    image_details.features = features

    return Task(
        description="Given an image URL, extract features from LLM and return a dictionary like: "
                    "{'sharpness': 0.4, 'resolution': (600, 400), 'background': 'complex'}",
        expected_output=str(gpt_output),
        agent=agent
    )

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

def get_image_features(image_url):
    prompt = """
    You are an expert in image quality assessment. Given an image, extract the following features:

    1. Resolution (width x height in pixels)
    2. Visual sharpness (from 0 to 100, higher means sharper)
    3. Background color (e.g., white, black, complex, transparent) in hexadecimal. Like for white #FFFFFF

    Respond in this format:
    {
      "resolution": [width, height],
      "sharpness_score": score,
      "background_color": #FFFFFF 
    }
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ],
        max_tokens=500
    )
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)

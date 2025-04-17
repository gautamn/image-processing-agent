from utils.image_details import ImageDetails
from utils.replicate_api import upscale_image, remove_bg_from_url

import ast

def process_image_with_replicate(image_details: ImageDetails):

    print("\n🧠 Starting image processing...")
    current_image = image_details.image_url
    operations = image_details.operations
    print(f"🤖🤖🤖 LLM Decisions: {operations}")

    #decisions = process_image_decision(operations)
    #print(f"🎯🎯🤖🤖🤖decisions: {decisions}")

    #current_image = image_url
    for operation in operations:

        if operation == "remove_background":
            print("🎯 Removing background...")
            current_image = remove_bg_from_url(current_image)
        elif operation == "upscale":
            print("📈 Upscaling image...")
            current_image = upscale_image(current_image)

    print("✅ Final processed image URL:", current_image)
    return current_image

def process_image_decision(decisions):

    try:
        # Clean and safely parse output to list
        decision_line = decisions.strip().split("\n")[-1]
        actions = ast.literal_eval(decision_line)
        if isinstance(actions, list):
            return actions
    except Exception as e:
        print("❌ Failed to parse LLM decision:", e)

    return []

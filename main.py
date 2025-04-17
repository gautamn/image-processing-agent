import os

from langtrace_python_sdk import langtrace
langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"))

from crewai import Crew
from agent_config.image_loader_agent import image_loader_agent
from agent_config.feature_extractor_agent import feature_extractor_agent
from agent_config.decision_maker_agent import decision_maker_agent
from agent_config.image_processor_agent import image_processor_agent

from tasks.task_loader import get_loader_task
from tasks.task_feature_extractor import get_feature_extraction_task
from tasks.task_decision import get_decision_task
from tasks.task_processor import get_processing_task

from dotenv import load_dotenv
from utils.image_details import ImageDetails

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

# List of image URLs to iterate
image_urls = [
    "https://d2zl67esqcp9tl.cloudfront.net/extract_images/9647.jpg"
]

if __name__ == "__main__":
    for idx, image_url in enumerate(image_urls):
        print(f"\n\n🔁 Processing image {idx+1}: {image_url}")
        image_details = ImageDetails(image_url=image_url, features={}, operations="")

        crew = Crew(
            agents=[
                image_loader_agent,
                feature_extractor_agent,
                decision_maker_agent,
                image_processor_agent
            ],
            tasks=[
                get_loader_task(image_loader_agent, image_details),
                get_feature_extraction_task(feature_extractor_agent, image_details),
                get_decision_task(decision_maker_agent, image_details),
                get_processing_task(image_processor_agent, image_details)
            ],
            verbose=True
        )

        result = crew.kickoff()
        print(f"\n✅ Final Output for image {idx+1}: {result}")


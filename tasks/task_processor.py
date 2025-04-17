from crewai import Task
from tools.image_processing_tools import ReplicateImageProcessorTool
from utils.image_details import ImageDetails

def get_processing_task(agent, image_details: ImageDetails):
    # Create tool instance with the image details
    replicate_image_processor_tool = ReplicateImageProcessorTool(image_details=image_details)
    return Task(
        description="""
            Call the `replicate_image_processor` tool to process the image.
            Return the final image URL after all processing is done.""",
        expected_output="A final image URL after processing.",
        agent=agent,
        tools=[replicate_image_processor_tool]
    )
from crewai.tools import BaseTool
from pydantic import Field
from utils.image_details import ImageDetails
from utils.processing_logic import process_image_with_replicate


class ReplicateImageProcessorTool(BaseTool):
    name: str = Field(default="replicate_image_processor")
    description: str = Field(default="Process images using Replicate API")
    image_details: ImageDetails = Field(default=None)

    def __init__(self, image_details=None):
        # Initialize with explicit description of how to use the tool
        super().__init__(
            name="replicate_image_processor",
            description="Process images using Replicate API. Provide any processing instructions as input."
        )
        object.__setattr__(self, "image_details", image_details)

    def _run(self, *args, **kwargs) -> str:
        # The query parameter must be used when the tool is invoked
        print(f"Processing image with instructions: {self.image_details}")
        return process_image_with_replicate(self.image_details)
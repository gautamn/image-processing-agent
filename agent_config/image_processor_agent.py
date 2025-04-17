from crewai import Agent

image_processor_agent = Agent(
    role="Image Processor",
    goal="Process image using Replicate APIs",
    backstory="Call Replicate APIs to enhance the image as required.",
    verbose=True
)

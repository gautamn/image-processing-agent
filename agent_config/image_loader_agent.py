from crewai import Agent

image_loader_agent = Agent(
    role="Image Loader",
    goal="Load the image URL for processing",
    backstory="Fetch image and pass its URL for further tasks.",
    verbose=True
)

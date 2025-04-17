from crewai import Agent

decision_maker_agent = Agent(
    role="Decision Maker",
    goal="Decide what actions to take on the image",
    backstory="Use extracted features to decide if we should remove the background or upscale the image.",
    verbose=True
)

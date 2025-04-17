from crewai import Agent

feature_extractor_agent = Agent(
    role="Feature Extractor",
    goal="Analyze sharpness, resolution, and background complexity",
    backstory="Use simple rules to determine if image needs enhancements.",
    verbose=True
)

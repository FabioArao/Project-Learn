from crewai import Agent, Crew, Task, Process
from app.tools.search_tools import SearchTools
from crewai_tools import (
    BrowserbaseLoadTool,
    CodeDocsSearchTool,
    CSVSearchTool,
    PDFSearchTool,
    WebsiteSearchTool,
)

# Initialize SearchTools
search_tools = SearchTools()

# Define agents
info_gatherer = Agent(
    role="Information Gatherer",
    goal="Gather books, articles, and videos on the requested topic.",
    tools=[search_tools.search_internet, PDFSearchTool(), WebsiteSearchTool()],
    backstory="An AI specialized in searching and gathering information from various sources."
)

content_curator = Agent(
    role="Content Curator",
    goal="Rate and curate the gathered content.",
    tools=[CSVSearchTool(), CodeDocsSearchTool()],
    backstory="An AI with expertise in evaluating and organizing information for better consumption."
)

translator = Agent(
    role="Translator",
    goal="Translate curated content into text.",
    tools=[PDFSearchTool()],
    backstory="An AI proficient in converting content into readable text formats."
)

# Create tasks for the agents
gather_task = Task(
    description='Gather relevant information on the requested topic',
    agent=info_gatherer,
    expected_output='List of gathered resources and articles'
)

curate_task = Task(
    description='Curate and rate the gathered content',
    agent=content_curator,
    expected_output='Curated list of high-quality resources'
)

translate_task = Task(
    description='Translate curated content into readable text',
    agent=translator,
    expected_output='Translated text content ready for consumption'
)

# Assemble the crew with a sequential process
learning_crew = Crew(
    agents=[info_gatherer, content_curator, translator],
    tasks=[gather_task, curate_task, translate_task],
    process=Process.sequential,
    full_output=True,
    verbose=True,
)

def create_learning_task(request_description):
    # Set the task description
    gather_task.description = request_description
    # Start the crew's task execution
    result = learning_crew.kickoff()
    return result

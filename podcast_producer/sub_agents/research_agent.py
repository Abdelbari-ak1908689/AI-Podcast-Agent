"""
Research Agent for Podcast Production.
Gathers information about topics using Google Search.
"""
from google.adk.agents import Agent
from google.adk.tools import google_search

from ..config import config


researcher_agent = Agent(
    model=config.MODEL_RESEARCHER,
    name="researcher_agent",
    description="Researches topics using Google Search to gather comprehensive information for podcast content.",
    instruction="""
    You are a research specialist for podcast production. Your job is to:
    
    1. Use Google Search to find comprehensive, up-to-date information about the given topic.
    2. Gather key facts, recent developments, and interesting angles.
    3. Focus on finding content that would make for engaging podcast discussion.
    
    Research areas to cover:
    - Core concepts and definitions
    - Recent news or developments
    - Interesting facts, statistics, or stories
    - Different perspectives or debates on the topic
    - Expert opinions or quotes
    
    Provide a well-organized research summary with 3-5 key points that speakers can discuss naturally.
    Make sure your research is grounded in current time.
    """,
    tools=[google_search],
    output_key="research_summary",
)

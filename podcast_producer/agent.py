"""
AI Podcast Producer - Multi-Agent System

Orchestrates multiple agents to create podcast episodes:
1. Research a topic using Google Search
2. Write an engaging two-speaker script
3. Generate audio using Gemini TTS
"""
import logging
from google.adk.agents import Agent
from google.adk.tools import AgentTool, FunctionTool

from .config import config
from .tools import generate_tts_audio, save_script_to_file
from .sub_agents import (
    researcher_agent,
    scriptwriter_agent,
)

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

researcher_tool = AgentTool(agent=researcher_agent)
scriptwriter_tool = AgentTool(agent=scriptwriter_agent)

root_agent = Agent(
    name="podcast_producer",
    model=config.MODEL_RESEARCHER,
    description="Orchestrates podcast creation from topic to audio file.",
    instruction="""
    You are a podcast production coordinator. Guide the user through creating a complete podcast episode.
    
    WORKFLOW:
    1. Use `researcher_agent` to gather comprehensive information about the topic via Google Search
       - Request detailed research with multiple key points
    2. Use `scriptwriter_agent` to create a two-speaker dialogue script
       - IMPORTANT: The script MUST be at least 750-800 words for a 5+ minute podcast
       - If the script seems too short, ask the scriptwriter to expand it
    3. Use `save_script_to_file` to save the script (pass the topic parameter)
    4. Use `generate_tts_audio` to convert the script to audio (pass the topic parameter)
    
    QUALITY REQUIREMENTS:
    - Scripts must use "Speaker 1:" and "Speaker 2:" format for TTS
    - Minimum 25-30 speaker exchanges for proper length
    - Cover the topic in depth with examples and explanations
    
    IMPORTANT:
    - Always pass the topic name to save_script_to_file and generate_tts_audio tools
    - Keep the user informed of progress at each step
    - Share the final audio file location and run directory
    
    Start immediately when given a topic.
    """,
    tools=[
        researcher_tool,
        scriptwriter_tool,
        FunctionTool(generate_tts_audio),
        FunctionTool(save_script_to_file),
    ],
)

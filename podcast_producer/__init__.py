"""
AI Podcast Producer - A multi-agent system for generating podcasts.

This package provides:
- root_agent: The main orchestrator agent
- Sub-agents:
  - researcher_agent: Web research using google_search
  - scriptwriter_agent: Creates two-speaker podcast scripts
  - quality_reviewer_agent: Validates script quality
- Tools: TTS generation, script saving
"""
from podcast_producer.agent import root_agent

__all__ = ["root_agent"]

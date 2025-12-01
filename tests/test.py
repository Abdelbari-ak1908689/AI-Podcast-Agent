"""
Test script for AI Podcast Producer.

This script tests the root_agent using ADK's Runner.
"""
import asyncio
import os
import logging
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

from podcast_producer import root_agent
from podcast_producer.config import config
from podcast_producer.tools import reset_run_directory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_podcast_producer(topic: str):
    """
    Tests the podcast producer with a given topic.
    
    Args:
        topic: The topic to create a podcast about.
    """
    logger.info(f"🎙️ Starting AI Podcast Producer test with topic: '{topic}'")
    
    reset_run_directory()
    
    session_service = InMemorySessionService()
    
    user_id = "test-user"
    session = await session_service.create_session(
        app_name=config.APP_NAME,
        user_id=user_id
    )
    session_id = session.id
    
    logger.info(f"Session created: {session_id}")
    
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name=config.APP_NAME
    )
    
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=f"Create a podcast about: {topic}")]
    )
    
    logger.info("Running the podcast producer agent...")
    
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message
        ):
         
            if hasattr(event, 'content') and event.content and event.content.parts:
                author = getattr(event, 'author', 'Unknown')

                part = event.content.parts[0]
                text = getattr(part, 'text', None)
                
                if text:   
                    preview = text[:300] + "..." if len(text) > 300 else text
                    logger.info(f"[{author}]: {preview}")
                else:
                    logger.debug(f"[{author}]: (non-text response)")
                
    except Exception as e:
        logger.error(f"Error during podcast production: {e}")
        raise
    
    logger.info("✅ Test completed!")


async def main():
    """Main entry point for testing."""
    
    if "GOOGLE_API_KEY" not in os.environ:
        logger.warning("⚠️ GOOGLE_API_KEY not found in environment variables.")
        logger.warning("Please set it with: export GOOGLE_API_KEY='your-key'")
        return
    
    topic = "The history of Artificial Intelligence"
    
    await test_podcast_producer(topic)


if __name__ == "__main__":
    asyncio.run(main())

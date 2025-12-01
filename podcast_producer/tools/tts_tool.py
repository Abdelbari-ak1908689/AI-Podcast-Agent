"""
TTS Tool for Podcast Production.
Converts podcast scripts to audio using Gemini TTS.
"""
import re
import time
import wave
import pathlib
import logging
from typing import Dict
from google import genai
from google.genai import types
from google.adk.tools import ToolContext
from podcast_producer.config import config

logger = logging.getLogger(__name__)


def _create_run_dir(topic: str = "podcast") -> tuple[pathlib.Path, str]:
    """
    Creates a new timestamped run directory for each podcast.
    
    Args:
        topic: The podcast topic (used for folder naming).
        
    Returns:
        Tuple of (run_directory_path, run_id).
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    sanitized_topic = re.sub(r'[^a-zA-Z0-9]', '_', topic)[:30]
    run_id = f"{timestamp}_{sanitized_topic}"
    
    run_dir = pathlib.Path(config.OUTPUT_DIR) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Created run directory: {run_dir}")
    
    return run_dir, run_id


def wave_file(filename: str, pcm: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
    """Save PCM bytes as a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


async def generate_tts_audio(
    script_text: str,
    tool_context: ToolContext,
    topic: str = "podcast"
) -> Dict[str, str]:
    """
    Converts a two-speaker podcast script into natural audio using Gemini TTS.
    
    Args:
        script_text: The podcast script with Speaker 1 and Speaker 2 dialogue.
        tool_context: ADK tool context for state management.
        topic: The podcast topic (used for file naming).
    
    Returns:
        Dictionary with status, message, and file_path.
    """
    try:
        logger.info(f"Starting TTS generation for script ({len(script_text)} chars)")
        
        if not script_text or len(script_text.strip()) < 10:
            return {
                "status": "error",
                "message": "Script text is too short or empty."
            }
        
        if "run_dir" in tool_context.state and "run_id" in tool_context.state:
            run_dir = pathlib.Path(tool_context.state["run_dir"])
            run_id = tool_context.state["run_id"]
        else:
            run_dir, run_id = _create_run_dir(topic)
            tool_context.state["run_dir"] = str(run_dir)
            tool_context.state["run_id"] = run_id
        
        client = genai.Client(api_key=config.API_KEY)

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=f"Read aloud in a warm, conversational podcast tone with natural pauses.\n\n{script_text}"
                    ),
                ],
            ),
        ]

        response = client.models.generate_content(
            model=config.MODEL_TTS,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=1.0,
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                        speaker_voice_configs=[
                            types.SpeakerVoiceConfig(
                                speaker="Speaker 1",
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                        voice_name=config.VOICE_SPEAKER_1
                                    )
                                ),
                            ),
                            types.SpeakerVoiceConfig(
                                speaker="Speaker 2",
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                        voice_name=config.VOICE_SPEAKER_2
                                    )
                                ),
                            ),
                        ]
                    )
                ),
            ),
        )

    
        audio_data = response.candidates[0].content.parts[0].inline_data.data

        output_path = run_dir / f"{run_id}.wav"
        
        wave_file(
            str(output_path),
            audio_data,
            channels=config.AUDIO_CHANNELS,
            rate=config.AUDIO_SAMPLE_RATE,
            sample_width=config.AUDIO_SAMPLE_WIDTH
        )

        logger.info(f"Audio saved successfully to {output_path.resolve()}")
        
        return {
            "status": "success",
            "message": f"🎧 Audio saved to {output_path.resolve()}",
            "file_path": str(output_path.resolve()),
            "run_directory": str(run_dir.resolve()),
        }

    except Exception as e:
        error_msg = f"TTS generation failed: {str(e)[:200]}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg
        }


async def save_script_to_file(
    script_text: str,
    tool_context: ToolContext,
    topic: str = "podcast"
) -> Dict[str, str]:
    """
    Saves the podcast script to a text file.
    
    Args:
        script_text: The podcast script content.
        tool_context: ADK tool context.
        topic: The podcast topic (used for file naming).
    
    Returns:
        Dictionary with status and file_path.
    """
    try:
        if "run_dir" in tool_context.state and "run_id" in tool_context.state:
            run_dir = pathlib.Path(tool_context.state["run_dir"])
            run_id = tool_context.state["run_id"]
        else:
            run_dir, run_id = _create_run_dir(topic)
            tool_context.state["run_dir"] = str(run_dir)
            tool_context.state["run_id"] = run_id
        
        output_path = run_dir / f"{run_id}.txt"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_text)
        
        logger.info(f"Script saved to {output_path.resolve()}")
        
        return {
            "status": "success",
            "message": f"📝 Script saved to {output_path.resolve()}",
            "file_path": str(output_path.resolve()),
            "run_directory": str(run_dir.resolve()),
        }
        
    except Exception as e:
        error_msg = f"Failed to save script: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg
        }


def reset_run_directory():
    """No longer needed - each run uses tool_context.state for directory management."""
    pass 
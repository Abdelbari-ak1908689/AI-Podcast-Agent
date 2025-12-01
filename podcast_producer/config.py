import os
from dataclasses import dataclass, field

os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")


@dataclass
class PodcastConfiguration:
    """Configuration for the AI Podcast Producer.

    Attributes:
        MODEL_RESEARCHER: Model for research and review tasks (faster).
        MODEL_SCRIPTWRITER: Model for script writing (higher quality).
        MODEL_TTS: Model for text-to-speech generation.
        APP_NAME: Application name for session management.
        VOICE_SPEAKER_1: Voice name for Speaker 1.
        VOICE_SPEAKER_2: Voice name for Speaker 2.
        AUDIO_SAMPLE_RATE: Sample rate for audio output.
        AUDIO_CHANNELS: Number of audio channels.
        AUDIO_SAMPLE_WIDTH: Sample width in bytes.
        OUTPUT_DIR: Directory for output files.
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR).
    """

    MODEL_RESEARCHER: str = "gemini-2.5-flash"  
    MODEL_SCRIPTWRITER: str = "gemini-2.5-pro"  
    MODEL_TTS: str = "gemini-2.5-pro-preview-tts" 
    

    APP_NAME: str = "ai-podcast-producer"
    
    VOICE_SPEAKER_1: str = "Zephyr"
    VOICE_SPEAKER_2: str = "Puck"
    
    AUDIO_SAMPLE_RATE: int = 24000
    AUDIO_CHANNELS: int = 1
    AUDIO_SAMPLE_WIDTH: int = 2
    

    OUTPUT_DIR: str = "output"
    
    LOG_LEVEL: str = "INFO"
    
    API_KEY: str = field(default_factory=lambda: os.environ.get("GOOGLE_API_KEY"))


config = PodcastConfiguration()

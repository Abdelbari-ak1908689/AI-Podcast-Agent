# 🎙️ AI Podcast Producer

> **Track:** Freestyle  
> **Submission:** Kaggle Agents Intensive Capstone Project (Dec 2025)

## 📋 Problem Statement

Creating high-quality podcast content is **time-consuming and resource-intensive**. Content creators face multiple challenges:

-   **Research burden**: Hours spent gathering accurate information on topics
-   **Script writing**: Crafting engaging two-person dialogue requires skill and time
-   **Audio production**: Professional voice recording is expensive and inaccessible

**The average podcast episode takes 4-8 hours to produce** — from research to final audio.

## 💡 Solution

**AI Podcast Producer** is a multi-agent AI system that **automatically generates a complete podcast episode from any topic** in minutes. Simply provide a topic, and the system handles everything:

1. **Researches** the topic using Google Search
2. **Writes** an engaging two-speaker dialogue script
3. **Generates** professional multi-voice audio using Gemini TTS

### Why Agents?

Traditional automation can't handle this task because each step requires **reasoning and adaptation**:

-   The researcher must evaluate search results and extract relevant facts
-   The scriptwriter must craft natural dialogue that flows conversationally
-   The coordinator must ensure each step builds on the previous one

**Agents uniquely solve this** by using LLMs to reason through each step, adapting their approach based on the topic and context.

---

## 🏗️ Architecture

The system uses the **AgentTool pattern** — a multi-agent orchestration approach where specialized agents are wrapped as tools for a root coordinator agent.

```
┌─────────────────────────────────────────────────────────────────┐
│                     🎯 ROOT AGENT                               │
│                   (podcast_producer)                            │
│                   Model: gemini-2.0-flash                       │
│                                                                 │
│   Orchestrates the entire podcast creation workflow             │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    AGENT TOOLS                          │   │
│   │                                                         │   │
│   │   🔍 researcher_agent                                   │   │
│   │      └── Uses Google Search to gather topic facts       │   │
│   │      └── Model: gemini-2.0-flash                        │   │
│   │      └── Tool: google_search (built-in)                 │   │
│   │                                                         │   │
│   │   ✍️  scriptwriter_agent                                │   │
│   │      └── Creates two-speaker dialogue scripts           │   │
│   │      └── Model: gemini-2.0-flash                        │   │
│   │      └── Output: Speaker 1/Speaker 2 format             │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                  FUNCTION TOOLS                         │   │
│   │                                                         │   │
│   │   🔊 generate_tts_audio                                 │   │
│   │      └── Gemini TTS with multi-speaker support          │   │
│   │      └── Model: gemini-2.5-flash-preview-tts            │   │
│   │      └── Voices: Zephyr (Speaker 1), Puck (Speaker 2)   │   │
│   │                                                         │   │
│   │   💾 save_script_to_file                                │   │
│   │      └── Saves script text to disk                      │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌─────────────────────────────────────────┐
              │            📁 output/                   │
              │  └── 20251201-163500_quantum_computing/ │
              │       ├── 20251201-163500_quantum...wav │
              │       └── 20251201-163500_quantum...txt │
              └─────────────────────────────────────────┘
```

### Agent Workflow

```
User Input: "Create a podcast about quantum computing"
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Step 1: RESEARCH                                             │
│ researcher_agent queries Google Search for key facts         │
│ Output: research_summary stored in session state             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Step 2: SCRIPT WRITING                                       │
│ scriptwriter_agent creates engaging two-speaker dialogue     │
│ Output: podcast_script stored in session state               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Step 3: AUDIO GENERATION                                     │
│ generate_tts_audio converts script to multi-voice audio      │
│ Output: WAV file saved to output/ directory                  │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
                     🎧 Complete Podcast!
```

---

## ✅ Features Implemented (Key Concepts from Course)

| Feature                | Implementation            | Description                                      |
| ---------------------- | ------------------------- | ------------------------------------------------ |
| **Multi-agent system** | ✅ 3 agents               | Root agent + 2 specialized sub-agents            |
| **Built-in tools**     | ✅ Google Search          | `google_search` for topic research               |
| **Custom tools**       | ✅ TTS + File Save        | `generate_tts_audio`, `save_script_to_file`      |
| **Sessions & State**   | ✅ InMemorySessionService | `output_key` for state management between agents |
| **Observability**      | ✅ Logging                | Comprehensive logging throughout the pipeline    |

---

## 🛠️ Setup Instructions

### Prerequisites

-   Python 3.10+
-   Google API Key with access to Gemini API

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Abdelbari-Kecita/AI-Podcast-Agent.git
cd AI-Podcast-Agent

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
export GOOGLE_API_KEY="your_api_key_here"
```

### Running the Agent

```bash
# Run the test script
python -m tests.test
```

---

## 📁 Project Structure

```
AI-Podcast-Agent/
├── podcast_producer/              # Main agent package
│   ├── __init__.py               # Package exports
│   ├── agent.py                  # Root agent with AgentTool orchestration
│   ├── config.py                 # Configuration (models, paths, voices)
│   │
│   ├── sub_agents/               # Specialized agents
│   │   ├── __init__.py
│   │   ├── research_agent.py     # Google Search research
│   │   └── script_writer.py      # Two-speaker script creation
│   │
│   └── tools/                    # Custom function tools
│       ├── __init__.py
│       └── tts_tool.py           # Multi-speaker TTS generation
│
├── tests/
│   └── test.py                   # Integration test with Runner
│
├── output/                       # Generated audio files
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🔧 Technical Implementation

### Why AgentTool Pattern?

When using the Gemini API (AI Studio) with Google ADK, combining `sub_agents` with `GoogleSearchTool` causes:

```
Error: "Tool use with function calling is unsupported"
```

**Solution:** Wrap each specialized agent as an `AgentTool`:

```python
from google.adk.tools import AgentTool

researcher_tool = AgentTool(agent=researcher_agent)
scriptwriter_tool = AgentTool(agent=scriptwriter_agent)

root_agent = Agent(
    tools=[researcher_tool, scriptwriter_tool, ...]
)
```

### Multi-Speaker TTS

The TTS tool uses Gemini's multi-speaker capability:

```python
speech_config = SpeechConfig(
    multi_speaker_voice_config=MultiSpeakerVoiceConfig(
        speaker_voice_configs=[
            SpeakerVoiceConfig(speaker="Speaker 1", voice_config=VoiceConfig(prebuilt_voice_config=PrebuiltVoiceConfig(voice_name="Zephyr"))),
            SpeakerVoiceConfig(speaker="Speaker 2", voice_config=VoiceConfig(prebuilt_voice_config=PrebuiltVoiceConfig(voice_name="Puck"))),
        ]
    )
)
```

### Session State Management

Agents share data via `output_key`:

```python
researcher_agent = Agent(
    output_key="research_summary",  # Stored in session state
    ...
)

scriptwriter_agent = Agent(
    output_key="podcast_script",    # Accessible to TTS tool
    ...
)
```

---

## 📦 Dependencies

```
google-adk>=1.19.0      # Google Agent Development Kit
google-genai>=1.52.0    # Google Generative AI SDK
```

---

## 🚀 Value Proposition

| Traditional Podcast             | AI Podcast Producer   |
| ------------------------------- | --------------------- |
| 4-8 hours per episode           | ~5 minutes            |
| Research + Writing + Recording  | Fully automated       |
| Expensive voice talent          | Free multi-voice TTS  |
| Limited by creator availability | Unlimited scalability |

**Use Cases:**

-   Educational content creators scaling their output
-   News summarization in audio format
-   Accessibility: converting written content to audio
-   Rapid prototyping of podcast ideas

---

## 🔮 Future Improvements

-   [ ] Add more voice options and customization
-   [ ] Support longer episodes with chunked TTS
-   [ ] Add background music and sound effects
-   [ ] Deploy to Cloud Run for API access
-   [ ] Add LoopAgent for script revision cycles

---

## 📝 License

MIT License - Free to use and modify.

---

## 👤 Author

**Abdelbari Kecita**  
**Osama Osman**  
Kaggle Agents Intensive Capstone Project  
December 2025

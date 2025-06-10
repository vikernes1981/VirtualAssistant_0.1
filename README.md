# VirtualAssistant

A modular, voice-controlled personal assistant built with Python. It integrates speech recognition, Porcupine wake word detection, GPT-4 for conversation, and system-level command execution. Designed for **Linux** with privacy and offline operation in mind.

## Features

- Wake word detection using Porcupine
- Voice recognition and text-to-speech (TTS) output
- GPT-4 integration for natural conversation
- Modular command routing and fallback handling
- System control: browser, volume, power, applications
- YouTube search and playback
- Voice note dictation to SQLite
- Book/audio playback via YouTube audiobook scraping
- Weather and contextual questions via Wit.ai

## Requirements

### Python

Python 3.11+

Install Python packages:

```bash
pip install -r requirements.txt
```

### System (Linux Only)

Ensure the following are installed (Ubuntu/Debian):

```bash
sudo apt install ffmpeg portaudio19-dev python3-pyaudio vlc python3-dev libffi-dev
```

> Note: This project is not cross-platform. Audio recording, playback, and Porcupine integration are implemented for Linux systems only.

## Project Structure

```
VirtualAssistant/
├── main.py                # Entry point
├── process_commands.py    # Main command dispatcher
├── speech.py              # Audio handling (recording, TTS)
├── gpt_conversation.py    # OpenAI GPT logic
├── wake_word.py           # Wake word detection with Porcupine
├── handle_*.py            # Subcommand handlers
├── youtube.py             # Search + play YouTube videos
├── read_book.py           # Download/play audiobooks from YouTube
├── dictate.py             # Voice note dictation
├── database.py            # SQLite-based storage
├── globals.py             # Shared config (env, audio settings)
├── .env                   # Secrets file (not committed)
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/VirtualAssistant.git
cd VirtualAssistant
```

2. (Optional) Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```ini
OPENAI_API_KEY=your_openai_key
WIT_API_KEY=your_wit_key
```

5. (Optional) Download your `.ppn` wake word file from Picovoice and configure `wake_word.py`.

## Usage

Start the assistant:

```bash
python3 -m main
```

## Notes

- Audio features require a functioning microphone
- Ensure VLC and FFmpeg are installed for YouTube audio playback
- All logic is local-first with minimal external API exposure
- `read_book.py` scrapes audiobook audio from YouTube and plays it using VLC

## License

MIT License

# Story Player App

A Gradio application that allows children to interact with interactive stories through speech.

## Overview

The Story Player App is a service that:
- Plays story content using text-to-speech (Coqui TTS)
- Asks questions to children about the story
- Records and transcribes their answers using speech-to-text (Wav2Vec2)
- Provides feedback on their answers
- Adapts the story flow based on answer correctness

## Installation

This service requires Python 3.9+ and depends on several Bonbon libraries:
- bb-lib-text-to-speech
- bb-lib-speech-to-text  
- bb-lib-story-graph

Install using:

```bash
uv sync --reinstall
```

## Usage

```bash
uv run python app_story_player.py
```

This will start the Gradio web interface at `http://localhost:7860`.


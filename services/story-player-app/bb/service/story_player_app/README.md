# Story Teller App

This service provides an interactive story telling application with speech recognition capabilities.

## Installation

```bash
uv sync --reinstall
```

## Key Components

### StoryPlayer
Contains the `StoryPlayer` class which handles story playback:
- Plays audio for story nodes
- Handles question nodes and answer validation
- Provides feedback on answers
- Manages story progression

### Utils
Contains utility functions for:
- Loading available stories from disk
- Loading story graph files
- Managing story playback state
- Handling audio recording and answer checking

## Features

The app supports:
- Interactive story playback with audio
- Speech recognition for answering questions
- Feedback on correct/incorrect answers 
- Multiple story paths based on answers
- Story progression tracking

## Usage story player app

The app provides a Gradio web interface with:
- Story selection dropdown
- Audio playback controls
- Microphone recording for answers
- Visual feedback and progression

Example usage:
1. Select a story from dropdown
2. Click "Play the story" to begin
3. Listen to story segments
4. Answer questions when prompted
5. Continue through story based on answers

## Dependencies

- Gradio - Web interface
- Story Graph library - Story data structure
- Text-to-Speech - Audio generation
- Speech-to-Text - Answer recognition

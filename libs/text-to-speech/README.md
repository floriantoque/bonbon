# Text to Speech Library

This library provides functionality for generating audio from text using TTS models.

## Key Components

### TTSGlobal
Contains the `TTSGlobal` class which is the base class for text-to-speech functionality:
- Defines interface for loading TTS models
- Defines interface for loading voice cloning models 
- Defines interface for generating audio from text

### TTSCoqui
Contains the `TTSCoqui` class which implements TTS using Coqui models:
- Loads appropriate TTS models based on language
- Loads voice cloning models
- Generates audio files from text
- Supports voice cloning to match target voices

## Usage

The library supports:
- Text-to-speech in multiple languages (French, English)
- Voice cloning to match target speaker voices
- Saving audio output to files

Example usage:
```python
tts = TTSCoqui(language="French")
tts.generate_audio("Bonjour, comment ça va?", "output.wav")
```



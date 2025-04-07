# Speech to Text Library

This library provides a modular interface for converting speech audio to text, with current support for Wav2Vec2 models from Hugging Face.

## Features

- Abstract base class `STT` for implementing different speech-to-text providers
- Built-in implementation for Wav2Vec2 (`STTWav2Vec2`) 
- Support for multiple languages (currently French and English)
- Handles both WAV file and audio array inputs
- Automatic resampling to model's required sample rate

## Installation
To install the package and its dependencies, run:
`uv sync --reinstall`

## Usage

To transcribe a WAV file using the Wav2Vec2 model:
```python
from bb.lib.speech_to_text import STTWav2Vec2

stt = STTWav2Vec2("French")
transcription = stt.transcribe_wav("path/to/your/audio.wav")
print(transcription)
```
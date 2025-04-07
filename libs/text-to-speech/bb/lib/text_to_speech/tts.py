"""Text to Speech Library

This library provides functionality for generating audio from text using TTS models.

## Key Components

### TTSGlobal
Contains the `TTSGlobal` class which is the main class for generating audio from text using TTS models. It handles:
- Loading TTS models
- Loading voice cloning models
- Generating audio from text

### TTSCoqui
Contains the `TTSCoqui` class which is a subclass of `TTSGlobal` for generating audio from text using Coqui TTS models.
"""

import os
import torch
from TTS.api import TTS

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


class TTSGlobal:
    def __init__(self, language: str = "French"):
        self.language = language
        self.model = self._load_model()
        self.vc_model = self._load_voice_cloning_model()

    def _get_model_name(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _get_voice_cloning_model_name(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _load_model(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _load_voice_cloning_model(self):
        raise NotImplementedError("Subclasses must implement this method")

    def generate_audio(self, text: str):
        raise NotImplementedError("Subclasses must implement this method")


class TTSCoqui(TTSGlobal):
    def _get_model_name(self):
        if self.language == "French":
            # return "tts_models/fr/mai/tacotron2-DDC"
            return "tts_models/fra/fairseq/vits"
        if self.language == "English":
            return "tts_models/en/ljspeech/tacotron2-DDC"

    def _get_voice_cloning_model_name(self):
        return (
            "voice_conversion_models/multilingual/multi-dataset/openvoice_v1"
        )

    def _load_model(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = TTS(self._get_model_name(), progress_bar=True).to(device)
        return model

    def _load_voice_cloning_model(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        vc_model = TTS(
            self._get_voice_cloning_model_name(), progress_bar=True
        ).to(device)
        return vc_model

    def generate_audio(self, text: str, output_path: str):
        self.model.tts_to_file(text=text, file_path=output_path)

    def generate_audio_with_voice_cloning(
        self, text: str, output_path: str, speaker_wav: str
    ):
        self.generate_audio(text, output_path)
        self.vc_model.voice_conversion_to_file(
            source_wav=output_path,
            target_wav=speaker_wav,
            file_path=output_path.replace(".wav", "_vc.wav"),
        )


class TTSElevenLabs(TTSGlobal):
    def __init__(self, language: str = "French"):
        super().__init__(language)

    def _load_model(self):
        load_dotenv()
        api_key = os.getenv("ELEVENLABS_API_KEY")
        model = ElevenLabs(api_key=api_key)
        return model

    def _load_voice_cloning_model(self):
        return None

    def generate_audio(self, text: str, output_path: str):
        audio = self.model.text_to_speech.convert(
            text=text,
            model_id="eleven_multilingual_v2",
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            output_format="mp3_44100_64",
        )
        with open(output_path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)


def get_tts_model(model_name: str) -> TTSGlobal:
    if model_name == "TTSCoqui":
        return TTSCoqui
    elif model_name == "TTSElevenLabs":
        return TTSElevenLabs
    else:
        raise ValueError(f"Invalid model name: {model_name}")

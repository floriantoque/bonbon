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

import torch
from TTS.api import TTS


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
        return "voice_conversion_models/multilingual/multi-dataset/openvoice_v1"

    def _load_model(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = TTS(self._get_model_name(), progress_bar=True).to(device)
        return model

    def _load_voice_cloning_model(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        vc_model = TTS(self._get_voice_cloning_model_name(), progress_bar=True).to(
            device
        )
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

"""Speech to text module for converting audio to text using various models.

This module provides classes for speech-to-text conversion using different models
like Wav2Vec2 from Hugging Face transformers library. It supports multiple languages
and audio formats.
"""

import librosa
import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor


class STT:
    def __init__(self, language: str):
        self.language = language
        self.model_id = self._get_model_id()
        self.processor = self._load_processor()
        self.model = self._load_model()

    def _get_model_id(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _load_processor(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _load_model(self):
        raise NotImplementedError("Subclasses must implement this method")

    def transcribe_wav(self, wav_path: str) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def transcribe_audio(self, audio: np.ndarray, sampling_rate: int) -> str:
        raise NotImplementedError("Subclasses must implement this method")


class STTWav2Vec2(STT):
    """Speech to text using Wav2Vec2 model.

    This class implements speech-to-text conversion using the Wav2Vec2 model
    from Hugging Face. It supports multiple languages and audio formats.

    Attributes:
        model (Wav2Vec2ForCTC): The Wav2Vec2 model for speech recognition.
        processor (Wav2Vec2Processor): The processor for audio preprocessing.
    """

    def __init__(self, language: str = "French"):
        """Initialize the STT model.

        Parameters
        ----------
        language (str): Language of the model.
            Defaults to "French".
        """
        super().__init__(language)
        self.model_sampling_rate = 16000

    def _get_model_id(self):
        if self.language == "French":
            model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-french"
        elif self.language == "English":
            model_id = "jonatasgrosman/wav2vec2-large-english"
        else:
            raise ValueError(f"Language {self.language} not supported")

        return model_id

    def _load_processor(self):
        return Wav2Vec2Processor.from_pretrained(self.model_id)

    def _load_model(self):
        return Wav2Vec2ForCTC.from_pretrained(self.model_id)

    def transcribe_wav(self, wav_path: str) -> str:
        """Transcribe a WAV file to text.

        Parameters
        ----------
        wav_path (str): Path to the WAV file.

        Returns:
            str: Transcribed text from the WAV file.
        """
        audio, sampling_rate = librosa.load(wav_path, sr=self.model_sampling_rate)

        input_values = self.processor(
            audio, sampling_rate=sampling_rate, return_tensors="pt"
        ).input_values

        with torch.no_grad():
            logits = self.model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.decode(predicted_ids[0])
        return transcription

    def transcribe_audio(self, audio: np.ndarray, sampling_rate: int) -> str:
        """Transcribe audio array to text.

        Parameters
        ----------
        audio (np.ndarray): Audio data as a numpy array.
        sampling_rate (int): Sampling rate of the audio in Hz.

        Returns
        -------
        str: Transcribed text from the audio.
        """
        if isinstance(audio, np.ndarray) and audio.dtype != np.float64:
            audio = audio.astype(np.float64)

        audio = librosa.resample(
            audio, orig_sr=sampling_rate, target_sr=self.model_sampling_rate
        )
        input_values = self.processor(
            audio, sampling_rate=self.model_sampling_rate, return_tensors="pt"
        ).input_values

        with torch.no_grad():
            logits = self.model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.decode(predicted_ids[0])
        return transcription

import os
from pathlib import Path

from bb.lib.text_to_speech import get_tts_model


def main():
    workspace_data = Path(os.environ.get("BONBON_WORKSPACE_DATA"))
    text = """
        Aujourd'hui, nous allons vous raconter une histoire amusante sur Mickey et Donald."""

    print("Generating audio with Coqui TTS...")
    tts_model = get_tts_model("TTSCoqui")
    tts = tts_model(language="French")
    tts.generate_audio(
        text=text,
        output_path=workspace_data / "output.wav",
    )

    print("Generating audio with ElevenLabs...")
    tts_model = get_tts_model("TTSElevenLabs")
    tts = tts_model(language="French")
    tts.generate_audio(
        text=text,
        output_path=workspace_data / "output_elevenlabs.wav",
    )


if __name__ == "__main__":
    main()

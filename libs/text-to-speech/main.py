import os
from pathlib import Path

from bb.lib.text_to_speech import TTSCoqui


def main():
    workspace_data = Path(os.environ.get("BONBON_WORKSPACE_DATA"))
    text = """
        Aujourd'hui, nous allons vous raconter une histoire amusante sur Mickey et Donald."""
    tts = TTSCoqui(language="French")
    tts.generate_audio(
        text=text,
        output_path=workspace_data / "output.wav",
    )


if __name__ == "__main__":
    main()

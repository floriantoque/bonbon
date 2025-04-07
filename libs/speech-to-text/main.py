import os
import time
from pathlib import Path

from bb.lib.speech_to_text.stt import STTWav2Vec2


def main():
    workspace_data = Path(os.environ.get("BONBON_WORKSPACE_DATA"))
    wav_path = workspace_data / "moi_fr_normal.wav"
    language = "French"

    # Test of the STTWav2Vec2 class
    stt = STTWav2Vec2(language)
    transcription = stt.transcribe_wav(wav_path)
    print(f"Transcription de STTWav2Vec2: {transcription}")

    # Test of the STTWav2Vec2 class speed
    times = []
    for i in range(10):
        start_time = time.time()
        transcription = stt.transcribe_wav(wav_path)
        end_time = time.time()
        execution_time = end_time - start_time
        times.append(execution_time)
    print(f"STTWav2Vec2 average time taken: {sum(times) / len(times)} seconds")


if __name__ == "__main__":
    main()

from pathlib import Path
import edge_tts


async def generate_audio(text, destination_path, rate="-15%"):
    Path(destination_path).parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text, "zh-TW-YunJheNeural", rate = rate)
    await communicate.save(destination_path)
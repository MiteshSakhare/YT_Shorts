#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
#  KOKORO_WORKER.PY — Persistent Kokoro synthesis worker
#  Keeps the model loaded once to avoid per-segment startup timeouts
# ═══════════════════════════════════════════════════════════════

import json
import sys
import traceback

import numpy as np
import soundfile as sf
from kokoro import KPipeline


def synthesize(text: str, voice: str, speed: float, output_path: str) -> float:
    pipeline = synthesize.pipeline
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=r"\n+")

    full_audio = []
    for _, _, audio in generator:
        if audio is not None:
            full_audio.append(audio)

    if not full_audio:
        raise RuntimeError("Kokoro generated empty audio")

    final_audio = np.concatenate(full_audio)
    sample_rate = 24000
    sf.write(output_path, final_audio, sample_rate)
    return len(final_audio) / sample_rate


def main() -> None:
    synthesize.pipeline = KPipeline(lang_code="a")

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue

        try:
            payload = json.loads(line)
            if payload.get("action") != "synthesize":
                raise ValueError("Unsupported action")

            duration = synthesize(
                text=payload["text"],
                voice=payload["voice"],
                speed=float(payload["speed"]),
                output_path=payload["output_path"],
            )
            print(json.dumps({"status": "ok", "duration": duration}), flush=True)
        except Exception as exc:
            traceback.print_exc(file=sys.stderr)
            print(json.dumps({"status": "error", "error": str(exc)}), flush=True)


if __name__ == "__main__":
    main()
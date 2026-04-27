# 🎬 YouTube Shorts Generator — Snippet Stories

Automated YouTube Short generator for **"The Twice-Crowned King"** dark fantasy series.

## Project Structure

```
YT/
├── src/                          # Core pipeline source code
│   ├── __init__.py               # Package init
│   ├── generate_short.py         # ★ Main pipeline orchestrator
│   ├── config.py                 # All configuration & tuning knobs
│   ├── background_engine.py      # Pexels API + procedural backgrounds
│   ├── sfx_engine.py             # Mood-based sound effect generation
│   ├── mood_detector.py          # Keyword-based mood classification
│   ├── audio_processor.py        # Character FX, normalization, ducking
│   ├── subtitle_sync.py          # Frame-perfect ASS subtitle sync
│   ├── local_tts.py              # Kokoro TTS integration (emotional voices)
│   ├── kokoro_worker.py          # Persistent Kokoro model worker
│   ├── psychology_engine.py      # Hook selection & algorithm optimization
│   └── error_handler.py          # Error handling utilities
│
├── tools/                        # Utility & batch scripts
│   ├── batch_generate.py         # Generate all parts in sequence
│   ├── split_story.py            # Split DOCX → input parts
│   ├── hook_rewriter.py          # AI hook rewriter (Ollama)
│   ├── verify_dependencies.py    # Dependency checker
│   └── verify_system.py          # System verification
│
├── assets/                       # Brand assets
│   ├── watermark.png             # Channel watermark overlay
│   ├── banner.png                # YouTube banner
│   └── profile.png               # Channel profile photo
│
├── input/                        # Script input files (part_0001.txt, ...)
├── output/                       # Generated videos & metadata
├── sfx/                          # Generated sound effects cache
├── story/                        # Source DOCX story file
├── docs/                         # Documentation & original assets
├── .temp/                        # Temporary processing files
├── .cache/                       # Pexels video cache
└── requirements.txt              # Python dependencies
```

## Quick Start

### 1. Setup
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Split Story (if starting from DOCX)
```bash
python tools/split_story.py
```

### 3. Generate One Video
```bash
python src/generate_short.py input/part_0001.txt
```

### 4. Batch Generate
```bash
python tools/batch_generate.py
python tools/batch_generate.py --start 10 --end 20  # Range mode
```

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| **2-Pass Render** | ✅ | Separate video+subs pass from audio mix (faster, debuggable) |
| **Natural Subtitles** | ✅ | Punctuation-aware chunking (no mid-sentence breaks) |
| **Kokoro TTS** | ✅ | Emotional local TTS with character voice mapping |
| **SFX Integration** | ✅ | Mood-based SFX placed on timeline at 25/50/75% marks |
| **Visual Branding** | ✅ | Persistent watermark + CTA overlay + Part tag |
| **Loop Bridge** | ✅ | Echo opening audio at end → triggers replays |
| **Smart Backgrounds** | ✅ | Fuzzy location keyword matching for scene-aware Pexels clips |
| **Progress Bar** | ✅ | Red progress indicator at bottom of video |
| **Auto-Ducking** | ✅ | Music volume drops during speech |
| **AI Disclosure** | ✅ | YouTube 2026 policy compliant overlay |

## Branding Strategy

> **No spoken intros/outros** — they kill retention on Shorts.

Instead, branding is 100% visual:
- **Watermark**: Channel logo in top-left corner (persistent, 70% opacity)
- **Part Tag**: "Part N" text in first 4 seconds
- **CTA Overlay**: "Like & Subscribe for Part N+1!" during final 3 seconds
- **Loop Bridge**: Audio loops seamlessly for re-watches

## Configuration

All settings are in [`src/config.py`](src/config.py). Key knobs:

```python
# TTS
USE_LOCAL_TTS = True       # Use Kokoro (emotional) vs Edge-TTS (flat)

# Visual Branding
SHOW_CHANNEL_WATERMARK = True
SHOW_CTA_OVERLAY = True
SHOW_PART_TAG = True

# Audio
MOOD_SFX_ENABLED = True    # Layer mood SFX on timeline
MUSIC_VOLUME = 0.10        # Background music level

# Duration
MAX_DURATION = 59          # YouTube Shorts limit
TARGET_DURATION = 50       # Sweet spot for algorithm
```

## Dependencies

- **FFmpeg** (required): Video/audio processing
- **Python 3.10+**: Core runtime
- **Kokoro** (optional): Local emotional TTS (install in `.kokoro_venv`)
- **Pexels API Key**: Background video footage (set in `.env`)

# 🎬 YouTube Shorts Generator
**The Twice-Crowned King** — AI-Generated Dark Fantasy Series  
*Status: ✅ Production Ready | Channel: Snippet Stories | Total Videos: 225 | v2.1 – Optimized*

---

## 🚀 **QUICK START (5 MINUTES)**

```powershell
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Generate single test video (verify system works)
python src/generate_short.py input/part_0001.txt 1

# 3. Generate all 225 videos (batch mode with resume)
python batch_generate.py

# 4. Generate specific range
python batch_generate.py --start 50 --end 100

# 5. Resume interrupted batch
python batch_generate.py --resume
```

**Expected Time:** 
- Single video: ~2 minutes
- All 225 videos: ~7-8 hours (batch mode, resumable)
- Output: 225 YouTube Shorts ready to upload

---

## 📖 COMPLETE DOCUMENTATION

👉 **[Full Guide → docs/INDEX.md](docs/INDEX.md)**  
👉 **[Setup Instructions → docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)**  
👉 **[View All Guides](docs/)**

---

## 📂 Project Structure

```
YT/
├── src/
│   ├── generate_short.py       # Main video generation pipeline
│   ├── batch_generate.py      # Batch processing with resume (NEW)
│   ├── config.py               # System configuration
│   ├── mood_detector.py        # AI mood analysis
│   ├── background_engine.py    # Pexels integration
│   ├── audio_processor.py      # Character FX & normalization
│   ├── sfx_engine.py           # Sound effects generation
│   └── test_edge.py            # Test utilities
│
├── input/                      # 225 story script segments (auto-split)
├── output/                     # Generated videos & metadata
│   ├── short_part_XX.mp4       # Final video (loop + AI label optional)
│   ├── thumbnail_part_XX.png   # YouTube thumbnail (1280×720)
│   ├── metadata_part_XX.json   # Upload metadata
│   └── batch_progress_*.json   # Batch resume checkpoint
│
├── docs/                       # Complete documentation
│   ├── INDEX.md               # Documentation index (START HERE)
│   ├── GETTING_STARTED.md     # Setup & installation
│   ├── QUICK_REFERENCE.md     # Command cheatsheet
│   ├── ADVANCED_TIPS.md       # Customization guide
│   └── YOUTUBE_SETUP_GUIDE.md # Upload walkthrough
│
├── .env                        # Secrets (API keys) – NOT in git
├── .gitignore                  # Ignores .env and build artifacts
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── venv/                       # Virtual environment
```

---

## ✨ Key Features

### Performance & Architecture
✅ **Parallel TTS generation** – 75-80% faster audio rendering  
✅ **Batch resume capability** – Save/resume interrupted sessions  
✅ **Error validation** – Input checks, timeout protection, detailed logging  
✅ **Music variety** – Harmonic synthesis with mood-based variations  

### Quality & Format
✅ **22-voice character system** with consistent personality memory  
✅ **Frame-perfect subtitle sync** (±50ms accuracy, per-character colors)  
✅ **Professional composition** (1080×1920, H.264 Main Profile, 30fps)  
✅ **YouTube-optimized** metadata & AI disclosure labels (2026 compliant)  

### Creative Features
✅ **Mood detection** (Epic, Dark, Happy, Thrilling, etc.)  
✅ **Pexels Tier 2 backgrounds** – Stock footage auto-selected by mood  
✅ **Procedural music generation** – Harmonic synthesis with dynamics  
✅ **Hook overlays & thumbnails** – Viral-optimized card design  
✅ **Loop transitions** – +15% replay boost via seamless looping  
✅ **SFX layers** – Mood-specific sound effects per scene  

### Reliability & Automation
✅ **Batch generation** – All 225 videos with automatic error recovery  
✅ **Resume from checkpoint** – Never lose progress on failed batches  
✅ **Progress tracking** – JSON files show completion/failure history  
✅ **Timeout protection** – 10-minute safety limit per video  

---

## 📚 Documentation & Guides

| Guide | Purpose | Read Time |
|-------|---------|-----------|
| **[INDEX.md](docs/INDEX.md)** | 📍 Start here – Overview & quick links | 5 min |
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | Installation, config, first video | 10 min |
| [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) | Command cheatsheet & shell scripts | 5 min |
| [ADVANCED_TIPS.md](docs/ADVANCED_TIPS.md) | Customization: voices, moods, music | 15 min |
| [YOUTUBE_SETUP_GUIDE.md](docs/YOUTUBE_SETUP_GUIDE.md) | Upload, scheduling, channel setup | 10 min |
| [SYSTEM_REFINEMENT_REPORT.md](docs/SYSTEM_REFINEMENT_REPORT.md) | Technical architecture & optimizations | 20 min |
| [PROJECT_COMPLETE.md](docs/PROJECT_COMPLETE.md) | Full project status & features | 15 min |

---

## 🛠️ System Requirements

| Component | Requirement | Why |
|-----------|-------------|-----|
| Python | 3.8+ | Async/await, f-strings |
| FFmpeg | Latest | Video encoding, composition |
| Edge-TTS | Auto-installed | Microsoft TTS voices |
| Internet | Required | TTS API calls, Pexels API |
| RAM | 8GB+ | Parallel TTS generation |
| Disk Space | ~10GB | 225 videos × ~25MB each |

**Setup time:** ~5 minutes  
**Dependencies installed via:** `pip install -r requirements.txt`

---

## � Getting Started

### Step 1: Setup (First Time Only)
```powershell
# Clone/navigate to project
cd YT

# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure
```powershell
# Edit config.py with your settings:
# - CHANNEL_NAME, STORY_TITLE, VOICES, MUSIC_MODE, etc.
# - Copy Pexels API key to .env file

# Verify system is ready
python src/generate_short.py input/part_0001.txt 1
```

### Step 3: Generate
```powershell
# Single video (test):
python src/generate_short.py input/part_XXXX.txt N

# All videos (batch mode with resume):
python batch_generate.py

# Resume if interrupted:
python batch_generate.py --resume
```

### Step 4: Upload
- Videos ready in `output/short_part_XX_looped.mp4`
- Thumbnails in `output/thumbnail_part_XX.png`
- Metadata in `output/metadata_part_XX.json`
- See [YOUTUBE_SETUP_GUIDE.md](docs/YOUTUBE_SETUP_GUIDE.md)

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **FFmpeg not found** | Ensure FFmpeg is in PATH: `ffmpeg -version` |
| **TTS fails** | Check internet connection for Edge-TTS API |
| **Pexels API error** | Verify API key in `.env` file (not in `config.py`) |
| **Memory issues** | Reduce parallel TTS: set `PARALLEL_TTS_WORKERS = 2` in config.py |
| **Video encoding timeout** | Videos >2min: increase timeout in `config.py` `VIDEO_TIMEOUT` |
| **Batch interrupted** | Resume with session ID: `python batch_generate.py --resume` |

For complete troubleshooting: See [docs/INDEX.md](docs/INDEX.md) FAQ

---

## 💡 Common Commands

```powershell
# Activate environment (run every session)
.\venv\Scripts\Activate.ps1

# Test single video
python src/generate_short.py input/part_0001.txt 1

# Generate videos 1-50
python batch_generate.py --start 1 --end 50

# Generate videos 100-150 (specific range)
python batch_generate.py --start 100 --end 150

# Resume batch from checkpoint
python batch_generate.py --resume

# Batch with stop-on-error (tight testing)
python batch_generate.py --error-handling stop

# List completed batches
ls output/batch_progress_*.json
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Parallel TTS speed | 3-5 sec for 8 segments |
| Single video generation | ~2 minutes (varies with BG) |
| Full batch (225 videos) | ~7-8 hours on single machine |
| Audio/subtitle sync | ±50ms (frame-perfect) |
| Video file size | ~24-35 MB per video |
| Total batch storage | ~6-8 GB |

---

## ✉️ Support & Contact

- **Issues?** Check [docs/INDEX.md](docs/INDEX.md) FAQ
- **Configuration?** See [docs/ADVANCED_TIPS.md](docs/ADVANCED_TIPS.md)
- **Upload help?** Follow [docs/YOUTUBE_SETUP_GUIDE.md](docs/YOUTUBE_SETUP_GUIDE.md)
- **System details?** Read [docs/SYSTEM_REFINEMENT_REPORT.md](docs/SYSTEM_REFINEMENT_REPORT.md)

---

*Status: ✅ Production Ready | Version: 2.1 – Optimized Pipeline | Last Updated: April 12, 2026*

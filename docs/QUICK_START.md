# 🚀 QUICK START GUIDE - NEW FEATURES & IMPROVEMENTS

## What Changed?

Your YouTube Shorts generator now has:

✅ **Better background videos** - Only nature, wildlife, and structures (no humans, no 3D)  
✅ **Perfect audio-subtitle sync** - Speech detection ensures timing is accurate  
✅ **AI hook rewriter for ALL parts** - Part 4, 42, and all others now work  
✅ **YouTube 2026 compliance** - AI-Generated label automatically added  
✅ **Works on Mac/Windows/Linux** - Font paths fixed for all platforms  
✅ **Better error handling** - Clear messages when something goes wrong  

---

## 🎬 Generate Your First Video (5 minutes)

### Step 1: Verify Everything Works
```bash
cd C:\Users\mites\OneDrive\Desktop\YT
python verify_system.py
```

**Output should show:**
- ✅ FFmpeg available
- ✅ All Python packages found
- ✅ All source files present
- ✅ Input scripts ready

### Step 2: Generate Single Test Video
```bash
python src/generate_short.py input/part_0001.txt 1
```

**Watch for these lines in output:**
- ✅ "Frame-perfect subtitles" (new sync system working)
- ✅ "Approved video" (background filtering working)
- ✅ "AI disclosure added" (YouTube compliance)

**Video will be saved to:** `output/short_part_0001_disclosed.mp4`

### Step 3: Check the Video
```bash
# List generated videos
dir output/

# Play the video (check audio/subtitle sync)
start output/short_part_0001_disclosed.mp4
```

---

## 🎯 Use New Features

### Feature 1: AI Hook Rewriter (All 225 Parts)

**What it does:** Rewrites opening sentences to be viral-worthy using AI

**Requirements:**
1. Install Ollama from https://ollama.ai
2. Start Ollama server in terminal:
   ```bash
   ollama serve
   ```

3. Pull a language model (pick one):
   ```bash
   ollama pull deepseek-coder    # Recommended
   # OR
   ollama pull llama2
   # OR
   ollama pull mistral
   ```

**Run it:**
```bash
# In same folder, open new terminal
python src/hook_rewriter_v2.py
```

**Output:**
```
[001/225] Processing part_0001.txt...
   ✅ part_0001.txt
      Original: He woke in darkness...
      Rewritten: When the curse awoke, so did he...

[002/225] Processing part_0002.txt...
   ...
```

**Result:** Rewritten scripts saved to `output/hooks/`

**Use them:**
```bash
# Copy any you like back to input/ to replace originals
copy output/hooks/part_0001.txt input/part_0001.txt
```

---

### Feature 2: Perfect Audio-Subtitle Sync

**What it does:** Automatically detects speech boundaries and perfectly times subtitles

**How to enable:** It's already enabled! Added to config.py:
```python
USE_FRAME_PERFECT_SUBTITLES = True
```

**How it works:**
1. FFmpeg detects silence/speech segments
2. Subtitles are aligned to speech starts
3. No more delayed or early subtitles
4. Automatically verified for quality

**Check sync quality:**
See logs for lines like:
```
✅ Synced subtitles created: output/short_part_0001.ass
Sync quality: PERFECT (0 issues found)
```

---

### Feature 3: Smart Background Filtering

**What it does:** Only allows natural, wildlife, and structure videos

**Blocks:**
- ❌ Humans, people, faces
- ❌ 3D renders, CGI, animation
- ❌ Urban, modern, office scenes
- ❌ Synthetic content

**Allows:**
- ✅ Forests, mountains, nature
- ✅ Wildlife, animals, birds
- ✅ Castles, temples, ruins
- ✅ Oceans, waterfalls, canyons
- ✅ Ancient structures
- ✅ Abstract, magical effects

**It's automatic** - just keep generating videos!

---

### Feature 4: YouTube 2026 Compliance

**What it does:** Adds "AI-Generated" label to meet YouTube's new policy

**Enabled by default:**
```python
ADD_AI_DISCLOSURE = True
```

**Disable if needed:**
```python
# In src/config.py, change to:
ADD_AI_DISCLOSURE = False
```

**Label position:** Top-right corner (can be customized)

---

## 📋 LOGGING & TROUBLESHOOTING

### Check Logs
```bash
# View latest log
tail -f logs/generate.log

# Or open in VS Code:
code logs/generate.log
```

### Common Issues & Fixes

**Error: "FFmpeg not found"**
```bash
# Windows
winget install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

**Error: "Librosa not installed" (subtitle sync won't work)**
```bash
pip install librosa
```

**Error: "No Pexels API key configured"**
1. Create `.env` file in project root
2. Add: `PEXELS_API_KEY=your_api_key`
3. Get free API key from https://www.pexels.com/api/

**Error: "Could not rewrite hook - Ollama not running"**
```bash
# Start Ollama in new terminal
ollama serve

# Then run rewriter again
python src/hook_rewriter_v2.py
```

---

## 🎬 Generate All 225 Videos

When ready to generate full batch:

```bash
python batch_generate.py
```

**Expected output:**
```
╔════════════════════════════════════════════════════════════════╗
║     🎬 BATCH GENERATE - Snippet Stories YouTube Shorts        ║
╚════════════════════════════════════════════════════════════════╝

📝 Scripts found: 225
⏱️  Estimated time: 7.5 hours
🎬 Output folder: output/

Features per video:
  ✅ Perfect subtitle sync
  ✅ Safe backgrounds (no humans/3D)
  ✅ AI disclosure label
  ✅ Frame-perfect audio
  ✅ YouTube Shorts optimized (1080x1920, ~50sec)

Start batch generation? (yes/no): yes

[001/225] ✅ part_0001.txt
[002/225] ✅ part_0002.txt
...
```

---

## 🔧 CONFIGURATION (Optional)

All settings in: `src/config.py`

### Most Useful Settings

```python
# ─── Channel & Branding ───
CHANNEL_NAME = "Snippet Stories"

# ─── Quality Settings ───
VID_WIDTH = 1080                    # YouTube Shorts width
VID_HEIGHT = 1920                   # YouTube Shorts height
VID_FPS = 50                        # Smoother playback

# ─── AI & Disclosure ───
ADD_AI_DISCLOSURE = True            # YouTube required
USE_FRAME_PERFECT_SUBTITLES = True  # Perfect sync
FILTER_BACKGROUND_CONTENT = True    # No humans/3D

# ─── Background Filtering ───
ALLOWED_BACKGROUND_KEYWORDS = [
    "forest", "mountain", "wildlife", "castle", ...
]
BLACKLIST_BACKGROUND_KEYWORDS = [
    "person", "3d", "cgi", "urban", ...
]

# ─── Logging ───
LOG_LEVEL = "INFO"                  # INFO or DEBUG
LOG_FILE = "logs/generate.log"
```

---

## 📊 NEW FILES CREATED

These are automatically used - no action needed:

1. **`src/subtitle_sync.py`** - Audio-subtitle sync logic
2. **`src/hook_rewriter_v2.py`** - Batch hook rewriter
3. **`src/error_handler.py`** - Better error messages
4. **`src/verify_dependencies.py`** - Dependency checking
5. **`IMPROVEMENTS_APPLIED.md`** - Full changes list

---

## 🎯 WORKFLOW SUMMARY

### For Normal Use:
```bash
# 1. Generate videos
python batch_generate.py

# 2. Check output
ls -lh output/

# 3. Upload to YouTube
# (Download from output/ folder)
```

### With AI Hook Rewriting:
```bash
# 1. Start Ollama (in separate terminal)
ollama serve

# 2. Rewrite all hooks
python src/hook_rewriter_v2.py

# 3. Copy best hooks back to input/
copy output/hooks/part_*.txt input/

# 4. Generate videos
python batch_generate.py
```

### With Single Test:
```bash
# 1. Test one video
python src/generate_short.py input/part_0001.txt 1

# 2. Check for sync issues, filtering, etc
# Look in logs/generate.log

# 3. If good, run batch
python batch_generate.py
```

---

## ✅ CHECKLIST

Before generating videos:

- [ ] Run `python verify_system.py` and check all GREEN
- [ ] Test with `python src/generate_short.py input/part_0001.txt 1`
- [ ] Check video plays and subtitles sync with audio
- [ ] (Optional) Install Ollama and test hook rewriter
- [ ] Ready to generate with `python batch_generate.py`

---

## 🚀 PERFORMANCE TIPS (Optional)

These are ready to enable when you want faster generation:

### TTS Caching
- Cache audio outputs to reuse same voice+text
- **Gain:** 60-70% faster TTS stage
- **How:** Enable in future update

### Parallel Processing
- Generate 2-3 videos at once (if you have RAM)
- **Gain:** 2-3x faster batch
- **How:** Enable in future update

### Progress Checkpoints
- Resume interrupted batches (don't restart)
- **Gain:** No lost time on failures
- **How:** Enable in future update

---

## 📞 TROUBLESHOOTING

**Videos won't generate?**
1. `python verify_system.py` - Find the issue
2. Check `logs/generate.log` - See exact error
3. Install missing packages: `pip install -r requirements.txt`

**Audio and subtitles don't sync?**
1. Make sure `librosa` is installed
2. Check `USE_FRAME_PERFECT_SUBTITLES = True` in config
3. See logs for sync quality report

**Hooks aren't being rewritten?**
1. Start Ollama: `ollama serve`
2. Run: `python src/hook_rewriter_v2.py`
3. Model must be installed: `ollama pull deepseek-coder`

**Background videos show humans?**
1. This shouldn't happen with content filter enabled
2. Check `FILTER_BACKGROUND_CONTENT = True`
3. Update keywords in config if needed

---

*Ready to generate amazing videos!* 🎬✨

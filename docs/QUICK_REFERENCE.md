# ⚡ QUICK REFERENCE - SNIPPET STORIES SETUP

**Channel**: Snippet Stories  
**Status**: 🟢 Production Ready (April 12, 2026)  
**Videos**: 225 YouTube Shorts ready to generate
**System**: ✅ All tests passed, fully refined

---

## 🎯 QUICK START COMMANDS (April 12 Updated)

### Test Single Video (Recommended First)
```bash
# Test one video to verify everything works
python src/generate_short.py input/part_0001.txt 1
# Output: output/short_part_01_looped.mp4 (106.5s)
# Time: ~2 minutes
```

### Generate All 225 Videos (Production)
```bash
# Generate all 225 videos with resume capability
python batch_generate.py
# Estimated time: 7-8 hours
# Can pause and resume: python batch_generate.py --resume
```

### Generate Specific Range
```bash
# Generate videos 1-50
python batch_generate.py --start 1 --end 50

# Generate videos 100-150
python batch_generate.py --start 100 --end 150
```

---

## 📋 OUTPUT FILES (What You'll Get)

For each video generated:
```
output/
├── short_part_01_looped.mp4    ✅ FINAL VIDEO (use this!)
├── thumbnail_part_01.png        ✅ YouTube thumbnail (1280×720)
├── metadata_part_01.json        ✅ Upload metadata
└── part_01/
    ├── subs.ass                 📝 Subtitles (frame-perfect)
    ├── hook.png                 🎨 Hook overlay image
    └── ...
```

**Use**: `short_part_XX_looped.mp4` (includes all features)

---

## 🚀 COMMON QUESTIONS (April 12 Updated)

---

## ⚙️ KEY CONFIGURATION OPTIONS (in src/config.py)

| Setting | Current | Options |
|---------|---------|---------|
| Video Resolution | 1080×1920 | YouTube Shorts standard |
| FPS | 30 | 24, 30 (recommended), 60 |
| Duration Mode | unlimited | unlimited, short, medium |
| Mood Detection | enabled | true/false |
| Mood SFX | enabled | true/false |
| Character FX | enabled | true/false |
| Loop Bridge | enabled | true/false |
| Loop Transition | enabled | true/false |
| AI Watermark | enabled | true/false |
| Background Source | Pexels | "pexels" (mood-matched) |
| Music Generation | enabled | generate new each time |
| Video Quality | CRF 20 | 18 (best) to 28 (smallest) |

---

## 📏 FILE QUICK REFERENCE

| File | Purpose | Status |
|------|---------|--------|
| `src/config.py` | All settings | ✅ UPDATED |
| `src/generate_short.py` | Video generator | ✅ UPDATED |
| `batch_generate.py` | Batch 214 videos | ✅ NEW |
| `CHANNEL_SETUP_COMPLETE.md` | Setup guide | ✅ NEW |
| `SNIPPET_STORIES_READY.md` | Full details | ✅ NEW |

---

## 🎬 VIDEO OUTPUT EXPLAINED

```
AFTER RUNNING: python src/generate_short.py input/part_01_01.txt

output/
├── short_part_01.mp4              ❌ Skip this (no watermark)
├── short_part_01_disclosed.mp4    ✅ USE THIS (has watermark!)
└── short_part_01_looped.mp4       ⚠️ Optional (experimental loop)
```

**Rule**: Always use `*_disclosed.mp4`

---

## 📊 BATCH GENERATION TIMELINE

```
Start:    python batch_generate.py
Progress: [001/214] ✅ part_01_01.txt
Progress: [002/214] ✅ part_01_02.txt
Progress: [003/214] ✅ part_01_03.txt
...
Progress: [214/214] ✅ part_24_10.txt

Estimated: 7-10 hours
Result: 214 × short_part_XX_YY_disclosed.mp4
```

---

## ✨ CUSTOMIZE YOUR WATERMARK

### Move to Different Corner
```python
# In src/config.py
AI_DISCLOSURE_POSITION = "bottom-left"   # New position
```

### Make More/Less Transparent
```python
# Make very visible (100%)
AI_DISCLOSURE_OPACITY = 1.0

# Make subtle (30%)
AI_DISCLOSURE_OPACITY = 0.3
```

### Disable Temporarily (Not recommended)
```python
# Remove watermark (for testing)
ADD_AI_DISCLOSURE = False
```

---

## 🎯 BEFORE UPLOADING

### Verify Checklist
- [ ] Watch sample video: `short_part_01_disclosed.mp4`
- [ ] Watermark visible? (Should see "Snippet Stories" top-right)
- [ ] Audio quality good?
- [ ] Subtitles in sync?
- [ ] ~50 seconds duration?
- [ ] Plays smoothly on mobile?

### If Something's Wrong
1. Check `src/config.py` settings
2. Re-generate one test video
3. Verify again
4. Adjust if needed
5. Run batch generation

---

## 📱 YOUTUBE SHORTS SPECS (What You Get)

✅ **Format**: 1080×1920 vertical  
✅ **Duration**: ~50 seconds  
✅ **FPS**: 30 frames per second  
✅ **Codec**: H.264 (YouTube standard)  
✅ **Audio**: AAC, 192k bitrate, -14 LUFS  
✅ **Subtitles**: Frame-perfect timing  
✅ **Watermark**: "Snippet Stories" branded  
✅ **Compliance**: YouTube 2026 AI disclosure ready  

---

## 🚀 EXACT COMMANDS TO RUN

### Test One Video
```bash
python src/generate_short.py input/part_01_01.txt
```

### Generate All 214
```bash
python batch_generate.py
```

### Check Progress
```bash
dir output\*disclosed.mp4 | measure-object -line
```

### List All Generated Videos
```bash
dir output\*disclosed.mp4
```

---

## 🎁 YOU NOW HAVE

✅ **Snippet Stories** channel branding  
✅ **214 ready-to-generate** video scripts  
✅ **Professional watermark** with channel name  
✅ **Batch generation** system  
✅ **YouTube 2026** compliance built-in  
✅ **Complete documentation** for customization  
✅ **Production-ready** system  

---

## 👉 NEXT: 3 STEPS

```
Step 1: python src/generate_short.py input/part_01_01.txt
        ↓ (verify watermark looks good)
        
Step 2: Review: output/short_part_01_disclosed.mp4
        ↓ (confirm quality, watermark visibility)
        
Step 3: python batch_generate.py
        ↓ (run overnight, wake up with 214 videos!)
        
Result: 214 × short_part_XX_YY_disclosed.mp4
        Ready to upload to YouTube!
```

---

**Status**: 🟢 Ready to Generate  
**Channel**: Snippet Stories  
**Next**: `python batch_generate.py`

from typing import List, Dict, Optional
#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
#  BACKGROUND_ENGINE.PY — Multi-Tier Background Video System
#  Tier 1: FFmpeg procedural animations (works everywhere)
#  Tier 2: Pexels stock footage (free API)
#  Tier 3: ComfyUI AI generation (future)
# ═══════════════════════════════════════════════════════════════

import subprocess
import os
import sys
import json
import hashlib
import logging
import random
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Handle both direct and module execution
sys.path.insert(0, str(Path(__file__).parent))

try:
    from . import config
except ImportError:
    import config


# ═══════════════════════════════════════════════════════════════
#  TIER 1: PROCEDURAL BACKGROUNDS (FFmpeg)
# ═══════════════════════════════════════════════════════════════

def _proc_plasma_dark(duration: float, out: str) -> bool:
    """Dark purple swirling plasma — great for dark/mystery moods."""
    logger.info("   🎨 Generating dark plasma background…")
    # Use cellular automata with dark fantasy color grading
    life_filter = (
        f"life=size={config.VID_WIDTH}x{config.VID_HEIGHT}:rate={config.VID_FPS}:"
        f"death_color=0x080012:life_color=0x5500aa:mold=80:random_fill_ratio=0.04"
    )
    color_filter = (
        f"scale={config.VID_WIDTH}:{config.VID_HEIGHT},"
        f"colorbalance=bs=0.3:bm=0.2:bh=0.15:rs=-0.15:rm=-0.08,"
        f"curves=r='0/0 0.4/0.12 1/0.5':g='0/0 0.4/0.08 1/0.4':b='0/0 0.4/0.35 1/0.9',"
        f"eq=brightness=-0.1:contrast=1.2:saturation=1.6,"
        f"vignette=PI/3.5,"
        f"gblur=sigma=2"
    )
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", life_filter,
        "-vf", color_filter, "-t", str(duration),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def _proc_particles_fire(duration: float, out: str) -> bool:
    """Floating fire ember particles on dark background."""
    logger.info("   🔥 Generating fire particles background…")
    life_filter = (
        f"life=size={config.VID_WIDTH}x{config.VID_HEIGHT}:rate={config.VID_FPS}:"
        f"death_color=0x0a0000:life_color=0xff4400:mold=40:random_fill_ratio=0.02"
    )
    color_filter = (
        f"scale={config.VID_WIDTH}:{config.VID_HEIGHT},"
        f"colorbalance=rs=0.3:rm=0.15:rh=0.1:bs=-0.2:bm=-0.15,"
        f"eq=brightness=-0.12:contrast=1.3:saturation=2.0,"
        f"vignette=PI/3,"
        f"gblur=sigma=3"
    )
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", life_filter,
        "-vf", color_filter, "-t", str(duration),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def _proc_particles_magic(duration: float, out: str) -> bool:
    """Glowing blue-white magic particles."""
    logger.info("   ✨ Generating magic particles background…")
    life_filter = (
        f"life=size={config.VID_WIDTH}x{config.VID_HEIGHT}:rate={config.VID_FPS}:"
        f"death_color=0x050510:life_color=0x4488ff:mold=50:random_fill_ratio=0.03"
    )
    color_filter = (
        f"scale={config.VID_WIDTH}:{config.VID_HEIGHT},"
        f"colorbalance=bs=0.25:bm=0.2:rs=-0.1:gs=-0.05,"
        f"eq=brightness=-0.08:contrast=1.15:saturation=1.5,"
        f"vignette=PI/4,"
        f"gblur=sigma=2.5"
    )
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", life_filter,
        "-vf", color_filter, "-t", str(duration),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def _proc_gradient_blue(duration: float, out: str) -> bool:
    """Slowly shifting blue-grey gradient for sad moods."""
    logger.info("   🌧 Generating sad blue gradient background…")
    from PIL import Image, ImageDraw
    random.seed(42)

    img = Image.new("RGB", (config.VID_WIDTH, config.VID_HEIGHT))
    draw = ImageDraw.Draw(img)
    for y in range(config.VID_HEIGHT):
        p = y / config.VID_HEIGHT
        r = int(15 + p * 20)
        g = int(20 + p * 30)
        b = int(50 + p * 60)
        draw.line([(0, y), (config.VID_WIDTH, y)], fill=(r, g, b))

    # Add rain-like dots
    for _ in range(200):
        x = random.randint(0, config.VID_WIDTH)
        y = random.randint(0, config.VID_HEIGHT)
        sz = random.randint(1, 2)
        br = random.randint(60, 120)
        draw.ellipse([x-sz, y-sz, x+sz, y+sz], fill=(br, br, br+20))

    frame = str(config.TEMP_DIR / "bg_blue.png")
    img.save(frame)

    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", frame,
        "-vf", f"vignette=PI/4,eq=brightness=-0.05",
        "-t", str(duration), "-r", str(config.VID_FPS),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def _proc_gradient_warm(duration: float, out: str) -> bool:
    """Golden warm gradient for happy/triumph moods."""
    logger.info("   ☀️ Generating warm gradient background…")
    from PIL import Image, ImageDraw
    random.seed(42)

    img = Image.new("RGB", (config.VID_WIDTH, config.VID_HEIGHT))
    draw = ImageDraw.Draw(img)
    for y in range(config.VID_HEIGHT):
        p = y / config.VID_HEIGHT
        r = int(50 + p * 40)
        g = int(25 + p * 30)
        b = int(5 + p * 15)
        draw.line([(0, y), (config.VID_WIDTH, y)], fill=(r, g, b))

    for _ in range(150):
        x = random.randint(0, config.VID_WIDTH)
        y = random.randint(0, config.VID_HEIGHT)
        sz = random.randint(1, 3)
        br = random.randint(150, 220)
        draw.ellipse([x-sz, y-sz, x+sz, y+sz], fill=(br, br-20, br-60))

    frame = str(config.TEMP_DIR / "bg_warm.png")
    img.save(frame)

    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", frame,
        "-vf", f"vignette=PI/4",
        "-t", str(duration), "-r", str(config.VID_FPS),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def _proc_flash_dark(duration: float, out: str) -> bool:
    """Flash white then dark — for surprise moments."""
    return _proc_plasma_dark(duration, out)  # Fallback to plasma


# Procedural mode dispatcher
PROCEDURAL_GENERATORS = {
    "plasma_dark":      _proc_plasma_dark,
    "particles_fire":   _proc_particles_fire,
    "particles_magic":  _proc_particles_magic,
    "gradient_blue":    _proc_gradient_blue,
    "gradient_warm":    _proc_gradient_warm,
    "flash_dark":       _proc_flash_dark,
}


def generate_procedural_background(mood: str, duration: float, out: str) -> bool:
    """Generate Tier 1 procedural background based on mood."""
    mode = config.BG_PROCEDURAL_MODES.get(mood, "particles_magic")
    generator = PROCEDURAL_GENERATORS.get(mode, _proc_particles_magic)

    success = generator(duration, out)
    if not success:
        logger.warning(f"⚠️  Procedural bg '{mode}' failed → fallback to static")
        _proc_gradient_blue(duration, out)

    return True


# ═══════════════════════════════════════════════════════════════
#  TIER 2: PEXELS STOCK FOOTAGE
# ═══════════════════════════════════════════════════════════════

def _search_pexels_video(query: str, orientation: str = "portrait") -> Optional[str]:
    """Search Pexels for a video and return download URL."""
    try:
        import requests
    except ImportError:
        logger.warning("requests not installed — pip install requests")
        return None

    if not config.PEXELS_API_KEY:
        logger.warning("No Pexels API key configured")
        return None

    headers = {"Authorization": config.PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": orientation,
        "size": "medium",
        "per_page": 15,
    }

    try:
        resp = requests.get(
            "https://api.pexels.com/videos/search",
            headers=headers, params=params, timeout=15
        )
        resp.raise_for_status()
        data = resp.json()

        videos = data.get("videos", [])
        if not videos:
            return None

        # Pick a random video from results for variety
        video = random.choice(videos[:10])

        # Find the best quality file (prefer HD, portrait)
        best_file = None
        for vf in video.get("video_files", []):
            w = vf.get("width", 0)
            h = vf.get("height", 0)
            if h > w and h >= 720:  # Portrait, at least 720p
                if best_file is None or h > best_file.get("height", 0):
                    best_file = vf

        # Fallback: any video file
        if not best_file and video.get("video_files"):
            best_file = video["video_files"][0]

        if best_file:
            return best_file.get("link")

    except Exception as e:
        logger.warning(f"Pexels API error: {e}")

    return None


def _download_file(url: str, output_path: str) -> bool:
    """Download a file."""
    try:
        import requests
        resp = requests.get(url, stream=True, timeout=60)
        resp.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        logger.warning(f"Download failed: {e}")
        return False


def _prepare_pexels_video(src: str, duration: float, out: str) -> bool:
    """Crop, scale, and color-grade a Pexels video for Shorts."""
    vf = (
        f"fps={config.VID_FPS},settb=1/1000,"
        f"crop=min(iw\\,ih*9/16):min(ih\\,iw*16/9),"
        f"scale={config.VID_WIDTH}:{config.VID_HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={config.VID_WIDTH}:{config.VID_HEIGHT},"
        f"eq=brightness=-0.06:contrast=1.08:saturation=0.9,"
        f"vignette=PI/4"
    )
    cmd = [
        "ffmpeg", "-y", "-stream_loop", "-1", "-i", src,
        "-vf", vf, "-t", str(duration), "-an",
        "-r", str(config.VID_FPS),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def generate_pexels_background(mood: str, duration: float, out: str) -> bool:
    """Generate Tier 2 Pexels background based on mood."""
    search_terms = config.PEXELS_SEARCH_TERMS.get(mood, config.PEXELS_SEARCH_TERMS["neutral"])
    query = random.choice(search_terms)

    # Check cache first
    cache_key = hashlib.md5(query.encode()).hexdigest()[:12]
    cached_raw = str(config.CACHE_DIR / f"pexels_{cache_key}.mp4")

    if not os.path.exists(cached_raw):
        logger.info(f"   🔍 Searching Pexels: '{query}'…")
        url = _search_pexels_video(query)
        if not url:
            logger.warning(f"   ⚠️  No Pexels results for '{query}' → trying fallback…")
            # Try another term
            for term in search_terms:
                if term != query:
                    url = _search_pexels_video(term)
                    if url:
                        break

        if not url:
            logger.warning("   ⚠️  Pexels failed → falling back to procedural")
            return generate_procedural_background(mood, duration, out)

        logger.info(f"   ⬇  Downloading Pexels video…")
        if not _download_file(url, cached_raw):
            return generate_procedural_background(mood, duration, out)

    logger.info(f"   🎥 Preparing Pexels background…")
    success = _prepare_pexels_video(cached_raw, duration, out)

    if not success:
        logger.warning("   ⚠️  Pexels video prep failed → fallback to procedural")
        return generate_procedural_background(mood, duration, out)

    logger.info("   ✅ Pexels background ready!")
    return True


# ═══════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════


def generate_scene_backgrounds(
    segments: List[Dict],
    total_duration: float,
    output_path: str,
) -> str:
    """
    Generate a background video that switches clips whenever the mood changes.

    Fixes problem: single video looping the entire short.

    How it works:
      1. Group consecutive segments by mood
      2. Allocate each group a proportional duration
      3. Fetch a unique Pexels clip per mood group
      4. FFmpeg-concat them into one seamless background

    Args:
        segments: List of segment dicts (each has 'mood' key from mood_detector)
        total_duration: Total video duration in seconds
        output_path: Where to write the stitched background

    Returns: Path to the stitched background video
    """
    if not segments:
        generate_background("neutral", total_duration, output_path)
        return output_path

    # ── Step 1: Group segments by mood ────────────────────────
    groups: List[Dict] = []
    for seg in segments:
        mood = seg.get("mood", "neutral")
        if groups and groups[-1]["mood"] == mood:
            groups[-1]["word_count"] += len(seg.get("text", "").split())
        else:
            groups.append({
                "mood":       mood,
                "word_count": len(seg.get("text", "").split()),
            })

    # Collapse tiny groups (< 5% of total) into neighbours to avoid flash cuts
    total_words = sum(g["word_count"] for g in groups) or 1
    merged: List[Dict] = []
    for g in groups:
        if g["word_count"] / total_words < 0.05 and merged:
            merged[-1]["word_count"] += g["word_count"]
        else:
            merged.append(g)
    groups = merged

    # ── Step 2: Allocate durations ────────────────────────────
    for g in groups:
        g["duration"] = max(3.0, total_duration * (g["word_count"] / total_words))

    logger.info(f"🎬 Scene backgrounds: {len(groups)} mood group(s)")
    for i, g in enumerate(groups):
        logger.info(f"   [{i+1}] mood={g['mood']:<10} dur={g['duration']:.1f}s")

    # ── Step 3: Generate one clip per group ───────────────────
    clip_paths: List[str] = []
    used_queries: set = set()

    first_clip_raw = None
    for i, group in enumerate(groups):
        clip_path = str(config.TEMP_DIR / f"scene_bg_{i:03d}.mp4")
        mood      = group["mood"]
        dur       = group["duration"] + 0.5   # tiny overlap for concat safety
        txt       = group.get("text", "").lower()

        # Force last clip to be the exact same as first clip
        if i == len(groups) - 1 and len(groups) > 1 and first_clip_raw is not None:
            if _prepare_pexels_video(first_clip_raw, dur, clip_path):
                clip_paths.append(clip_path)
                logger.info(f"   [{i+1}] ? Pexels loop clip ready (matches first clip)")
                continue

        if config.PEXELS_API_KEY:
            # Smart relative keyword extraction for epic fantasy story
            import string
            stop_words = {'which', 'there', 'their', 'about', 'would', 'could', 'should', 'where', 'because', 'without', 'through', 'before', 'himself', 'herself', 'thought', 'always', 'never'}
            fantasy_nouns = ['king', 'emperor', 'sword', 'castle', 'magic', 'creatures', 'shadows', 'light', 'academy', 'empire', 'energy', 'fire', 'darkness', 'battle', 'forest', 'mountain', 'stars', 'night', 'sky']
            
            words = [w.strip(string.punctuation) for w in txt.split()]
            keywords = [w for w in words if len(w) > 4 and w not in stop_words]
            
            extracted = None
            for kw in keywords:
                if kw in fantasy_nouns:
                    extracted = f"{mood} {kw}"
                    break
                    
            if not extracted and keywords:
                extracted = f"{mood} {max(set(keywords), key=keywords.count)}"
                
            candidates = [extracted] if extracted else config.PEXELS_SEARCH_TERMS.get(
                mood, config.PEXELS_SEARCH_TERMS["neutral"]
            )
            
            fresh = [q for q in candidates if q not in used_queries] or candidates
            query = random.choice(fresh)
            used_queries.add(query)

            logger.info(f"   [{i+1}] Pexels: '{query}'…")
            url = _search_pexels_video(query)

            if url:
                cache_key = hashlib.md5(query.encode()).hexdigest()[:12]
                cached_raw = str(config.CACHE_DIR / f"pexels_{cache_key}.mp4")

                if not os.path.exists(cached_raw):
                    if not _download_file(url, cached_raw):
                        url = None

                if url and os.path.exists(cached_raw):
                    if _prepare_pexels_video(cached_raw, dur, clip_path):
                        clip_paths.append(clip_path)
                        logger.info(f"   [{i+1}] ✅ Pexels clip ready")
                        continue

            logger.warning(f"   [{i+1}] ⚠️  Pexels failed → procedural fallback")

        # Fallback: procedural
        generate_procedural_background(mood, dur, clip_path)
        clip_paths.append(clip_path)

    if not clip_paths:
        generate_background("neutral", total_duration, output_path)
        return output_path

    if len(clip_paths) == 1:
        # Just trim to exact duration
        _trim_clip(clip_paths[0], total_duration, output_path)
        return output_path

    # ── Step 4: Stitch clips with crossfade ───────────────────
    return _crossfade_concat(clip_paths, groups, total_duration, output_path)


def _trim_clip(src: str, duration: float, output: str) -> str:
    """Trim a video clip to an exact duration."""
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-t", str(duration),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", output,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return output if r.returncode == 0 else src


def _crossfade_concat(
    clip_paths: List[str],
    groups: List[Dict],
    total_duration: float,
    output_path: str,
) -> str:
    """
    Crossfade-concatenate multiple clips using FFmpeg xfade filter.
    Falls back to hard cut concat if xfade fails.
    """
    FADE_DUR = 0.5   # seconds of crossfade overlap

    try:
        # Build xfade filter chain
        # xfade requires clips to have IDENTICAL resolution and FPS
        n = len(clip_paths)
        filter_parts = []
        current_label = "[0:v]"

        # Pre-process all inputs to strictly ensure identical timebase and framerate
        for i in range(n):
            filter_parts.append(f"[{i}:v]settb=1/1000,fps={config.VID_FPS}[v_norm_{i}]")
            
        current_label = "[v_norm_0]"

        for i in range(1, n):
            # offset = start time of clip i in the concatenated timeline
            offset = sum(g["duration"] for g in groups[:i]) - FADE_DUR * i
            offset = max(0.1, offset)

            out_label = f"[v{i}]" if i < n - 1 else "[vout]"
            filter_parts.append(
                f"{current_label}[v_norm_{i}]xfade=transition=fade:"
                f"duration={FADE_DUR}:offset={offset:.3f}{out_label}"
            )
            current_label = out_label

        filter_complex = "; ".join(filter_parts)

        inputs = []
        for p in clip_paths:
            inputs += ["-i", p]

        cmd = (
            ["ffmpeg", "-y"] + inputs
            + ["-filter_complex", filter_complex,
               "-map", "[vout]",
               "-t", str(total_duration),
               "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
               "-pix_fmt", "yuv420p", output_path]
        )

        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if r.returncode == 0:
            logger.info(f"✅ Scene backgrounds stitched with crossfade ({n} clips)")
            return output_path

        logger.warning("xfade concat failed — using hard-cut concat")

    except Exception as e:
        logger.warning(f"crossfade error: {e} — hard-cut fallback")

    # ── Hard-cut fallback ─────────────────────────────────────
    concat_file = str(config.TEMP_DIR / "bg_concat.txt")
    with open(concat_file, "w") as f:
        for p in clip_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")

    r = subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-vf", f"scale={config.VID_WIDTH}:{config.VID_HEIGHT}",
        "-t", str(total_duration),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", output_path,
    ], capture_output=True, text=True, timeout=120)

    if r.returncode == 0:
        logger.info(f"✅ Scene backgrounds stitched (hard cut, {len(clip_paths)} clips)")
        return output_path

    logger.error(f"❌ Background concat failed: {r.stderr[-300:]}")
    # Last resort: return first clip
    _trim_clip(clip_paths[0], total_duration, output_path)
    return output_path


# ────────────────────────────────────────────────────────────────
#  REPLACE generate_background() with this version
#  (keeps all existing logic, adds scene routing)
# ────────────────────────────────────────────────────────────────

def generate_background(
    mood: str,
    duration: float,
    out: str,
    segments: list = None,   # ← NEW optional param
) -> None:
    """
    Generate background video.

    UPGRADED:
      If segments are provided (from generate_short pipeline), call
      generate_scene_backgrounds() for per-scene clip switching.
      Otherwise behaves exactly as before.

    Args:
        mood:     Overall mood string (used as fallback when no segments)
        duration: Total duration in seconds
        out:      Output file path
        segments: Optional list of segment dicts with 'mood' keys
    """
    # Custom video override
    if config.BG_CUSTOM_VIDEO and os.path.exists(config.BG_CUSTOM_VIDEO):
        logger.info(f"🎥 Using custom background: {config.BG_CUSTOM_VIDEO}")
        _prepare_pexels_video(config.BG_CUSTOM_VIDEO, duration, out)
        return

    # Multi-scene path (NEW)
    if segments and len(segments) > 1:
        generate_scene_backgrounds(segments, duration, out)
        return

    # Single-mood path (original behaviour)
    tier = config.BG_TIER
    if tier >= 2 and config.PEXELS_API_KEY:
        if generate_pexels_background(mood, duration, out):
            return

    generate_procedural_background(mood, duration, out)

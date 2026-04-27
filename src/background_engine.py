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


def _proc_solid_color(mood: str, duration: float, out: str) -> bool:
    """Generate a simple solid dark grey background for Tier 0 (No BS mode)."""
    logger.info("   ⬛ Generating solid color background…")
    
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=0x111111:s={config.VID_WIDTH}x{config.VID_HEIGHT}",
        "-t", str(duration), "-r", str(config.VID_FPS),
        "-c:v", config.VIDEO_CODEC, "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", out
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode == 0
    except Exception as e:
        logger.error(f"Failed to generate solid background: {e}")
        return False

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
#  TIER 2: PEXELS STOCK FOOTAGE with Content Filtering
# ═══════════════════════════════════════════════════════════════

def _filter_background_content(video_obj: Dict) -> bool:
    """
    Filter background videos to exclude:
    - Humans, people, faces
    - 3D particles, CGI, renders
    - Urban/modern content
    - Only allow: nature, wildlife, structures, abstract
    
    Args:
        video_obj: Video object from Pexels API
    
    Returns: True if video passes filters, False otherwise
    """
    if not config.FILTER_BACKGROUND_CONTENT:
        return True
    
    # Get video attributes: tags, id, url, etc
    video_tags = str(video_obj.get("tags", [])).lower()
    video_url = str(video_obj.get("url", "")).lower()
    video_id = video_obj.get("id", 0)
    
    # Check blacklist (reject these terms)
    for blacklisted in config.BLACKLIST_BACKGROUND_KEYWORDS:
        if blacklisted.lower() in video_tags or blacklisted.lower() in video_url:
            logger.debug(f"   ❌ Rejected video {video_id} — contains '{blacklisted}'")
            return False
    
    # Check whitelist (prefer these terms)
    allowed = False
    for allowed_term in config.ALLOWED_BACKGROUND_KEYWORDS:
        if allowed_term.lower() in video_tags or allowed_term.lower() in video_url:
            allowed = True
            break
    
    if not allowed:
        logger.debug(f"   ❌ Rejected video {video_id} — no allowed keywords found")
        return False
    
    logger.debug(f"   ✅ Approved video {video_id}")
    return True


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

        # Filter videos by content policy
        filtered_videos = [v for v in videos if _filter_background_content(v)]
        
        if not filtered_videos:
            logger.warning(f"   ⚠️  No suitable videos after content filtering for query: {query}")
            return None

        # Pick a random video from filtered results for variety
        video = random.choice(filtered_videos[:10])

        # Find the best quality file (prefer HD, portrait)
        best_file = None
        for vf in video.get("video_files", []):
            w = vf.get("width", 0)
            h = vf.get("height", 0)
            
            # Prioritize TRUE HD & 4K (h >= 1920). Still fall back to 1080 or 720 if not available
            if h >= w:
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
        "-c:v", config.VIDEO_CODEC, "-preset", config.VIDEO_PRESET, "-crf", str(config.VIDEO_CRF),
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
            groups[-1]["text"] += " " + seg.get("text", "")
        else:
            groups.append({
                "mood":       mood,
                "word_count": len(seg.get("text", "").split()),
                "text":       seg.get("text", ""),
            })

    # Collapse tiny groups (< 5% of total) into neighbours to avoid flash cuts
    total_words = sum(g["word_count"] for g in groups) or 1
    merged: List[Dict] = []
    for g in groups:
        if g["word_count"] / total_words < 0.05 and merged:
            merged[-1]["word_count"] += g["word_count"]
            merged[-1]["text"] += " " + g["text"]
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
            # Bypass dynamic natural language keyword extraction which accidentally
            # triggers Pexels to return videos of human actors (e.g. "king", "knight").
            # Instead, we strictly use the predefined B-Roll scenery terms in config
            # and guarantee no people are included by appending scenery constraints.
            
            candidates = [
                f"{q} landscape scenery nobody"
                for q in config.PEXELS_SEARCH_TERMS.get(mood, config.PEXELS_SEARCH_TERMS["neutral"])
            ]

            # ── Context-Aware Location Keywords (fuzzy multi-match) ──
            # Check if ANY word from a location key appears in the scene text.
            # This catches paraphrases like "polished mahogany" → "mahogany" key.
            group_text = group.get("text", "").lower()
            location_candidates = []
            for loc_key, loc_query in getattr(config, "LOCATION_KEYWORDS", {}).items():
                # Fuzzy: check if ANY word from the key is in the text
                key_words = loc_key.lower().split()
                if any(kw in group_text for kw in key_words):
                    location_candidates.append(loc_query)
                    logger.debug(f"      Location match: '{loc_key}' → '{loc_query}'")

            # Prioritize scene-specific queries OVER generic mood queries
            if location_candidates:
                candidates = location_candidates + candidates

            fresh = [q for q in candidates if q not in used_queries] or candidates
            query = random.choice(fresh)
            used_queries.add(query)

            # ── CURATED BACKGROUND LIBRARY OVERRIDE ──
            # Check if there is a local file in assets/backgrounds that matches mood or location
            local_clip = None
            curated_dir = Path("assets/backgrounds")
            if curated_dir.exists():
                search_terms = [mood] + [k.replace(" ", "_") for k in getattr(config, "LOCATION_KEYWORDS", {}).keys()]
                for term in search_terms:
                    term_dir = curated_dir / term
                    if term_dir.exists():
                        local_files = list(term_dir.glob("*.mp4"))
                        if local_files:
                            local_clip = str(random.choice(local_files))
                            logger.info(f"   [{i+1}] 📁 Using CuratedBackgroundLibrary clip: {local_clip}")
                            break
            
            if local_clip:
                if first_clip_raw is None:
                    first_clip_raw = local_clip
                if _prepare_pexels_video(local_clip, dur, clip_path):
                    clip_paths.append(clip_path)
                    logger.info(f"   [{i+1}] ✅ Curated clip ready")
                    continue
                else:
                    logger.warning(f"   [{i+1}] ⚠️  Failed to prepare curated clip, falling back to Pexels")

            logger.info(f"   [{i+1}] Pexels: '{query}'…")
            url = _search_pexels_video(query)

            if url:
                cache_key = hashlib.md5(query.encode()).hexdigest()[:12]
                cached_raw = str(config.CACHE_DIR / f"pexels_{cache_key}.mp4")

                if not os.path.exists(cached_raw):
                    if not _download_file(url, cached_raw):
                        url = None

                if url and os.path.exists(cached_raw):
                    if first_clip_raw is None:
                        first_clip_raw = cached_raw
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
        # Build xfade filter chain - using dynamic dopamine transitions
        import random
        dopamine_transitions = ["zoomin", "slideleft", "slideright", "wipeleft", "wiperight", "smoothleft", "fade"]
        
        n = len(clip_paths)
        filter_parts = []

        # Pre-process all inputs to strictly ensure identical timebase and framerate
        for i in range(n):
            filter_parts.append(f"[{i}:v]settb=1/1000,fps={config.VID_FPS}[v_norm_{i}]")

        # Concat all clips with hard cuts
        concat_inputs = "".join([f"[v_norm_{i}]" for i in range(n)])
        filter_parts.append(f"{concat_inputs}concat=n={n}:v=1:a=0[v_merged]")

        # Apply a fade-in at the very beginning and fade-out at the very end
        fade_out_start = max(0.1, total_duration - 1.5)  # 1.5 second fade out
        filter_parts.append(f"[v_merged]fade=t=in:st=0:d=1.5,fade=t=out:st={fade_out_start:.3f}:d=1.5[vout]")

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
    if segments and len(segments) > 1 and config.BG_TIER > 0:
        generate_scene_backgrounds(segments, duration, out)
        return

    # Single-mood path (original behaviour)
    tier = config.BG_TIER
    if tier >= 2 and config.PEXELS_API_KEY:
        if generate_pexels_background(mood, duration, out):
            return

    if tier >= 1:
        generate_procedural_background(mood, duration, out)
        return
        
    # Tier 0 (or fallback for all): Solid Color Background
    _proc_solid_color(mood, duration, out)
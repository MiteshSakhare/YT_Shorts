# ═══════════════════════════════════════════════════════════════
#  CONFIG.PY — YouTube Shorts Generator Configuration (v2.0)
#  The Twice-Crowned King — AI Video Pipeline
#  Edit these settings to customize your video generation
# ═══════════════════════════════════════════════════════════════

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / ".env")

# ─────────────────────────────────────────────────────────────
#  DIRECTORY SETUP
# ─────────────────────────────────────────────────────────────
# Set BASE_DIR relative to where the project root is (one folder up from src/)
BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / ".temp"
SFX_DIR = BASE_DIR / "sfx"
CACHE_DIR = BASE_DIR / ".cache"

for _d in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, SFX_DIR, CACHE_DIR]:
    _d.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────
#  VIDEO SETTINGS
# ─────────────────────────────────────────────────────────────
VID_WIDTH = 1080              # YouTube Shorts width
VID_HEIGHT = 1920             # YouTube Shorts height
VID_FPS = 50                  # Frames per second

# Duration presets  ←  CHOOSE ONE
DURATION_MODE = "unlimited"       # "unlimited" = full audio length (no hard cap)
DURATION_SETTINGS = {
    "unlimited": {"max_secs": 999,  "target_words": 999},   # No limit - play full audio
    "short":  {"max_secs": 50,  "target_words": 140},   # ~40-50 sec (allows intro+story+outro)
    "medium": {"max_secs": 65,  "target_words": 180},   # ~50-65 sec (allows intro+story+outro)
}
MAX_DURATION = DURATION_SETTINGS[DURATION_MODE]["max_secs"]
TARGET_WORDS = DURATION_SETTINGS[DURATION_MODE]["target_words"]

# ─────────────────────────────────────────────────────────────
#  VOICE ASSIGNMENTS  (Character Memory)
#  These stay CONSISTENT across ALL 48+ parts
#  See all voices: edge-tts --list-voices
# ─────────────────────────────────────────────────────────────
VOICES = {
    # ── Main Characters ──────────────────────────────────────
    "narrator":     "en-US-AriaNeural",       # Rich, dramatic female narrator
    "kaelen":       "en-US-GuyNeural",        # Deep, calm male protagonist
    "seraphina":    "en-GB-SoniaNeural",      # Elegant British female
    "rin":          "en-US-SaraNeural",       # Playful energetic female
    "elara":        "en-US-MichelleNeural",   # Warm thoughtful female
    "vex'ahlia":    "en-US-NancyNeural",      # Mysterious female
    # ── Secondary Characters ──────────────────────────────────
    "morwen":       "en-US-JennyNeural",      # Stern female
    "valerius":     "en-US-TonyNeural",       # Arrogant male
    "gaius":        "en-GB-RyanNeural",       # Wise British male
    "malachar":     "en-US-DavisNeural",      # Dark villain male
    "mara":         "en-US-JaneNeural",       # Cold female
    "aldric":       "en-GB-ElliotNeural",     # Commanding male (The Lion)
    "duke":         "en-US-GuyNeural",        # Noble male
    "herald":       "en-US-TonyNeural",       # Formal male
    "guard":        "en-US-TonyNeural",       # Soldier male
    "instructor":   "en-US-DavisNeural",      # Teacher male
    "oracle":       "en-US-NancyNeural",      # Mystical female
    "arcturus":     "en-US-GuyNeural",        # Emperor's past voice
    "commander":    "en-US-DavisNeural",      # Military male
    "council":      "en-GB-RyanNeural",       # Council member
    "inquisitor":   "en-US-JaneNeural",       # Inquisitor female
    # ── Fallback ──────────────────────────────────────────────
    "_default":     "en-US-AriaNeural",       # Default fallback
}

# Voice style modifiers — rate and pitch per character
VOICE_STYLE = {
    "narrator":     {"rate": "+0%",  "pitch": "+0Hz"},     # Natural cinematic
    "kaelen":       {"rate": "-5%",  "pitch": "-5Hz"},     # Slower, deeper
    "seraphina":    {"rate": "+0%",  "pitch": "+5Hz"},     # Elevated elegant
    "rin":          {"rate": "+10%", "pitch": "+10Hz"},    # Fast, bright
    "elara":        {"rate": "-5%",  "pitch": "+0Hz"},     # Thoughtful pacing
    "vex'ahlia":    {"rate": "-8%",  "pitch": "-3Hz"},     # Ominous slow
    "valerius":     {"rate": "+5%",  "pitch": "-8Hz"},     # Aggressive low
    "malachar":     {"rate": "-10%", "pitch": "-8Hz"},     # Deep villain
    "aldric":       {"rate": "-3%",  "pitch": "-3Hz"},     # Commanding
    "oracle":       {"rate": "-8%",  "pitch": "+3Hz"},     # Ethereal
    "mara":         {"rate": "+0%",  "pitch": "+0Hz"},     # Neutral cold
    "gaius":        {"rate": "-5%",  "pitch": "-3Hz"},     # Old wise
    "_default":     {"rate": "+0%",  "pitch": "+0Hz"},
}

# Character name aliases — maps alternate names to canonical voice keys
CHARACTER_ALIASES = {
    "arcturus": "kaelen",         # Past life = same voice
    "emperor": "kaelen",
    "duke arcturus": "duke",
    "lord malachar": "malachar",
    "commander": "vex'ahlia",
    "the lion": "aldric",
    "king aldric": "aldric",
    "envoy": "herald",
    "soldier": "guard",
    "teacher": "instructor",
    "inquisitor mara": "mara",
}

# ─────────────────────────────────────────────────────────────
#  CHARACTER-SPECIFIC AUDIO EFFECTS (FFmpeg filters)
#  Each character gets unique spatial/tonal treatment
# ─────────────────────────────────────────────────────────────
CHARACTER_AUDIO_FX_ENABLED = True

CHARACTER_AUDIO_FX = {
    "narrator":   "highpass=f=80,equalizer=f=200:t=h:w=200:g=1",
    # Clean + warm — professional narration

    "kaelen":     "highpass=f=60,equalizer=f=150:t=h:w=100:g=3,lowpass=f=5000",
    # Bass boost + slightly muffled — brooding power

    "seraphina":  "highpass=f=100,equalizer=f=3000:t=h:w=500:g=2",
    # Bright + clear treble — elegant commanding

    "rin":        "highpass=f=120,equalizer=f=2000:t=h:w=300:g=2",
    # Energetic + crisp midrange

    "elara":      "highpass=f=80,equalizer=f=800:t=h:w=400:g=1",
    # Warm + full — thoughtful

    "vex'ahlia":  "highpass=f=60,aecho=0.8:0.88:40:0.2,lowpass=f=4000",
    # Echo + low pass — mysterious ominous

    "malachar":   "highpass=f=50,equalizer=f=100:t=h:w=100:g=4,aecho=0.8:0.9:60:0.3",
    # Heavy bass + echo — dark villain

    "valerius":   "highpass=f=80,equalizer=f=1500:t=h:w=300:g=2,volume=1.1",
    # Slightly louder + dominant midrange — arrogant

    "aldric":     "highpass=f=70,equalizer=f=200:t=h:w=200:g=2",
    # Strong low-mids — commanding king

    "oracle":     "highpass=f=80,aecho=0.6:0.5:80:0.4,equalizer=f=4000:t=h:w=500:g=2",
    # Ethereal echo + shimmer — mystical

    "_default":   "highpass=f=80",
}

# ─────────────────────────────────────────────────────────────
#  SUBTITLE SETTINGS (Viral karaoke style)
# ─────────────────────────────────────────────────────────────
WORDS_PER_CUE = 2                # Words shown at once (3 = more punchy)
FONT_NAME = "Bangers"            # Viral YouTube Shorts font
FONT_SIZE = 92                  # Large for mobile readability
OUTLINE_WIDTH = 6                # Thick outline for contrast
MARGIN_BOTTOM = 160              # Distance from bottom of frame
SHADOW_DEPTH = 3                 # Shadow offset pixels
SUBTITLE_GLOW = True             # Add glow effect behind text

# ASS color format (AABBGGRR)
SUBTITLE_WHITE = "&H00FFFFFF"    # White text
SUBTITLE_YELLOW = "&H0000FFFF"   # Yellow highlight (karaoke active word)
SUBTITLE_BLACK = "&H00000000"    # Black outline

# Per-character subtitle highlight colors
CHARACTER_SUB_COLORS = {
    "narrator":   "&H00FFFFFF",   # White
    "kaelen":     "&H00FFCC99",   # Ice blue
    "seraphina":  "&H0000D4FF",   # Gold
    "rin":        "&H00FFFF00",   # Cyan
    "elara":      "&H00AAFFAA",   # Soft green
    "vex'ahlia":  "&H00FF66FF",   # Purple
    "malachar":   "&H004444FF",   # Dark red
    "valerius":   "&H006699FF",   # Orange
    "aldric":     "&H0000CCFF",   # Amber
    "_default":   "&H0000FFFF",   # Yellow
}

# ─────────────────────────────────────────────────────────────
#  BACKGROUND SETTINGS (Multi-tier system)
# ─────────────────────────────────────────────────────────────
# Tier 1 = procedural (FFmpeg, works everywhere)
# Tier 2 = Pexels stock footage (free API)
# Tier 3 = ComfyUI AI generation (future)
BG_TIER = 2                       # Start with Tier 2 (Pexels)
BG_CUSTOM_VIDEO = ""              # Path to custom background if needed

# Mood → procedural background mapping (Tier 1)
BG_PROCEDURAL_MODES = {
    "dark":     "plasma_dark",     # Swirling dark purple plasma
    "sad":      "gradient_blue",   # Slowly shifting blue-grey
    "thrill":   "particles_fire",  # Floating ember particles
    "happy":    "gradient_warm",   # Golden warm gradient
    "epic":     "particles_fire",  # Fire + particles
    "surprise": "flash_dark",      # Flash white → dark
    "mystery":  "plasma_dark",     # Dark plasma
    "neutral":  "particles_magic", # Magic particle default
}

# Pexels API (Tier 2) — FREE
# Loaded from .env file for security (DO NOT hardcode in source)
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# Mood → Pexels search terms
PEXELS_SEARCH_TERMS = {
    "dark":     ["dark forest fog", "shadows dark corridor", "dark smoke"],
    "sad":      ["rain window cinematic", "dark ocean waves", "cloudy sky moody"],
    "thrill":   ["fire sparks dark", "lightning storm night", "fast motion blur"],
    "happy":    ["golden sunlight nature", "sunrise forest", "light particles"],
    "epic":     ["mountain clouds aerial", "castle fortress dark", "storm clouds dramatic"],
    "surprise": ["explosion light", "bright flash abstract", "energy particles"],
    "mystery":  ["fog forest night", "dark tunnel light", "misty lake"],
    "neutral":  ["abstract dark particles", "dark fantasy landscape", "cosmic stars nebula"],
}

# ─────────────────────────────────────────────────────────────
#  SOUND EFFECTS (Mood-based)
# ─────────────────────────────────────────────────────────────
MOOD_SFX_ENABLED = True
SFX_VOLUME = 0.15               # SFX mix volume (0.0-1.0)

# Transition SFX between scene changes
TRANSITION_SFX_ENABLED = True

# ─────────────────────────────────────────────────────────────
#  BACKGROUND MUSIC
# ─────────────────────────────────────────────────────────────
MUSIC_MODE = "generated"         # "generated" = dark ambient | "none" = silence
MUSIC_VOLUME = 0.10              # Background music volume
DYNAMIC_MUSIC_DUCKING = True     # Auto-lower music when voice plays

# Mood → music style
MUSIC_MOODS = {
    "dark":     {"freqs": [73.4, 146.8, 220],    "decay": 0.20, "filter": "lowpass=f=600"},
    "sad":      {"freqs": [130.8, 196.0, 261.6], "decay": 0.30, "filter": "lowpass=f=800"},
    "thrill":   {"freqs": [98.0, 146.8, 196.0],  "decay": 0.10, "filter": "lowpass=f=500"},
    "happy":    {"freqs": [261.6, 329.6, 392.0], "decay": 0.25, "filter": "lowpass=f=1200"},
    "epic":     {"freqs": [73.4, 110.0, 146.8],  "decay": 0.15, "filter": "lowpass=f=700"},
    "neutral":  {"freqs": [146.8, 220, 293.7],   "decay": 0.20, "filter": "lowpass=f=800"},
}

# ─────────────────────────────────────────────────────────────
#  HOOK SETTINGS (First 3 seconds = critical)
# ─────────────────────────────────────────────────────────────
SHOW_HOOK = True
HOOK_DURATION = 3.0              # Seconds

# ─────────────────────────────────────────────────────────────
#  LOOP BRIDGE (2026 Algorithm Hack)
# ─────────────────────────────────────────────────────────────
ADD_LOOP_BRIDGE = True              # Audio loop bridge for seamless replay
LOOP_BRIDGE_DURATION = 2.0        # Match loop_transition duration for seamless UX

# ─────────────────────────────────────────────────────────────
#  2026 UPGRADE FEATURES (Critical Improvements)
# ─────────────────────────────────────────────────────────────
USE_REAL_TIME_DURATION = True          # Measure actual TTS output (±20ms accuracy)
USE_FRAME_PERFECT_SUBTITLES = False    # Librosa speech detection for sync [WIP]
ADD_LOOP_TRANSITION = True             # ✅ ENABLED — 2-3 second loop overlay for replay boost
ADD_AI_DISCLOSURE = False              # ❌ DISABLED — Removes watermark, keeps cleaner look
USE_CURATED_BACKGROUNDS = True         # Use curated library instead of random Pexels

AI_DISCLOSURE_POSITION = "top-right"   # or "bottom-left", "top-left", "bottom-right"
AI_DISCLOSURE_OPACITY = 0.85           # 0.0 (transparent) to 1.0 (opaque)

# ─────────────────────────────────────────────────────────────
#  VIDEO ENCODING — Optimized for Smooth Playback on YouTube
# ─────────────────────────────────────────────────────────────
VIDEO_CODEC = "libx264"        # H.264 (universal YouTube compatibility)
VIDEO_PRESET = "faster"        # faster = smoother motion, good quality/speed tradeoff
VIDEO_CRF = 18                 # 18 = high quality (lower = better, 0-51 range)
AUDIO_CODEC = "aac"
AUDIO_BITRATE = "192k"
AUDIO_SAMPLE_RATE = "48000"
USE_HWACCEL = True             # Use hardware acceleration if available
VIDEO_PROFILE = "main"         # H.264 profile (main = compatibility)
VIDEO_LEVEL = "4.2"            # H.264 level (4.2 = YouTube compatible)
MAXRATE = "5000k"              # Max bitrate for smooth playback
BUFSIZE = "10000k"             # Buffer size for reducing bitrate jitter

# ─────────────────────────────────────────────────────────────
#  SCRIPT PARSING
# ─────────────────────────────────────────────────────────────
SAID_VERBS = [
    "said", "whispered", "replied", "answered", "called", "murmured", "breathed",
    "asked", "announced", "interrupted", "laughed", "snapped", "hissed", "growled",
    "admitted", "continued", "added", "noted", "demanded", "corrected", "stated",
    "repeated", "explained", "spoke", "exclaimed", "cried", "shouted", "told",
    "purred", "drawled", "chimed", "mused", "sighed", "began", "finished", "scoffed",
]

# ─────────────────────────────────────────────────────────────
#  YOUTUBE METADATA & BRANDING
# ─────────────────────────────────────────────────────────────
CHANNEL_NAME = "Snippet Stories"
STORY_TITLE = "The Twice-Crowned King"
STORY_HASHTAGS = (
    "#shorts #fantasy #reincarnation #darkfantasy #storyshorts "
    "#demonking #academyfantasy #storytime #animestory #webtoon "
    "#fyp #foryoupage #viral #thetwicecrownedking"
)

# ─────────────────────────────────────────────────────────────
#  INTRO & OUTRO (Channel Branding)
# ─────────────────────────────────────────────────────────────
ADD_INTRO = True                      # Add channel intro at start
ADD_OUTRO = True                      # Add channel outro at end
INTRO_DURATION = 2.0                   # Seconds
OUTRO_DURATION = 2.0                   # Seconds
INTRO_VIDEO_PATH = BASE_DIR / "assets" / "intro.mp4"  # Path to intro video file
OUTRO_VIDEO_PATH = BASE_DIR / "assets" / "outro.mp4"  # Path to outro video file

# If video files don't exist, use text-based branding instead
USE_TEXT_INTRO = True                  # Generate text intro if no video file
USE_TEXT_OUTRO = True                  # Generate text outro if no video file
INTRO_TEXT = f"👑 {CHANNEL_NAME}"      # Text for intro overlay
OUTRO_TEXT = f"Subscribe to {CHANNEL_NAME}"  # Text for outro overlay
BRANDING_FONT_SIZE = 92               # Size of branding text
BRANDING_TEXT_COLOR = "&H0000FFFF"     # Yellow text (ASS format)
BRANDING_BACKGROUND_COLOR = "black"    # Background: black, navy, purple, etc.

# ─────────────────────────────────────────────────────────────
#  CHANNEL WATERMARK (Always visible frame corner)
# ─────────────────────────────────────────────────────────────
SHOW_CHANNEL_WATERMARK = False          # Show channel name watermark
WATERMARK_POSITION = "top-left"        # "top-left", "top-right", "bottom-left", "bottom-right"
WATERMARK_STYLE = "simple"             # "simple" (text only) or "badge" (with background)
WATERMARK_OPACITY = 0.75               # 0.0 (transparent) to 1.0 (opaque)

# ─────────────────────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────────────────────
LOG_LEVEL = "INFO"
LOG_FILE = OUTPUT_DIR / "generation.log"

# ═══════════════════════════════════════════════════════════════
#  VALIDATION
# ═══════════════════════════════════════════════════════════════
assert VID_WIDTH > 0 and VID_HEIGHT > 0
assert 0 <= MUSIC_VOLUME <= 1
assert FONT_SIZE >= 50
assert VIDEO_CRF >= 0 and VIDEO_CRF <= 51

print("[CONFIG] Configuration loaded")
print(f"         Video: {VID_WIDTH}x{VID_HEIGHT} @ {VID_FPS}fps")
print(f"         Duration: {DURATION_MODE} ({MAX_DURATION}s max, ~{TARGET_WORDS} words)")
print(f"         Background: Tier {BG_TIER} | Music: {MUSIC_MODE}")
print(f"         Mood SFX: {MOOD_SFX_ENABLED} | Character FX: {CHARACTER_AUDIO_FX_ENABLED}")
print(f"         Loop bridge: {ADD_LOOP_BRIDGE} | Hook: {SHOW_HOOK}")

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
ASSETS_DIR = BASE_DIR / "assets"

for _d in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, SFX_DIR, CACHE_DIR, ASSETS_DIR]:
    _d.mkdir(exist_ok=True)

# Create logs directory
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────
#  CHANNEL & LOGGING SETTINGS
# ─────────────────────────────────────────────────────────────
CHANNEL_NAME = "Snippet Stories"          # Your YouTube channel name
LOG_FILE = str(LOGS_DIR / "generate.log") # Log output file
LOG_LEVEL = "INFO"                        # CRITICAL, ERROR, WARNING, INFO, DEBUG

# ─────────────────────────────────────────────────────────────
#  VIDEO SETTINGS
# ─────────────────────────────────────────────────────────────
VID_WIDTH = 1080              # YouTube Shorts width
VID_HEIGHT = 1920             # YouTube Shorts height
VID_FPS = 60                  # Frames per second

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

# USE_LOCAL_TTS: If True, uses locally hosted AI voice generation
# (e.g. Kokoro-TTS) for emotional, cloned inflections.
# Requires: pip install kokoro soundfile torch
USE_LOCAL_TTS = True

# Local Kokoro-TTS voices (requires the Kokoro v1.0 voicepacks)
# "am" = American Male, "af" = American Female, "bm" = British Male, etc.
KOKORO_VOICES = {
    # ── Main Characters ──────────────────────────────────────
    "narrator":     "af_bella",       # Rich, dramatic female narrator
    "kaelen":       "am_puck",        # Deep, calm male protagonist
    "seraphina":    "bf_emma",        # Elegant British female
    "rin":          "af_nicole",      # Playful energetic female
    "elara":        "af_sarah",       # Warm thoughtful female
    "vex'ahlia":    "af_sky",         # Mysterious female
    # ── Secondary Characters ──────────────────────────────────
    "morwen":       "af_alloy",       # Stern female
    "valerius":     "am_eric",        # Arrogant male
    "gaius":        "bm_george",      # Wise British male
    "malachar":     "am_michael",     # Dark villain male
    "mara":         "af_alloy",       # Cold female
    "aldric":       "bm_lewis",       # Commanding male (The Lion)
    "duke":         "am_puck",        # Noble male
    "herald":       "am_adam",        # Formal male
    "guard":        "am_adam",        # Soldier male
    "instructor":   "am_michael",     # Teacher male
    "oracle":       "af_sky",         # Mystical female
    "arcturus":     "am_puck",        # Emperor's past voice
    "commander":    "am_michael",     # Military male
    "council":      "bm_george",      # Council member
    "inquisitor":   "af_alloy",       # Inquisitor female
    # ── Fallback ──────────────────────────────────────────────
    "_default":     "af_bella",       # Default fallback
}

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
    "narrator":     {"rate": "+25%", "pitch": "+0Hz"},     # Natural cinematic (fast-paced for retention)
    "kaelen":       {"rate": "+25%", "pitch": "+0Hz"},     # Slower, deeper (sped up for retention)
    "seraphina":    {"rate": "+20%", "pitch": "+5Hz"},     # Elevated elegant
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
WORDS_PER_CUE = 4               # Words shown at once (4 is good for full context)
FONT_NAME = "Bangers"           # Viral YouTube Shorts font
FONT_SIZE = 82                  # Adjusted for 4 words per cue
OUTLINE_WIDTH = 5               # Thick outline for contrast
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
# Tier 0 = Solid color / none
BG_TIER = 2                       # Changed to Tier 2 to use context-based Pexels clips (dopamine/nature/cinematic)
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
    "dark":     ["dark forest mist cinematic", "storm clouds time lapse", "dark ocean aerial", "ancient dark ruins architecture"],
    "sad":      ["rain on glass cinematic", "gloomy towering mountains", "foggy landscape cinematic", "dark nature aerial"],
    "thrill":   ["lightning strike slow motion", "fast moving clouds cinematic", "drone aerial city night", "flowing river dark"],
    "happy":    ["golden hour nature drone", "sunlight through tall trees cinematic", "clear blue sky time lapse", "beautiful waterfalls cinematic"],
    "epic":     ["epic mountain peaks aerial", "ancient castle fortress drone", "dramatic sunset clouds time lapse", "majestic architecture cinematic"],
    "surprise": ["lightning storm cinematic nature", "light rays through clouds", "fast moving river nature"],
    "mystery":  ["fog thick forest night", "dark architecture tunnel", "misty lake majestic aerial"],
    "neutral":  ["beautiful nature landscape cinematic", "majestic drone view mountains", "ancient architecture aerial"],
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
ADD_LOOP_BRIDGE = False             # ❌ DISABLED — Removes the confusing sound echo at the end
LOOP_BRIDGE_DURATION = 3.5        # Increased to capture "Hey everyone! Welcome back..."

# ─────────────────────────────────────────────────────────────
#  2026 UPGRADE FEATURES (Critical Improvements)
# ─────────────────────────────────────────────────────────────
USE_REAL_TIME_DURATION = True          # Measure actual TTS output (±20ms accuracy)
USE_FRAME_PERFECT_SUBTITLES = True     # Librosa speech detection for audio/subtitle sync
ADD_LOOP_TRANSITION = False            # ❌ DISABLED — YouTube algorithm prefers hard cut loops over fade to black
ADD_AI_DISCLOSURE = True               # ✅ ENABLED — YouTube 2026 compliance requirement
USE_CURATED_BACKGROUNDS = False        # ❌ DISABLED — so Pexels API fetches dynamic weather, nature, structures

AI_DISCLOSURE_POSITION = "top-right"   # or "bottom-left", "top-left", "bottom-right"
AI_DISCLOSURE_OPACITY = 0.85           # 0.0 (transparent) to 1.0 (opaque)

# ─────────────────────────────────────────────────────────────
#  BACKGROUND CONTENT FILTERING (Safety & Quality)
# ─────────────────────────────────────────────────────────────
# Only allow these natural/fantasy content types
ALLOWED_BACKGROUND_KEYWORDS = [
    # Nature
    "forest", "mountain", "landscape", "nature", "wilderness", "sky", "clouds",
    "ocean", "sea", "river", "waterfall", "valley", "canyon", "desert",
    "meadow", "field", "plains", "jungle", "rainforest", "cave", "peak", "volcano",
    # Wildlife
    "wildlife", "animal", "bird", "eagle", "wolf", "deer", "bear", "lion",
    "elephant", "horse", "butterfly", "fish", "underwater", "whale", "eagle",
    # Structures & Architecture
    "castle", "temple", "ruins", "architecture", "fortress", "mansion",
    "ancient", "historical", "monument", "stone", "bridge", "structure",
    # Abstract/Fantasy-friendly
    "abstract", "light", "fire", "smoke", "mist", "fog", "aurora", "space",
    "galaxy", "stars", "nebula", "cosmos", "magical", "dark", "epic"
]

# REJECT backgrounds with these keywords (content safety)
# Blocks humans, 3D particles, modern urban content, CGI
BLACKLIST_BACKGROUND_KEYWORDS = [
    # Humans & Body Parts (CRITICAL)
    "person", "people", "human", "face", "crowd", "man", "woman", "child", 
    "hands", "feet", "portrait", "walking", "talking", "couple", "tourist",
    "model", "girl", "boy",
    
    # Modern & Urban (Breaks Fantasy Immersion)
    "street", "city", "car", "traffic", "urban", "modern", "office", 
    "indoor", "room", "phone", "computer", "building", "neon", "skyscraper",
    "road", "highway", "laptop", "glass building", "subway",
    
    # Fake / Copyright / Unwanted Styles
    "3d", "3d render", "3d particle", "cgi", "animation", "cartoon", 
    "synthetic", "render", "blender", "unreal", "engine", "gaming", 
    "anime", "illustration", "drawing", "text", "watermark", "logo",
    
    # Unwanted Perspectives
    "timelapse", "hyperlapse", "vlog", "selfie"
]

LOCATION_KEYWORDS = {
    # ── Kaelen's Past & The Betrayal ──
    "obsidian fortress": "dark jagged stone castle stormy sky scenery nobody",
    "demon realm": "volcanic ash landscape dark sky scenery nobody",
    "dark throne": "ancient empty dark throne room stone scenery nobody",
    "battlefield": "foggy desolate battlefield ruins landscape scenery nobody",
    "holy sword": "sunlight breaking through dark clouds cinematic nobody",
    
    # ── Rebirth & The Ducal Estate ──
    "blinding white": "abstract ethereal white light clouds scenery nobody",
    "mahogany room": "vintage luxurious dark wood room interior scenery nobody",
    "chandelier": "elegant crystal chandelier dark room interior nobody",
    "manor": "grand ancient medieval mansion exterior scenery nobody",
    "estate": "beautiful vast medieval estate gardens scenery nobody",
    "study": "ancient dusty library old books candle light scenery nobody",
    
    # ── The Magic Academy (Interiors) ──
    "academy": "grand historical university architecture exterior scenery nobody",
    "classroom": "ancient empty gothic classroom wood desks scenery nobody",
    "library": "massive ancient library towering bookshelves scenery nobody",
    "hallway": "dark stone castle corridor arches scenery nobody",
    "dormitory": "simple medieval stone room window light scenery nobody",
    "dining hall": "grand long wooden table medieval feast hall scenery nobody",
    
    # ── The Magic Academy (Exteriors) ──
    "courtyard": "ancient stone courtyard gothic architecture scenery nobody",
    "training ground": "empty medieval dirt training yard weapons scenery nobody",
    "arena": "ancient roman colosseum ruins sand scenery nobody",
    "gates": "massive iron gates ancient castle entrance scenery nobody",
    
    # ── Nature & The Borderlands ──
    "dark forest": "creepy dark misty pine forest trees scenery nobody",
    "bright forest": "sunlight shining through green forest trees scenery nobody",
    "mountains": "majestic snow capped mountain peaks aerial scenery nobody",
    "valley": "beautiful green valley river landscape scenery nobody",
    "river": "fast flowing dark river nature landscape scenery nobody",
    "waterfall": "epic tall waterfall jungle nature scenery nobody",
    "borderlands": "desolate barren wasteland landscape stormy scenery nobody",
    "cave": "dark mysterious underground cave tunnel scenery nobody",
    "ruins": "ancient forgotten stone temple ruins overgrown scenery nobody",
    
    # ── The Royal Capital & The Church ──
    "capital": "epic medieval city aerial view sunset scenery nobody",
    "palace": "gleaming white marble palace exterior scenery nobody",
    "royal court": "grand majestic marble hall pillars scenery nobody",
    "golden throne": "luxurious golden throne room bright light scenery nobody",
    "cathedral": "massive gothic church interior stained glass scenery nobody",
    "sanctuary": "peaceful holy temple interior sunlight scenery nobody",
    
    # ── Abstract & Magic Elements ──
    "void": "dark swirling abstract smoke particles scenery nobody",
    "magic circle": "glowing abstract magical energy particles scenery nobody"
}


FILTER_BACKGROUND_CONTENT = True  # Enable content filtering for Pexels

# ─────────────────────────────────────────────────────────────
VIDEO_CODEC = "libx264"        # H.264 (universal YouTube compatibility)
VIDEO_PRESET = "medium"        # 'medium' maximizes video quality
VIDEO_CRF = 14                 # 14 = near visually lossless, ultra high quality (lower = better)
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
#  INTRO & OUTRO (DISABLED — kills retention)
#  Branding is now visual-only: watermark + CTA overlay
# ─────────────────────────────────────────────────────────────
ADD_INTRO = False                    # ❌ DISABLED — spoken intros cause instant swipe
ADD_OUTRO = False                    # ❌ DISABLED — spoken outros destroy loop bridge

# ─────────────────────────────────────────────────────────────
#  INTEGRATED CTA OVERLAY (visual only, during climax)
#  Shows text on screen during the final seconds WITHOUT
#  stopping the story or breaking the audio flow
# ─────────────────────────────────────────────────────────────
SHOW_CTA_OVERLAY = True              # ✅ Flash CTA text during the final seconds
CTA_TEXT = "Like & Subscribe for Part {next_part}!"
CTA_DURATION = 3.0                   # seconds, shown at the very end
CTA_FONT_SIZE = 52                   # Readable but not obnoxious
CTA_COLOR = "&H0000FFFF"             # Yellow (ASS format)

# ─────────────────────────────────────────────────────────────
#  PART TAG (top-left, first 4 seconds)
#  Viewers intuitively go to your channel to find Part 2
# ─────────────────────────────────────────────────────────────
SHOW_PART_TAG = True                 # ✅ Show "Part N" in the first seconds
PART_TAG_DURATION = 4.0              # seconds visible

# ─────────────────────────────────────────────────────────────
#  CHANNEL WATERMARK (Always visible — replaces spoken intro)
# ─────────────────────────────────────────────────────────────
SHOW_CHANNEL_WATERMARK = True          # ✅ ENABLED — persistent visual branding
WATERMARK_IMAGE = ASSETS_DIR / "watermark.png"  # Use channel watermark image
WATERMARK_POSITION = "top-left"        # "top-left", "top-right", "bottom-left", "bottom-right"
WATERMARK_SCALE = 120                  # Width in pixels (height auto-scaled)
WATERMARK_OPACITY = 0.70               # 0.0 (transparent) to 1.0 (opaque)
WATERMARK_MARGIN = 30                  # Pixels from edge

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
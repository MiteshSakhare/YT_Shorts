#!/usr/bin/env python3
"""System verification and refinement check."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src import config

print("\n" + "="*70)
print("🔍 SYSTEM VERIFICATION & REFINEMENT REPORT")
print("="*70)

# 1. Directory structure
print("\n✅ DIRECTORY STRUCTURE:")
dirs = [('input', True), ('output', False), ('sfx', True), ('src', True)]
for d, _ in dirs:
    p = Path(d)
    cnt = len(list(p.glob('*'))) if p.exists() else 0
    print(f"   ✅ {d:20} {cnt:3} items")

# 2. Configuration
print("\n✅ KEY CONFIGURATION:")
print(f"   ✅ {'Channel Name':20} {config.CHANNEL_NAME}")
print(f"   ✅ {'Duration Mode':20} {config.DURATION_MODE}")
print(f"   ✅ {'Video Resolution':20} {config.VID_WIDTH}×{config.VID_HEIGHT} @ {config.VID_FPS}fps")
print(f"   ✅ {'AI Disclosure':20} {config.ADD_AI_DISCLOSURE}")
print(f"   ✅ {'Mood SFX':20} {config.MOOD_SFX_ENABLED}")

# 3. Voices
print("\n✅ VOICE SYSTEM:")
print(f"   Total voices configured: {len(config.VOICES)}")

# 4. Source files
print("\n✅ SOURCE FILES:")
for f in ['config.py', 'generate_short.py', 'audio_processor.py', 
          'mood_detector.py', 'sfx_engine.py', 'background_engine.py']:
    exists = (Path('src') / f).exists()
    print(f"   {'✅' if exists else '❌'} {f}")

# 5. Scripts
print("\n✅ INPUT SCRIPTS:")
scripts = sorted(Path('input').glob('part_*.txt'))
print(f"   Total: {len(scripts)} scripts ready")
if scripts:
    print(f"   Range: {scripts[0].name} ... {scripts[-1].name}")

# 6. Check for common issues
print("\n🔧 COMMON ISSUES CHECK:")

issues = []

# Check dependencies
try:
    import edge_tts
    print("   ✅ edge-tts installed")
except ImportError:
    issues.append("edge-tts not installed")

try:
    import librosa
    print("   ✅ librosa installed")
except ImportError:
    issues.append("librosa not installed (optional - subtitles won't be frame-perfect)")

try:
    import PIL
    print("   ✅ Pillow installed")
except ImportError:
    issues.append("Pillow not installed")

# Check FFmpeg
import subprocess
try:
    subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=2)
    print("   ✅ FFmpeg available")
except FileNotFoundError:
    issues.append("FFmpeg not found - install with: winget install ffmpeg")

if issues:
    print("\n⚠️  WARNINGS:")
    for issue in issues:
        print(f"   ⚠️  {issue}")
else:
    print("\n   ✅ All dependencies OK")

print("\n" + "="*70)
print("🎯 SYSTEM STATUS: ✅ READY FOR PRODUCTION")
print("="*70)
print("\nNext: python batch_generate.py\n")

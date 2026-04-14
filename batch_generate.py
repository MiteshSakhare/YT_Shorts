#!/usr/bin/env python3
"""
Batch Generate Script - Process All 214 YouTube Shorts
Generates "The Twice-Crowned King" series with "Snippet Stories" branding
"""

import os
import subprocess
import time
import sys
from pathlib import Path

# Ensure src directory is in path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    input_dir = Path("input")
    output_dir = Path("output")
    
    # Get all part_XX_YY.txt files
    script_files = sorted([
        f for f in input_dir.glob("part_*.txt")
    ])
    
    if not script_files:
        print("❌ No scripts found in input/ directory")
        print("   Expected: input/part_01_01.txt, part_01_02.txt, etc.")
        sys.exit(1)
    
    total = len(script_files)
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     🎬 BATCH GENERATE - Snippet Stories YouTube Shorts        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    print(f"📝 Scripts found: {total}")
    print(f"⏱️  Estimated time: {total * 2.5 / 60:.1f} hours")
    print(f"🎬 Output folder: {output_dir.absolute()}")
    print()
    print("Features per video:")
    print("  ✅ Snippet Stories watermark")
    print("  ✅ AI-VOICED disclosure label")
    print("  ✅ Frame-perfect subtitles")
    print("  ✅ Mood-based SFX")
    print("  ✅ YouTube Shorts optimized (1080x1920, ~50sec)")
    print()
    
    response = input("Start batch generation? (yes/no): ").strip().lower()
    if response not in ["yes", "y"]:
        print("Cancelled.")
        sys.exit(0)
    
    print()
    print("🎬 Starting generation...")
    print()
    
    start_time = time.time()
    success_count = 0
    error_count = 0
    failed_scripts = []
    
    for i, script_path in enumerate(script_files, 1):
        script_name = script_path.name
        
        # Progress bar
        progress = f"[{i:3d}/{total}]"
        
        try:
            # Run generator with src in PYTHONPATH
            env = os.environ.copy()
            env['PYTHONPATH'] = str(Path(__file__).parent)
            
            result = subprocess.run(
                ["python", "src/generate_short.py", str(script_path)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=300,  # 5 minute timeout per video
                env=env,
                cwd=str(Path(__file__).parent)  # Run from project root
            )
            
            if result.returncode == 0:
                print(f"{progress} ✅ {script_name}")
                success_count += 1
            else:
                print(f"{progress} ❌ {script_name} (non-zero exit)")
                error_count += 1
                failed_scripts.append(script_name)
                
        except subprocess.TimeoutExpired:
            print(f"{progress} ⏱️  {script_name} (timeout - skipped)")
            error_count += 1
            failed_scripts.append(script_name)
        except Exception as e:
            print(f"{progress} ❌ {script_name} ({str(e)[:40]})")
            error_count += 1
            failed_scripts.append(script_name)
    
    # Summary
    elapsed = time.time() - start_time
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                    BATCH GENERATION COMPLETE                  ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    print(f"✅ Success: {success_count}/{total}")
    print(f"❌ Failed:  {error_count}/{total}")
    print(f"⏱️  Time: {elapsed/3600:.2f} hours ({elapsed/60:.0f} minutes)")
    print()
    
    if error_count > 0:
        print("Failed scripts:")
        for script in failed_scripts[:10]:
            print(f"  - {script}")
        if len(failed_scripts) > 10:
            print(f"  ... and {len(failed_scripts) - 10} more")
    
    print()
    print(f"📂 Videos saved to: {output_dir}")
    print()
    
    # Calculate video count
    video_count = len(list(output_dir.glob("short_part_*_disclosed.mp4")))
    print(f"🎬 Total videos ready: {video_count}")
    print()
    
    if success_count == total:
        print("🎉 ALL VIDEOS GENERATED SUCCESSFULLY!")
        print()
        print("Next steps:")
        print("  1. Review videos: output/short_part_01_01_disclosed.mp4")
        print("  2. Upload to YouTube:")
        print("     - Channel name: Snippet Stories")
        print("     - Schedule 2x daily uploads")
        print("     - Monitor analytics")
    else:
        print(f"⚠️  {error_count} videos failed. Retry with:")
        print("  python batch_generate.py")
    
    print()

if __name__ == "__main__":
    main()

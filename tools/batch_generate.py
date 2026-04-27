#!/usr/bin/env python3
"""
Batch Generate Script - Process All YouTube Shorts
Generates "The Twice-Crowned King" series with "Snippet Stories" branding

Usage (from project root):
    python tools/batch_generate.py
    python tools/batch_generate.py --start 10 --end 20
"""

import os
import subprocess
import time
import sys
import argparse
from pathlib import Path

# Project root is one level up from tools/
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    parser = argparse.ArgumentParser(description="Batch generate YouTube Shorts")
    parser.add_argument("--start", type=int, default=1, help="Start part number")
    parser.add_argument("--end", type=int, default=None, help="End part number (inclusive)")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()

    input_dir = PROJECT_ROOT / "input"
    output_dir = PROJECT_ROOT / "output"

    # Get all part_XXXX.txt files
    script_files = sorted([f for f in input_dir.glob("part_*.txt")])

    if not script_files:
        print("❌ No scripts found in input/ directory")
        print("   Expected: input/part_0001.txt, part_0002.txt, etc.")
        sys.exit(1)

    # Filter by range
    if args.end:
        script_files = script_files[args.start - 1 : args.end]
    elif args.start > 1:
        script_files = script_files[args.start - 1 :]

    total = len(script_files)
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     🎬 BATCH GENERATE — Snippet Stories YouTube Shorts       ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    print(f"📝 Scripts to process: {total}")
    print(f"⏱️  Estimated time: {total * 2.5 / 60:.1f} hours")
    print(f"🎬 Output folder: {output_dir.absolute()}")
    print()

    if not args.yes:
        response = input("Start batch generation? (yes/no): ").strip().lower()
        if response not in ["yes", "y"]:
            print("Cancelled.")
            sys.exit(0)

    print("\n🎬 Starting generation...\n")

    start_time = time.time()
    success_count = 0
    error_count = 0
    failed_scripts = []

    for i, script_path in enumerate(script_files, 1):
        script_name = script_path.name
        progress = f"[{i:3d}/{total}]"

        try:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(PROJECT_ROOT)

            result = subprocess.run(
                [sys.executable, str(PROJECT_ROOT / "src" / "generate_short.py"), str(script_path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
                env=env,
                cwd=str(PROJECT_ROOT),
            )

            if result.returncode == 0:
                print(f"{progress} ✅ {script_name}")
                success_count += 1
            else:
                print(f"{progress} ❌ {script_name} (non-zero exit)")
                error_count += 1
                failed_scripts.append(script_name)

        except subprocess.TimeoutExpired:
            print(f"{progress} ⏱️  {script_name} (timeout — skipped)")
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

    if failed_scripts:
        print("Failed scripts:")
        for script in failed_scripts[:10]:
            print(f"  - {script}")
        if len(failed_scripts) > 10:
            print(f"  ... and {len(failed_scripts) - 10} more")

    print(f"\n📂 Videos saved to: {output_dir}")

    video_count = len(list(output_dir.glob("short_part_*.mp4")))
    print(f"🎬 Total videos ready: {video_count}\n")

    if success_count == total:
        print("🎉 ALL VIDEOS GENERATED SUCCESSFULLY!")
    elif error_count > 0:
        print(f"⚠️  {error_count} videos failed. Retry failed parts individually.")


if __name__ == "__main__":
    main()
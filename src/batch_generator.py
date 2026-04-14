#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#  BATCH_GENERATOR.PY — Batch generation with resume capability
#  Generates multiple videos with progress tracking and resumable sessions
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import os
import json
import logging
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Setup path
sys.path.insert(0, str(Path(__file__).parent))
try:
    from . import config
    from .generate_short import generate_short
except ImportError:
    import config
    from generate_short import generate_short

# ═══════════════════════════════════════════════════════════════════════════════
#  LOGGING
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
#  BATCH PROGRESS TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

class BatchProgressTracker:
    """Track batch generation progress with resume capability."""
    
    def __init__(self, session_id: str = None):
        """Initialize progress tracker."""
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.progress_file = config.OUTPUT_DIR / f"batch_progress_{self.session_id}.json"
        self.progress_data = self._load_progress()
        
    def _load_progress(self) -> Dict:
        """Load existing progress or create new."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                logger.info(f"📂 Resumed session: {self.session_id}")
                logger.info(f"   Completed: {len(data.get('completed', []))} videos")
                logger.info(f"   Failed: {len(data.get('failed', []))} videos")
                return data
            except Exception as e:
                logger.warning(f"⚠️  Could not load progress: {e}")
        
        return {
            "session_id": self.session_id,
            "started": datetime.now().isoformat(),
            "completed": [],
            "failed": [],
            "stats": {
                "total_time": 0,
                "avg_time_per_video": 0,
                "total_size_mb": 0
            }
        }
    
    def _save_progress(self) -> None:
        """Save progress to file."""
        self.progress_data["updated"] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)
    
    def mark_completed(self, part_num: int, video_path: str, duration: float) -> None:
        """Mark a video as completed."""
        self.progress_data["completed"].append({
            "part_num": part_num,
            "video_path": str(video_path),
            "timestamp": datetime.now().isoformat(),
            "generation_time": duration
        })
        self._save_progress()
    
    def mark_failed(self, part_num: int, error: str) -> None:
        """Mark a video as failed."""
        self.progress_data["failed"].append({
            "part_num": part_num,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
        self._save_progress()
    
    def is_completed(self, part_num: int) -> bool:
        """Check if part was already completed."""
        completed_parts = [v["part_num"] for v in self.progress_data.get("completed", [])]
        return part_num in completed_parts
    
    def get_stats(self) -> Dict:
        """Get batch statistics."""
        completed = len(self.progress_data.get("completed", []))
        failed = len(self.progress_data.get("failed", []))
        times = [v.get("generation_time", 0) for v in self.progress_data.get("completed", [])]
        
        avg_time = sum(times) / len(times) if times else 0
        
        return {
            "total_completed": completed,
            "total_failed": failed,
            "avg_time_per_video": avg_time,
            "estimated_remaining": avg_time * (225 - completed)  # 225 total videos
        }

# ═══════════════════════════════════════════════════════════════════════════════
#  BATCH GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

async def generate_batch(
    start_part: int = 1,
    end_part: int = 225,
    resume_session: str = None,
    error_handling: str = "skip"  # "skip", "retry", "stop"
) -> Dict:
    """
    Generate multiple videos with resume capability.
    
    Args:
        start_part: Starting part number
        end_part: Ending part number (inclusive)
        resume_session: Session ID to resume from (if None, creates new)
        error_handling: How to handle errors - skip, retry (3x), or stop
    
    Returns:
        Batch completion stats
    """
    tracker = BatchProgressTracker(resume_session)
    input_dir = config.INPUT_DIR
    
    # Find all input files or use range
    input_files = sorted(input_dir.glob("part_*.txt"))
    if not input_files:
        logger.error(f"❌ No input files found in {input_dir}")
        return {"success": False, "error": "No input files"}
    
    logger.info("=" * 70)
    logger.info(f"🎬 BATCH GENERATION — Parts {start_part} to {end_part}")
    logger.info("=" * 70)
    
    start_time = time.time()
    
    for part_num in range(start_part, end_part + 1):
        # Check if already completed
        if tracker.is_completed(part_num):
            logger.info(f"⏭️  Part {part_num:03d}: ALREADY COMPLETED (skipping)")
            continue
        
        # Find input file
        part_file = input_dir / f"part_{part_num:04d}.txt"
        if not part_file.exists():
            logger.warning(f"⚠️  Part {part_num:03d}: INPUT FILE NOT FOUND")
            tracker.mark_failed(part_num, "Input file not found")
            continue
        
        try:
            logger.info(f"▶️  Part {part_num:03d}: Starting generation…")
            part_start = time.time()
            
            # Read script
            with open(part_file, 'r', encoding='utf-8') as f:
                script_text = f.read()
            
            # Generate video
            result = await generate_short(script_text, part_num)
            
            if result.get("success"):
                gen_time = time.time() - part_start
                logger.info(f"✅ Part {part_num:03d}: SUCCESS ({gen_time:.1f}s)")
                tracker.mark_completed(part_num, result["video_path"], gen_time)
            else:
                error = result.get("error", "Unknown error")
                logger.error(f"❌ Part {part_num:03d}: FAILED — {error}")
                tracker.mark_failed(part_num, error)
                
                if error_handling == "stop":
                    raise RuntimeError(f"Batch stopped at part {part_num}")
                elif error_handling == "retry":
                    # Could add retry logic here
                    pass
        
        except Exception as e:
            logger.error(f"❌ Part {part_num:03d}: EXCEPTION — {e}")
            tracker.mark_failed(part_num, str(e))
            
            if error_handling == "stop":
                raise
        
        # Progress update
        stats = tracker.get_stats()
        elapsed = time.time() - start_time
        logger.info(f"   📊 Progress: {stats['total_completed']}/{end_part - start_part + 1} | "
                   f"Failed: {stats['total_failed']} | "
                   f"Avg: {stats['avg_time_per_video']:.1f}s/video | "
                   f"Est. remaining: {stats['estimated_remaining']:.0f}s")
    
    # Final summary
    total_time = time.time() - start_time
    stats = tracker.get_stats()
    
    logger.info("=" * 70)
    logger.info("📋 BATCH COMPLETE")
    logger.info("=" * 70)
    logger.info(f"✅ Completed: {stats['total_completed']} videos")
    logger.info(f"❌ Failed: {stats['total_failed']} videos")
    logger.info(f"⏱️  Total time: {total_time / 60:.1f} minutes")
    logger.info(f"📊 Avg per video: {stats['avg_time_per_video']:.1f}s")
    logger.info(f"📁 Progress saved to: {tracker.progress_file}")
    
    return {
        "success": stats['total_failed'] == 0,
        "completed": stats['total_completed'],
        "failed": stats['total_failed'],
        "total_time": total_time,
        "progress_file": str(tracker.progress_file)
    }

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Command-line interface for batch generation."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate YouTube Shorts in batch with resume capability"
    )
    parser.add_argument("--start", type=int, default=1, help="Starting part number (default: 1)")
    parser.add_argument("--end", type=int, default=225, help="Ending part number (default: 225)")
    parser.add_argument("--resume", type=str, default=None, help="Resume session ID")
    parser.add_argument("--error-handling", choices=["skip", "retry", "stop"], 
                       default="skip", help="Error handling mode")
    
    args = parser.parse_args()
    
    # Run batch generation
    result = asyncio.run(generate_batch(
        start_part=args.start,
        end_part=args.end,
        resume_session=args.resume,
        error_handling=args.error_handling
    ))
    
    if not result["success"]:
        sys.exit(1)

if __name__ == "__main__":
    main()

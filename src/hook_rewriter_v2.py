#!/usr/bin/env python3
"""
AI Hook Rewriter v2 — Batch Rewrite Opening Sentences
Uses Ollama (local LLM) to create viral hooks for each short
"""

import os
import requests
from pathlib import Path
import re
import sys

INPUT_DIR = Path('input')
OUTPUT_DIR = Path('output')

# Create output dir for rewritten files
(OUTPUT_DIR / "hooks").mkdir(exist_ok=True)

def check_ollama_server():
    """Check if Ollama server is running."""
    try:
        response = requests.get('http://localhost:11434/', timeout=2)
        return True
    except:
        return False


def rewrite_hook(original_hook: str, context: str = "epic fantasy") -> str:
    """
    Use Ollama to rewrite a hook into something viral.
    
    Args:
        original_hook: Original first sentence
        context: Story context (e.g. "epic fantasy")
    
    Returns: Rewritten hook or original if failed
    """
    prompt = f"""You are a viral YouTube Shorts script writer specializing in {context} content.

TASK: Rewrite this opening sentence into an intense, captivating hook that makes people STOP scrolling.

Original: "{original_hook}"

New hook (1-2 sentences, punchy, mysterious):"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            new_hook = result.get('response', '').strip()
            
            # Clean up
            new_hook = new_hook.replace('"', '').strip()
            new_hook = ' '.join(new_hook.split())
            
            # Remove if it's just echoing instructions
            if 'original' not in new_hook.lower() and len(new_hook) > 5 and len(new_hook) < 500:
                return new_hook
        else:
            return None
    except Exception as e:
        return None
    
    return None


def extract_first_sentence(text: str) -> str:
    """Extract the first complete sentence from text."""
    # Remove chapter headers
    text = re.sub(r'^#.*?\n', '', text).strip()
    text = re.sub(r'^NARRATOR:\s*', '', text, flags=re.IGNORECASE).strip()
    
    # Find first sentence
    match = re.match(r'([^.!?]*[.!?])', text)
    if match:
        return match.group(1).strip()
    
    # Fallback: first 20 words
    words = text.split()[:20]
    return ' '.join(words) + ('.' if words else '')


def rewrite_script_hook(input_file: Path, verbose: bool = False) -> bool:
    """
    Rewrite the hook in a script file.
    
    Returns: True if successful, False otherwise
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract original hook
        original_hook = extract_first_sentence(content)
        if not original_hook or len(original_hook) < 5:
            if verbose:
                print(f"     [-] No valid hook found in {input_file.name}")
            return False
        
        # Rewrite with Ollama
        new_hook = rewrite_hook(original_hook)
        
        if not new_hook:
            if verbose:
                print(f"     [-] Ollama returned empty response for {input_file.name}")
            return False
        
        # Clean up the new hook - it might have quotes
        new_hook = new_hook.strip().strip('"').strip("'")
        
        # Replace hook in content
        # Find the NARRATOR: section
        narrator_match = re.search(r'(NARRATOR:\s*)', content, re.IGNORECASE)
        if not narrator_match:
            if verbose:
                print(f"     [-] No NARRATOR: found in {input_file.name}")
            return False
        
        narrator_pos = narrator_match.end()
        content_after_narrator = content[narrator_pos:]
        
        # Find first sentence inside NARRATOR section
        first_sentence_match = re.match(r'([^.!?]*[.!?])', content_after_narrator)
        
        if first_sentence_match:
            old_hook = first_sentence_match.group(1).strip()
            
            # Make sure we have different content
            if old_hook.lower() == new_hook.lower():
                if verbose:
                    print(f"     [-] New hook same as old, skipping {input_file.name}")
                return False
            
            # Replace old hook with new one - ensure punctuation
            if not new_hook.endswith(('.', '!', '?')):
                new_hook = new_hook + '.'
            
            updated_content = (
                content[:narrator_pos]
                + new_hook + content_after_narrator[len(old_hook):]
            )
            
            # Save rewritten file
            output_file = OUTPUT_DIR / "hooks" / input_file.name
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            if verbose:
                print(f"   [+] {input_file.name}")
                print(f"      Original: {old_hook[:60]}...")
                print(f"      Rewritten: {new_hook[:60]}...")
            
            return True
        else:
            if verbose:
                print(f"     [-] Could not parse NARRATOR section in {input_file.name}")
            return False
            
    except Exception as e:
        if verbose:
            print(f"   [-] Exception in {input_file.name}: {type(e).__name__}: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("[*] AI HOOK REWRITER v2 - Viral Hook Generator")
    print("="*70)
    
    # Check Ollama
    print("\n[*] Checking for Ollama server...")
    if not check_ollama_server():
        print("""
❌ Ollama is NOT running!

To use this tool:
1. Download Ollama from: https://ollama.ai
2. Install and run: ollama serve
3. In another terminal, pull a model: ollama pull deepseek-coder
   (or: ollama pull llama2, ollama pull mistral)
4. Then run this script again

Without Ollama, hooks will not be rewritten.
        """)
        return
    
    print("[+] Ollama is running!")
    
    # Get all input scripts
    script_files = sorted([f for f in INPUT_DIR.glob("part_*.txt")])
    
    if not script_files:
        print("\n[-] No scripts found in input/ directory")
        return
    
    print(f"\n[*] Found {len(script_files)} scripts to process")
    
    # Process all scripts
    success_count = 0
    failed_count = 0
    
    for i, script_file in enumerate(script_files, 1):
        part_num = i
        verbose = i <= 3  # Show details for first 3 items
        
        if verbose:
            print(f"\n[{part_num:3d}/{len(script_files)}] Processing {script_file.name}...")
        
        if rewrite_script_hook(script_file, verbose=verbose):
            success_count += 1
            if not verbose:
                print(f"[{part_num:3d}/{len(script_files)}] [+] {script_file.name}")
        else:
            failed_count += 1
            if not verbose:
                print(f"[{part_num:3d}/{len(script_files)}] [-] {script_file.name}")
    
    # Summary
    print("\n" + "="*70)
    print("[*] HOOK REWRITING COMPLETE")
    print("="*70)
    print(f"\n[+] Successful: {success_count}/{len(script_files)}")
    print(f"[-] Failed: {failed_count}/{len(script_files)}")
    print(f"\n[*] Rewritten scripts saved to: {OUTPUT_DIR / 'hooks'}")
    print("\nNext steps:")
    print("  1. Review rewritten hooks: output/hooks/")
    print("  2. Copy your favorites back to input/ directory")
    print("  3. Run batch generator: python batch_generate.py")
    

if __name__ == "__main__":
    main()
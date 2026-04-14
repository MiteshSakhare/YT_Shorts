# 🚀 YouTube Shorts Production — Advanced Tips & 2026 Strategy

This guide contains strategies to help you scale your channel and improve the quality of your AI-generated shorts.

## 🎭 Character Audio & Voices
The system currently uses **Character Memory**. This means every character has a consistent voice across all 48 parts. 

| Character | Voice Role | Processing |
|-----------|------------|------------|
| NARRATOR | Deep, clear | Warm EQ + Compressor |
| KAELEN | Mysterious | Low-pass filter + Bass boost |
| Duke Arcturus| Booming, angry | Overdrive + High Gain |

> [!TIP]
> **Customizing Voices:** You can change these in `src/config.py` under the `VOICES` dictionary. Use `edge-tts --list-voices` in your terminal to see all available options.

## 🧠 Mood Detection Magic
The system detects keywords like "blood", "fire", "sad", or "victory" to change:
1. **Backgrounds:** Search terms for Pexels are updated automatically (e.g., searching for "dark fire" instead of just "fire").
2. **SFX:** Whooshes, booms, and atmospheric drones are added only when the mood changes.

## 📈 2026 Strategy Feed
To maximize your growth on the new decoupled YouTube Shorts algorithm:

*   **The Bridge Loop:** The script automatically adds a 2-second "bridge" at the end to make the video loop perfectly. This "infinite loop" increases your **Average View Duration** significantly.
*   **The Hook:** Step 8 generates a high-contrast text overlay (`hook.png`) for the first 3 seconds. This is critical to stop the scroll.
*   **The Comment Loop:** Always pin a question (AI generates a suggestion in the upload checklist) to spark high-engagement debate in the comments.

## 🛠 Project Roadmap (Update Suggestions)
If you want to upgrade the system further, here are my top 3 recommendations:

1. **Auto-Parting:** Modify the script to take a 5,000-word text dump and automatically slice it into Part 1, 2, 3... and generate them all overnight.
2. **ComfyUI Integration (Tier 3):** Instead of Pexels stock footage, use Stable Diffusion to generate custom 2D/3D background animations specifically for your characters.
3. **Face-Swap Sync:** Add a module to animate the character's mouth specifically when they speak, rather than just using generic background video.

---
*Created by Antigravity — Your AI Production Partner.*

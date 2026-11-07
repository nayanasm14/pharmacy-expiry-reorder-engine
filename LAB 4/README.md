# Lab 4 - Vibe Coding: Whack-a-Mole

Assigned starter: https://github.com/SETAPESU26/48_whack-a-mole

## Tasks implemented
1. **Collision detection:** hitboxes are reduced so adjacent holes do not overlap. The click handler also selects no more than one active mole per click, even if hitboxes overlap unexpectedly.
2. **Game Over:** when the countdown reaches zero, a graphical end screen displays the final score and best score.
3. **Replay and difficulty:** Easy, Medium, and Hard are selectable from on-screen buttons or keyboard keys 1/2/3. Each mode changes mole spawn rate and visible duration.
4. **Sound feedback:** generated short sound effects play for successful hits, missed clicks, and round end. Audio is optional; if the audio device is unavailable, the game remains playable silently.

## Run
```bash
python -m pip install -r requirements.txt
python main.py
```

## Tests
```bash
python -m unittest discover -s tests -v
```

The included tests use a lightweight Pygame stub to test logic without opening an SDL window. Live GUI and audio playback still need to be checked on the target Mac.

## Submission evidence
The handout requires authentic 10-second gameplay videos before and after the changes, updated code, and an exported Chat/LLM history. Add `before.mp4` and `after.mp4` after recording the real game on your Mac. See `VIDEO_CAPTURE_GUIDE.md`. The attached Chat_History_Lab4.pdf is a session summary of the AI-assisted implementation, not a complete native ChatGPT data export; include the actual conversation share/export as required by your instructor.

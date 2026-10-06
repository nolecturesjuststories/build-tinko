# ⏰ 7:00 AM: Tinko wakes up. Does he remember Rohan's favorite pizza?
# Short-term memory = the "whiteboard" (the chat messages). It gets wiped.
# Long-term memory  = a diary file on disk. It survives a restart.
import json
from pathlib import Path

from toy_brain import ToyBrain

DIARY = Path(__file__).with_name("tinko_diary.json")   # lives next to this file
brain = ToyBrain()


def save_note(note):
    notes = load_diary()
    if note not in notes:              # don't write the same note twice
        notes.append(note)
    DIARY.write_text(json.dumps(notes, indent=2))


def load_diary():
    if DIARY.exists():
        return json.loads(DIARY.read_text())
    return []


def search_diary(word):
    # Tiny search: keep every note that contains the word.
    return [n for n in load_diary() if word in n.lower()]


question = "What is Rohan's favorite pizza?"

print("📅 Last night, Rohan told Tinko something important...")
whiteboard = [{"role": "user", "content": "Note: favorite pizza = paneer"}]
save_note("favorite pizza = paneer")          # also written in the diary!
save_note("Grandma lands at 6 pm")

print("😴 Tinko restarts. The whiteboard is wiped.")
whiteboard = []                                # short-term memory: gone
whiteboard.append({"role": "user", "content": question})
print("🤖 Without memory:", brain.reply(whiteboard))

print("\n📖 Now Tinko checks his diary first...")
found = search_diary("pizza")
print("   Diary search for 'pizza' found:", found)
whiteboard = [{"role": "user", "content": "Note: " + n} for n in found]
whiteboard.append({"role": "user", "content": question})
print("🤖 With memory:", brain.reply(whiteboard))
print(f"\n💾 The diary is saved in {DIARY.name}. Run me again: it's still there!")

# 🔁 Make it real: swap ToyBrain() for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B4 Memory

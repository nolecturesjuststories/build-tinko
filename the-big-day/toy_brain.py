"""
🧸 ToyBrain: a PRETEND brain (a fake LLM).

This is a pretend brain so you can run everything with no setup:
no internet, no API keys, no installs. It only follows a few keyword rules.

A real AI (an LLM) reads your words and *predicts* a good reply.
ToyBrain just checks "does the message contain this word?". But it talks
the same way a real AI does, so every scene's code stays the same:
  - plain text  -> "here is my answer"
  - JSON text   -> a tool call: "please run this function for me"
"""
import json


class ToyBrain:
    def __init__(self, rules=None):
        # rules = {"keyword": "reply"}. Each scene can teach the brain a few.
        self.rules = rules or {}

    def reply(self, messages_or_text):
        # Real AI APIs take a list of chat messages: [{"role": ..., "content": ...}].
        # For convenience we also accept one plain string.
        if isinstance(messages_or_text, str):
            messages = [{"role": "user", "content": messages_or_text}]
        else:
            messages = messages_or_text
        last = messages[-1]["content"].lower()

        # 1) Is there a note on the whiteboard? Answer from it (memory + RAG).
        for message in messages:
            for line in message["content"].splitlines():
                if line.lower().startswith("note:"):
                    return "From my notes: " + line[5:].strip()

        # 2) Rules this scene taught me. The first keyword that matches wins.
        for keyword, answer in self.rules.items():
            if keyword in last:
                return answer

        # 3) A pizza order becomes a tool call (JSON "order slip").
        if "pizza" in last and "order" in last:
            size = "large" if "large" in last else "medium"
            topping = "paneer" if "paneer" in last else "cheese"
            return json.dumps({"tool": "order_pizza", "size": size, "topping": topping})

        # 4) No rule matched. An honest toy brain says so.
        return "Hmm, I'm only a toy brain. I don't know that one yet!"

    # Agent code often says "think". Same thing, friendlier name.
    think = reply


if __name__ == "__main__":
    brain = ToyBrain()
    print("🧸 ToyBrain says:", brain.reply("Hi Tinko!"))
    print("🧸 ToyBrain says:", brain.reply("Order me a large paneer pizza"))

# 🔁 Make it real: swap ToyBrain() for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B1–B3 Your first agent

# ⏰ 12:00 PM: Lunch! Tinko orders Rohan's birthday pizza.
# The big secret of tool calling: the AI never runs anything itself.
# It only writes an "order slip" (JSON text). YOUR code reads the slip
# and runs the real function. Then the result goes back to the AI.
import json

from toy_brain import ToyBrain

brain = ToyBrain()


def order_pizza(size, topping):                 # a tool = just a function
    return f"{size} {topping} pizza arrives at 8 pm"


TOOLS = {"order_pizza": order_pizza}            # name -> function

print("🙋 Rohan: Order me a large paneer pizza")
slip = brain.reply("Order me a large paneer pizza")
print("🧾 The brain wrote an order slip (just text!):")
print("   ", slip)

call = json.loads(slip)                          # text -> Python dict
print("📦 Parsed into a dict:", call)

result = TOOLS[call.pop("tool")](**call)
# What that line does, step by step:
#   call.pop("tool")   -> "order_pizza" (and removes it from the dict)
#   TOOLS[...]         -> the order_pizza function
#   (**call)           -> order_pizza(size="large", topping="paneer")
print("🍕 Tool result:", result)

# The result goes back to the brain, so it can tell Rohan in plain words.
messages = [
    {"role": "user", "content": "Order me a large paneer pizza"},
    {"role": "tool", "content": result},
]
brain.rules["arrives"] = "Done! Your large paneer pizza arrives at 8 pm. 🎂"
print("🤖 Tinko:", brain.reply(messages))

# 🔁 Make it real: swap ToyBrain() for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B2 Tool calling

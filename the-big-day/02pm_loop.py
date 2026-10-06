# ⏰ 2:00 PM: Baking Rohan's birthday cake.
# The agent loop: THINK (what next?) -> ACT (do it) -> CHECK (did it work?)
# ...and repeat until the job is done. Like a real cook tasting as they go.
import json

from toy_brain import ToyBrain

batter = {"thickness": "too thick"}           # the kitchen's "state"


def add_ingredients():
    return "ingredients added"

def mix():
    return f"mixed. Batter is {batter['thickness']}"

def add_milk():
    batter["thickness"] = "smooth"
    return "milk added"

def bake():
    return "cake baked, smells amazing"

TOOLS = {"add_ingredients": add_ingredients, "mix": mix,
         "add_milk": add_milk, "bake": bake}

# Toy rules: "after THIS happens, do THAT next".
brain = ToyBrain(rules={
    "bake a cake": json.dumps({"tool": "add_ingredients"}),
    "ingredients added": json.dumps({"tool": "mix"}),
    "too thick": json.dumps({"tool": "add_milk"}),   # the check says: try again!
    "milk added": json.dumps({"tool": "mix"}),
    "smooth": json.dumps({"tool": "bake"}),
    "baked": "DONE: the cake is ready! 🎂",
})

MAX_STEPS = 10                    # safety: never loop forever
messages = [{"role": "user", "content": "Please bake a cake for Rohan"}]
done = False
steps = 0
while not done:
    reply = brain.think(messages)                       # 🧠 THINK
    steps += 1
    if reply.startswith("DONE"):                         # 🛑 stop condition
        print(f"✅ {reply} ({steps - 1} actions, then one last think to decide it's done)")
        done = True
    elif steps >= MAX_STEPS:                             # 🛑 safety stop
        print("⚠️ Too many steps. Stopping to stay safe.")
        done = True
    else:
        call = json.loads(reply)
        result = TOOLS[call["tool"]]()                   # 🛠️ ACT
        print(f"Step {steps}: 🛠️ {call['tool']:<15} 🔍 {result}")   # CHECK
        messages.append({"role": "tool", "content": result})

# 🔁 Make it real: swap ToyBrain() for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B3 The agent loop

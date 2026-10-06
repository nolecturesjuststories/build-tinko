# ⏰ 7:30 AM: Grandma needs a flight for Diwali. Tinko books it.
# An agent = a brain + tools + a loop that keeps going until the goal is done.
import json

from toy_brain import ToyBrain


# 🧰 Tools are just ordinary Python functions.
def search_flights(city):
    return f"Found flight AI-202 from {city}, lands 6 pm"

def check_calendar(day):
    return f"Calendar is free on {day} evening"

def book_flight(flight):
    return f"Booked {flight}! Ticket sent to Grandma"

TOOLS = {"search_flights": search_flights,
         "check_calendar": check_calendar,
         "book_flight": book_flight}

# The toy brain's rules: "when I see THIS, my next move is THAT".
# A real AI figures these steps out by itself.
brain = ToyBrain(rules={
    "goal:":       json.dumps({"tool": "search_flights", "city": "Jaipur"}),
    "found flight": json.dumps({"tool": "check_calendar", "day": "Saturday"}),
    "is free":     json.dumps({"tool": "book_flight", "flight": "AI-202"}),
    "booked":      "DONE: Grandma's flight is booked. She lands at 6 pm! 🎉",
})

messages = [{"role": "user", "content": "Goal: book Grandma's flight for Diwali"}]
done = False
step = 0
while not done and step < 10:                 # 10 = safety limit
    step += 1
    reply = brain.think(messages)              # 🧠 THINK
    print(f"\nStep {step}")
    print("  🧠 think:", reply)
    if reply.startswith("DONE"):               # ✅ CHECK: is the goal done?
        done = True
        print("  ✅ check: goal reached, stopping.")
        break
    call = json.loads(reply)                   # 🛠️ ACT: run the tool
    result = TOOLS[call.pop("tool")](**call)
    print("  🛠️  act:  ", result)
    print("  🔍 check: not done yet, keep going...")
    messages.append({"role": "tool", "content": result})

# 🔁 Make it real: swap ToyBrain() for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B1–B3 Your first agent

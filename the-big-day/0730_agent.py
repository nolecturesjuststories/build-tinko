# ⏰ 7:30 AM: Grandma needs a flight for Diwali. Tinko books it.
# An agent = a brain + tools + a loop that keeps going until the goal is done.
import json

from toy_brain import ToyBrain


# 🧰 Tools are just ordinary Python functions.
# In real life each one calls a real service's API (a flight search, a calendar
# like Google Calendar, an airline's booking system). Here they return pretend answers.
def search_flights(date):
    return "Three flights found: 6 PM, 7 PM, 8 PM"

def calendar_free_times(person):
    return f"{person} is free after 7 PM"

def airline_book(flight, seats):
    return f"Seat 12A confirmed on the {flight} flight ({seats} seat)"

TOOLS = {"search_flights": search_flights,
         "calendar_free_times": calendar_free_times,
         "airline_book": airline_book}

# The toy brain's rules: "when I see THIS, my next move is THAT".
# A real AI figures these steps out by itself.
brain = ToyBrain(rules={
    "goal:":         json.dumps({"tool": "search_flights", "date": "today"}),
    "flights found": json.dumps({"tool": "calendar_free_times", "person": "Rohan"}),
    "free after":    json.dumps({"tool": "airline_book", "flight": "8 PM", "seats": 1}),
    "confirmed":     "DONE: Grandma's flight is booked. Seat 12A, she lands at 8 PM! 🎉",
})

messages = [{"role": "user", "content": "Goal: book Grandma's flight for tonight's party"}]
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

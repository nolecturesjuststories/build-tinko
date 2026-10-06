# ⏰ 6:30 PM: Tinko gets excited and tries to order 100 pizzas. Uh oh.
# Guardrails = safety rules written in CODE, not just asked for in the prompt.
# A brain can ignore a polite request. It can't skip an if-statement.
import json
import sys

from toy_brain import ToyBrain

# Rule 1: guardrails. Hard limits Tinko can never cross, no matter what.
MAX_PIZZAS = 5
MAX_RUPEES = 2000


def ask_human(question):
    # Human-in-the-loop: a person says yes or no before anything risky.
    if "--yes" in sys.argv or not sys.stdin.isatty():
        print(f"🙋 {question} (y/n) y   [auto-yes for the demo]")
        return True
    return input(f"🙋 {question} (y/n) ").strip().lower() == "y"


def order_pizza(count, cost):
    return f"🍕 Ordered {count} pizzas for ₹{cost:,}"


def run_safely(slip):
    call = json.loads(slip)
    count, cost = call["count"], call["cost"]
    print(f"\n🤖 Tinko wants: {count} pizzas for ₹{cost:,}")
    if count > MAX_PIZZAS:
        print(f"⛔ BLOCKED: more than {MAX_PIZZAS} pizzas is not allowed.")
        return
    if cost > MAX_RUPEES:
        print(f"⛔ BLOCKED: more than ₹{MAX_RUPEES:,} is not allowed.")
        return
    # Rule 2: ask first. Paying is risky, so a human says yes before every payment.
    if not ask_human(f"{count} pizzas, ₹{cost:,}. Approve?"):
        print("🚫 Rohan said no. Order cancelled.")
        return
    print("✅", order_pizza(count, cost))


brain = ToyBrain(rules={
    "everyone": json.dumps({"tool": "order_pizza", "count": 100, "cost": 50000}),
    "fanciest": json.dumps({"tool": "order_pizza", "count": 4, "cost": 2800}),
    "family": json.dumps({"tool": "order_pizza", "count": 5, "cost": 1200}),
})

run_safely(brain.reply("Get pizza for everyone in the city!"))       # 100 pizzas: blocked
run_safely(brain.reply("Get the fanciest pizzas in town"))          # over ₹2,000: blocked
run_safely(brain.reply("Get pizza for the whole family"))            # within limits: ask Rohan

# 🔁 Make it real: swap ToyBrain() for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B8 Guardrails

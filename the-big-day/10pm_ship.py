# ⏰ 10:00 PM: The party's over. Time to make Tinko ready for EVERY day.
# "Shipping" an agent means it runs without you watching. So it needs:
#   📝 logs     - a diary of everything it did (to debug tomorrow)
#   💰 a budget - real AI costs money per token, so cap the daily spend
#   🚨 alerts   - shout when a tool breaks, retry, then recover
import logging
from pathlib import Path

from toy_brain import ToyBrain

LOG_FILE = Path(__file__).with_name("tinko.log")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"),
                              logging.StreamHandler()])        # file + screen
log = logging.getLogger("tinko")

DAILY_BUDGET = 1.00          # dollars per day
PRICE_PER_TOKEN = 0.0002     # made-up price, just for the demo
spent = 0.0
pizza_calls = 0


def order_pizza(size, topping):
    global pizza_calls
    pizza_calls += 1
    if pizza_calls == 1:                       # simulate: the shop's site is down once
        raise ConnectionError("pizza shop not answering")
    return f"{size} {topping} pizza arrives at 8 pm"


def count_cost(text):
    # Rough rule: 1 word is about 1 token. Real APIs tell you the exact count.
    global spent
    spent += len(text.split()) * PRICE_PER_TOKEN
    if spent > DAILY_BUDGET:
        raise RuntimeError("💸 Daily budget used up. Tinko rests until tomorrow.")


def health_checked(tool, tries=3, **args):
    for attempt in range(1, tries + 1):
        try:
            return tool(**args)
        except ConnectionError as error:
            log.error("🚨 ALERT: %s failed (try %d/%d): %s", tool.__name__, attempt, tries, error)
    raise RuntimeError("Tool is down. Tell a human!")


brain = ToyBrain()
request = "Order me a large paneer pizza"
log.info("Request: %s", request)
count_cost(request)
slip = brain.reply(request)
log.info("Brain wrote: %s", slip)
result = health_checked(order_pizza, size="large", topping="paneer")
log.info("✅ Recovered after retry: %s", result)
count_cost(slip + result)
log.info("💰 Spent today: $%.4f of $%.2f budget", spent, DAILY_BUDGET)
print(f"\n📝 Full log saved to {LOG_FILE.name}. Good night, Tinko! 🌙")

# 🔁 Make it real: swap ToyBrain() for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B10 Ship it

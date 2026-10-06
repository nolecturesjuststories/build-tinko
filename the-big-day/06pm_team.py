# ⏰ 6:00 PM: The Diwali party is too big for one agent. Time for a team!
# Multi-agent = a Manager splits the job, each specialist does one part,
# and the Manager merges the results. Like a kitchen with a head chef.
import time
from concurrent.futures import ThreadPoolExecutor


class Bot:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def work(self, task):
        time.sleep(0.5)                      # pretend this takes a while
        return f"{self.name} ({self.role}): {task} ✔"


class Manager:
    def __init__(self, team):
        self.team = team

    def split(self, goal):
        # A real AI manager would write these tasks itself.
        print(f"🧑‍💼 Manager: splitting '{goal}' into tasks...")
        return {"ChefBot": "cook kheer and samosas",
                "ShopperBot": "buy sweets and candles",
                "DecoBot": "hang lights and draw a rangoli"}

    def run(self, goal):
        tasks = self.split(goal)
        bots = [bot for bot in self.team if bot.name in tasks]
        start = time.time()
        # All bots work AT THE SAME TIME (threads), not one after another.
        with ThreadPoolExecutor() as pool:
            jobs = [pool.submit(bot.work, tasks[bot.name]) for bot in bots]
            results = [job.result() for job in jobs]     # wait for everyone
        seconds = time.time() - start
        print(f"⏱️  3 jobs of 0.5 s each finished in {seconds:.1f} s (together!)")
        return results


team = [Bot("ChefBot", "cook"), Bot("ShopperBot", "shopper"), Bot("DecoBot", "decorator")]
manager = Manager(team)
results = manager.run("Diwali party")

print("\n📦 Manager merges the results:")
for line in results:
    print("   " + line)
print("🪔 The party is ready. Happy Diwali, and happy birthday Rohan!")

# 🔁 Make it real: give each bot a real AI brain (free, local) in Season B.
# 🎬 Full build: Season B, episode B12 CrewAI (team)

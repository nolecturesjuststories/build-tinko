# ⏰ 5:00 PM: Party prep! Too many jobs to just "wing it".
#
# Two ways an agent can work:
#   ReAct (what we did at 2 PM): think one step, act, look, think again.
#       Great for short or surprising jobs.
#   Plan-and-execute (this scene): write the whole plan FIRST, then do it
#       step by step and tick the boxes. Great for big jobs with many parts.
#       If a step fails, don't panic: RE-PLAN and carry on.

def make_plan(goal):
    # A real AI would write this list from the goal. Our toy plan is fixed.
    print(f"🗒️  Goal: {goal}")
    return ["Hang the Diwali lights", "Buy snacks at the corner shop",
            "Light the diyas", "Set the table for Grandma"]


def do_step(step):
    if "corner shop" in step:
        return False, "the snacks shop is closed! 😬"
    return True, "done"


def show(plan, ticked):
    for step in plan:
        box = "✅" if step in ticked else "⬜"
        print(f"   {box} {step}")


plan = make_plan("Get the house party-ready by 6 pm")
ticked = []
print("📋 The plan:")
show(plan, ticked)

i = 0
while i < len(plan):
    step = plan[i]
    ok, note = do_step(step)
    if ok:
        ticked.append(step)
        print(f"\n▶️  {step}: {note}")
    else:
        print(f"\n❌ {step}: {note}")
        print("🔄 Re-planning: swap that step for a new one.")
        plan[i] = "Make snacks at home with Grandma"
        continue                      # try the NEW step at the same spot
    i += 1

print("\n🎉 Final checklist:")
show(plan, ticked)

# 🔁 Make it real: swap the fixed plan for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B6 Planning

# ⏰ 1:00 PM: Grandma's kheer! Tinko must cook it exactly HER way.
# RAG = Retrieval-Augmented Generation:
#   1) Retrieve: find the right pages in your own notes
#   2) Augment:  paste those pages into the prompt
#   3) Generate: the brain answers FROM the pages, not from guesses
from toy_brain import ToyBrain

LIBRARY = [
    "Grandma's kheer: rice, milk, cardamom, a pinch of saffron. Stir slowly.",
    "Rohan's birthday cake: flour, sugar, butter, eggs, cocoa. Bake 30 minutes.",
    "Diwali rangoli: colored powder at the front door, diyas around it.",
    "House note: the spare key is under the blue flower pot.",
    "Pizza night: Rohan's favorite topping is paneer.",
    "Grandma's chai: tea leaves, milk, ginger, cardamom. Boil twice.",
]


class Notes:
    def __init__(self, pages):
        self.pages = pages

    def search(self, question, top=3):
        # Score each page by how many words it shares with the question.
        # Real RAG uses embeddings (meaning-numbers) + a vector database,
        # so "dessert" can match "kheer" even with no shared words.
        q_words = set(question.lower().replace("?", "").split())
        scored = []
        for page in self.pages:
            p_words = set(page.lower().replace(":", "").replace(",", "").split())
            scored.append((len(q_words & p_words), page))
        scored.sort(reverse=True)                  # best score first
        return [page for score, page in scored[:top] if score > 0]


brain = ToyBrain(rules={"kheer": "Kheer? Easy: chocolate, ketchup and sprinkles! 🍫"})
notes = Notes(LIBRARY)
question = "How do I make Grandma's kheer?"

print("❌ WITHOUT retrieval (the brain just guesses):")
print("   🤖", brain.reply(question))
print("   😱 Confident... and totally made up. That's a 'hallucination'.\n")

print("✅ WITH retrieval:")
pages = notes.search(question, top=2)
for i, page in enumerate(pages, 1):
    print(f"   📄 page {i}: {page}")
prompt = "\n".join("Note: " + p for p in pages) + "\nQuestion: " + question
print("   📝 Augmented prompt sent to the brain:")
print("      " + prompt.replace("\n", "\n      "))
print("   🤖", brain.reply(prompt))
print("   👵 Grandma approves!")

# 🔁 Make it real: swap ToyBrain() for a real AI (free, local) in Season B.
# 🎬 Full build: Season B, episode B5 RAG

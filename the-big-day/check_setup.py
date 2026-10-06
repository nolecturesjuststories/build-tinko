# 🔧 Run me first! I check that your computer is ready for "Tinko's Big Day".
# (This file uses only very old, simple Python, so it works even on old versions
#  and can tell you what to fix.)
import sys
import importlib.util

print("🐍 Your Python version: " + sys.version.split()[0])

if sys.version_info >= (3, 10):
    print("✅ You're ready! Try:  python3 07am_memory.py")
    print("   (On Windows, type  py  instead of  python3)")
else:
    print("❌ You need Python 3.10 or newer.")
    print("   1. Go to https://www.python.org/downloads/ and install the latest.")
    print("   2. Windows: tick 'Add Python to PATH' on the first install screen.")
    print("   3. Close and reopen your terminal, then run this file again.")
    print("   No install possible? Use GitHub Codespaces or Google Colab instead.")
    sys.exit(0)

# Optional extra: only the 5:30 PM MCP scene uses it, and it works without it.
if importlib.util.find_spec("mcp") is not None:
    print("✅ Optional 'mcp' package found: 0530pm_mcp_server.py can run a real server.")
else:
    print("ℹ️  Optional 'mcp' package not installed. That's fine!")
    print("   0530pm_mcp_server.py will run a plain demo instead.")
    print("   Want the real server later?  pip install mcp")

print("\n🎬 Everything else uses only built-in Python. No installs, no API keys.")

# 🔁 Make it real: in Season B you'll also install Ollama, a free local AI.
# 🎬 Full build: Season B, episode B1–B3 Your first agent

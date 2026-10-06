# ⏰ 5:30 PM: Tinko plugs into the party speaker and the weather app.
# MCP (Model Context Protocol) = a universal plug for AI tools.
# Write your tools ONCE as an MCP server, and any MCP app (like Claude Desktop)
# can find them and use them. No custom glue code for each app.
#
# This is a REAL MCP server. It needs one install:   pip install mcp
# No install? It still runs a plain demo of the same idea. Try:  --demo
#
# 🔌 Connect it to Claude Desktop: Settings > Developer > Edit Config, then add:
#   {"mcpServers": {"tinko": {
#       "command": "python3",
#       "args": ["/full/path/to/the-big-day/0530pm_mcp_server.py"]}}}
# (Windows: "py". Not starting? Use the full path to your python.) Then restart Claude Desktop.
import sys

try:
    from mcp.server.fastmcp import FastMCP     # the official MCP package
    server = FastMCP("tinko-party")
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

    class PretendServer:
        # Stand-in so the @server.tool() lines below still work without mcp.
        def tool(self):
            return lambda func: func            # hand the function back unchanged

    server = PretendServer()


@server.tool()
def play_music(song: str) -> str:
    """Play a song on the party speaker."""
    return f"🎵 Now playing '{song}' on the living-room speaker"


@server.tool()
def get_weather(city: str) -> str:
    """Get tonight's weather for a city."""
    return f"🌙 {city} tonight: clear sky, 24°C. Perfect for fireworks!"


def plain_demo():
    # What MCP does for you, by hand: a list of tools any app can ask for...
    registry = {"play_music": play_music, "get_weather": get_weather}
    print("📋 App asks: 'what tools do you have?'")
    for name, func in registry.items():
        print(f"   - {name}: {func.__doc__}")
    # ...and a standard way to call one by name with arguments.
    print("📞 App calls: play_music(song='Happy Birthday')")
    print("  ", registry["play_music"](song="Happy Birthday"))
    print("📞 App calls: get_weather(city='Jaipur')")
    print("  ", registry["get_weather"](city="Jaipur"))


if __name__ == "__main__":
    if HAS_MCP and "--demo" not in sys.argv:
        # Real server: talks to the app over stdin/stdout, so print to stderr.
        print("🔌 Tinko's MCP server is running (Ctrl+C to stop)", file=sys.stderr)
        server.run()                            # stdio by default
    else:
        if not HAS_MCP:
            print("ℹ️  The real server needs:  pip install mcp")
            print("   Here's what it would do, using a plain Python dict:\n")
        plain_demo()

# 🔁 Make it real: plug this server into a real AI app (free, local) in Season B.
# 🎬 Full build: Season B, episode B7 MCP

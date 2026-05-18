from src.primitive import prompts, resources, tools
from src.server import mcp

if __name__ == "__main__":
    mcp.run(transport="sse")

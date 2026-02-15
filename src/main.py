from src.primitive import prompts, resources, tools
from .server import mcp

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
from server import mcp
from src.settings import settings
import src.primitive.tools
import src.primitive.resources
import src.primitive.prompts

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
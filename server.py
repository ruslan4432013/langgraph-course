from fastmcp import FastMCP
from fastmcp.server.auth.providers.github import GitHubProvider
from src.settings import settings

auth = GitHubProvider(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    base_url=settings.BASE_URL,
)

mcp = FastMCP("My Server", auth=auth)

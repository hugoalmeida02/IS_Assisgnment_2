from app.mcp.server import mcp
from app.mcp import tools  # noqa: F401
from app.mcp import resources  # noqa: F401
from app.mcp import prompts  # noqa: F401


if __name__ == "__main__":
    mcp.run()
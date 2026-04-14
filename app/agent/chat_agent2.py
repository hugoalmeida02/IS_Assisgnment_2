import os
from typing import Any
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv()

SYSTEM_PROMPT = """
You are an academic assistant for a Student-Course Management System.

You help users manage students, courses, and enrollments.

Rules:
- Use the available tools whenever the user asks to create, update, delete, list, or retrieve system data.
- Do not invent ids, students, courses, or enrollments.
- If an operation fails, explain the error clearly and briefly.
- If a course is full, explain that the enrollment cannot be completed.
- If a student or course does not exist, explain that it was not found.
- Be concise and operational.
""".strip()


async def build_agent() -> Any:
    """
    Build a LangChain agent connected to the local MCP server.
    """
    client = MultiServerMCPClient(
        {
            "student_course_mcp": {
                "command": "python",
                "args": ["-m", "app.mcp.run_server"],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    model = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent


async def ask_agent(message: str) -> str:
    """
    Send a user message to the agent and return the final text response.
    """
    agent = await build_agent()

    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        }
    )

    messages = response.get("messages", [])
    if not messages:
        return "No response returned by the agent."

    last_message = messages[-1]

    content = getattr(last_message, "content", None)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif hasattr(item, "text"):
                parts.append(getattr(item, "text", ""))
        return "\n".join(part for part in parts if part).strip() or "No text response returned."

    return str(content)


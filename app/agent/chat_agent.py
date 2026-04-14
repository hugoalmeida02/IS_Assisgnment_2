import os
import uuid
from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("A variável OPENAI_API_KEY não está definida no .env")


class AgentRuntime:
    def __init__(self) -> None:
        self.agent = None
        self.memory = InMemorySaver()
        self.thread_config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        self._stdio_ctx = None
        self._session_ctx = None
        self._read = None
        self._write = None
        self.session: Optional[ClientSession] = None

    async def startup(self) -> None:
        """
        Start one MCP session, load prompt/resource/tools, and build the agent once.
        """
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.run_server"],
        )

        self._stdio_ctx = stdio_client(server_params)
        self._read, self._write = await self._stdio_ctx.__aenter__()

        self._session_ctx = ClientSession(self._read, self._write)
        self.session = await self._session_ctx.__aenter__()
        await self.session.initialize()

        prompt_data = await self.session.get_prompt("academic_assistant_prompt")
        system_instruction = prompt_data.messages[0].content.text

        resource_data = await self.session.read_resource("school://schema")
        schema_text = resource_data.contents[0].text

        system_instruction += f"\n\nServer context:\n{schema_text}"

        tools = await load_mcp_tools(self.session)

        model = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
            api_key=OPENAI_API_KEY,
        )

        self.agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=system_instruction,
            checkpointer=self.memory,
        )

    async def shutdown(self) -> None:
        """
        Cleanly close the MCP session and transport.
        """
        if self._session_ctx is not None:
            await self._session_ctx.__aexit__(None, None, None)
            self._session_ctx = None
            self.session = None

        if self._stdio_ctx is not None:
            await self._stdio_ctx.__aexit__(None, None, None)
            self._stdio_ctx = None

    async def ask(self, message: str) -> str:
        """
        Send one message to the agent and return the final text response.
        """
        if self.agent is None:
            raise RuntimeError("Agent is not initialized.")

        inputs = {"messages": [HumanMessage(content=message)]}
        response = await self.agent.ainvoke(inputs, config=self.thread_config)

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

    def reset_memory(self) -> None:
        self.thread_config = {"configurable": {"thread_id": str(uuid.uuid4())}}


agent_runtime = AgentRuntime()


@asynccontextmanager
async def agent_lifespan():
    await agent_runtime.startup()
    try:
        yield
    finally:
        await agent_runtime.shutdown()


async def ask_agent(message: str) -> str:
    return await agent_runtime.ask(message)


def reset_agent_memory() -> None:
    agent_runtime.reset_memory()
from textwrap import dedent

import pytest
from mcp import StdioServerParameters

from mcpadapt.core import MCPAdapt
from mcpadapt.langchain_adapter import LangChainAdapter


@pytest.fixture
def echo_server_script():
    return dedent(
        '''
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("Echo Server")

        @mcp.tool()
        def echo_tool(text: str) -> str:
            """Echo the input text"""
            return f"Echo: {text}"
        
        mcp.run()
        '''
    )


@pytest.mark.asyncio
async def test_langchain_adapter_async(echo_server_script):
    async with MCPAdapt(
        StdioServerParameters(
            command="uv", args=["run", "python", "-c", echo_server_script]
        ),
        LangChainAdapter(),
    ) as tools:
        assert len(tools) == 1  # we expect one tool as defined above
        assert tools[0].name == "echo_tool"  # we expect the tool to be named echo_tool
        response = await tools[0].ainvoke("hello")
        assert response == "Echo: hello"  # we expect the tool to return "Echo: hello"


def test_langchain_adapter_sync(echo_server_script):
    with MCPAdapt(
        StdioServerParameters(
            command="uv", args=["run", "python", "-c", echo_server_script]
        ),
        LangChainAdapter(),
    ) as tools:
        assert len(tools) == 1
        assert tools[0].name == "echo_tool"
        assert tools[0].invoke("hello") == "Echo: hello"

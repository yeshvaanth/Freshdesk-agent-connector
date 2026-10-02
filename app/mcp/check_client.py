import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Start the MCP server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.tools"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Show available tools
            response = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in response.tools:
                print(f"- {tool.name}: {tool.description}")

            # Test listing tickets
            print("\n--- List tickets ---")

            list_result = await session.call_tool(
                "list_tickets",
                arguments={"page": 1, "limit": 2},
            )
            print(list_result)

            # Test getting a ticket
            print("\n--- Get ticket ---")

            ticket_result = await session.call_tool(
                "get_ticket",
                arguments={"ticket_id": 1},
            )
            print(ticket_result)

            # Test searching tickets
            print("\n--- Search tickets ---")

            search_result = await session.call_tool(
                "search_tickets",
                arguments={"query": "payment"},
            )
            print(search_result)


if __name__ == "__main__":
    asyncio.run(main())
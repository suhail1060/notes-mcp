import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Tells the client how to launch the server process
server_params = StdioServerParameters(
    command="python",
    args=["server/notes_server.py"],
)


async def main():
    # stdio_client spawns the server and gives us read/write streams
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Handshake: negotiate protocol version, exchange capabilities
            await session.initialize()

            # --- Discovery ---
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])

            resources = await session.list_resources()
            print("Available resources:", [r.uri for r in resources.resources])

            prompts = await session.list_prompts()
            print("Available prompts:", [p.name for p in prompts.prompts])

            # --- Call a tool ---
            result = await session.call_tool(
                "create_note",
                arguments={"title": "client test", "content": "Created via client!"},
            )
            print("\ncreate_note result:", result.content[0].text)

            # --- Read a resource ---
            resource_result = await session.read_resource("notes://list")
            print("\nnotes://list contents:", resource_result.contents[0].text)

            # --- Fetch a prompt ---
            prompt_result = await session.get_prompt(
                "summarize_note", arguments={"filename": "client_test.md"}
            )
            print("\nsummarize_note prompt:", prompt_result.messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())
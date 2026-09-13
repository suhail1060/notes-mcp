import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from llm_agent import mcp_tools_to_gemini, ask_gemini_with_tools, extract_function_call

server_params = StdioServerParameters(command="python", args=["server/notes_server.py"])


async def handle_message(session, gemini_tools, user_message: str):
    response = ask_gemini_with_tools(user_message, gemini_tools)
    fn_call = extract_function_call(response)

    if fn_call is None:
        print(f"\nAssistant: {response.text}")
        return

    print(f"\n[calling tool: {fn_call.name}({dict(fn_call.args)})]")
    result = await session.call_tool(fn_call.name, arguments=dict(fn_call.args))
    tool_output = result.content[0].text
    print(f"[tool result: {tool_output}]")

    final_response = ask_gemini_with_tools(
        f"I ran {fn_call.name} and got this result: {tool_output}. "
        f"Briefly confirm to the user what happened.",
        gemini_tools,
    )
    print(f"\nAssistant: {final_response.text}")


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            gemini_tools = mcp_tools_to_gemini(tools.tools)

            print("notes-mcp agent ready. Available tools:", [t.name for t in tools.tools])
            print("Type your request, or 'exit' to quit.\n")

            while True:
                user_message = input("You: ").strip()
                if user_message.lower() in ("exit", "quit"):
                    break
                if not user_message:
                    continue
                await handle_message(session, gemini_tools, user_message)


if __name__ == "__main__":
    asyncio.run(main())
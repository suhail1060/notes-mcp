import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # Load environment variables from .env file

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def mcp_tools_to_gemini(mcp_tools) -> list[types.Tool]:
    """Convert MCP tool definitions into Gemini function declarations."""
    function_declarations = []
    for tool in mcp_tools:
        function_declarations.append(
            types.FunctionDeclaration(
                name=tool.name,
                description=tool.description or "",
                parameters=tool.input_schema,  # MCP already gives JSON schema
            )
        )
    return [types.Tool(function_declarations=function_declarations)]


def ask_gemini_with_tools(user_message: str, gemini_tools: list[types.Tool]):
    """Send a message to Gemini with available tools, return the response."""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_message,
        config=types.GenerateContentConfig(tools=gemini_tools),
    )
    return response


def extract_function_call(response):
    """Pull the function call out of a Gemini response, if present."""
    part = response.candidates[0].content.parts[0]
    return part.function_call  # None if Gemini just responded with text
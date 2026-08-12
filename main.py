"""Main entry point for the application."""

from pathlib import Path

import orjson
import rich
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageFunctionToolCall,
)
from platformdirs import user_data_dir
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.markdown import Markdown

from config import load_config
from tools import TOOL_IMPLS, tools

config = load_config()

# Constants
SYSTEM_PROMPT = Path(Path(__file__).parent / "system_prompt.md").read_text()
LOGO = Path(Path(__file__).parent / "logo.txt").read_text()
INPUT_STYLE = Style.from_dict({"prompt": "ansired"})
HISTORY_PATH = Path(user_data_dir("brokie")) / "history.txt"

# Ensure the history directory exists
HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

# Initialize the OpenAI client with an ollama base URL
client = OpenAI(base_url=config["url"], api_key=config["api_key"])

# Initialize context as a list with the system prompt
context = []
context.append({"role": "system", "content": SYSTEM_PROMPT})

# Global state
read_files = {}

# Rich console for pretty printing
console = Console()


def main() -> None:
    """Main function to run the application."""
    print(" ")
    rich.print(f"[bold green]{LOGO}")
    print(" ")
    session = PromptSession(history=FileHistory(str(HISTORY_PATH)))
    try:
        while True:
            prompt = session.prompt([("class:prompt", "❯ ")], style=INPUT_STYLE)  # noqa: RUF001
            if not prompt.strip():
                continue
            llm_response = llm_request(prompt, model=config["model"])
            console.print(Markdown(llm_response), style="blue")
            print(" ")
    except KeyboardInterrupt:
        rich.print("\n[bold red]Exiting...[/bold red]")


def llm_request(prompt: str, model: str) -> str:
    """Send a request to the LLM, execute tool calls, and return the response."""
    context.append({"role": "user", "content": prompt})

    while True:
        response = client.chat.completions.create(
            model=model,
            tools=tools,
            messages=context,
            parallel_tool_calls=False,
        )
        message = response.choices[0].message

        # No tool calls means this is the final answer
        if not message.tool_calls:
            context.append({"role": "assistant", "content": message.content})
            return message.content or ""

        # Print the model's reasoning
        thinking = (
            getattr(message, "reasoning", None)
            or getattr(message, "reasoning_content", None)
        )
        if thinking:
            console.print(Markdown(thinking), style="grey50")
            print(" ")

        # Record the model's tool call requests in context
        context.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                    if isinstance(tc, ChatCompletionMessageFunctionToolCall)
                ],
            },
        )

        # Execute each requested tool call
        for tool_call in message.tool_calls:
            if not isinstance(tool_call, ChatCompletionMessageFunctionToolCall):
                continue
            impl = TOOL_IMPLS.get(tool_call.function.name)
            if impl is None:
                result = f"Error: unknown tool '{tool_call.function.name}'"
            else:
                args = orjson.loads(tool_call.function.arguments)
                if tool_call.function.name == "edit":
                    result = impl(**args, read_files=read_files)
                else:
                    result = impl(**args)
                if tool_call.function.name == "read" and "path" in args:
                    abs_path = str(Path(args["path"]).resolve())
                    if not str(result).startswith("Error reading file:"):
                        read_files[abs_path] = result
            context.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                },
            )


if __name__ == "__main__":
    main()

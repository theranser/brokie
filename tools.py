"""Tool definitions for the agent."""

from openai.types.chat import ChatCompletionFunctionToolParam

from functions import edit, read, shell

tools: list[ChatCompletionFunctionToolParam] = [
    ChatCompletionFunctionToolParam(
        type="function",
        function={
            "name": "shell",
            "description": "Run a shell command.",
            "parameters": {
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to run.",
                    },
                },
                "required": ["command"],
            },
        },
    ),
    ChatCompletionFunctionToolParam(
        type="function",
        function={
            "name": "read",
            "description": "Read a file from the filesystem and return its contents.",
            "parameters": {
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to read.",
                    },
                },
                "required": ["path"],
            },
        },
    ),
    ChatCompletionFunctionToolParam(
        type="function",
        function={
            "name": "edit",
            "description": ("Edit a file with one or more exact text replacements."),
            "parameters": {
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to edit.",
                    },
                    "edits": {
                        "type": "array",
                        "description": "Targeted replacements matched against the original file.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "old_text": {
                                    "type": "string",
                                    "description": (
                                        "Exact text to replace. Must be unique in the file."
                                    ),
                                },
                                "new_text": {
                                    "type": "string",
                                    "description": "Replacement text for this edit.",
                                },
                            },
                            "required": ["old_text", "new_text"],
                        },
                    },
                },
                "required": ["path", "edits"],
            },
        },
    ),
]
TOOL_IMPLS = {
    "shell": shell,
    "read": read,
    "edit": edit,
}

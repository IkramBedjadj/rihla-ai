import json
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def run_agent(model, system_prompt, user_prompt, tools, tool_mapping):
    """
    Generic agent runner that supports Groq tool calling.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    while True:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append({
            "role": "assistant",
            "content": message.content or "",
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
            ],
        })

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print("\n================ TOOL CALL ================")
            print("Tool:", tool_name)
            print("Arguments:", arguments)
            print("============================================\n")

            if tool_name not in tool_mapping:
                raise ValueError(f"Unknown tool: {tool_name}")

            tool_function = tool_mapping[tool_name]
            tool_result = tool_function(**arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": json.dumps(tool_result, ensure_ascii=False),
            })

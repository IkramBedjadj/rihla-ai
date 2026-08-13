import json
import ollama


def run_agent(model, system_prompt, user_prompt, tools, tool_mapping):
    """
    Generic agent runner that supports Ollama tool calling.

    Args:
        model: model name
        system_prompt: system prompt
        user_prompt: user question
        tools: list of tool definitions (JSON schema)
        tool_mapping: dict {"tool_name": python_function}

    Returns:
        Final assistant response.
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    while True:

        response = ollama.chat(
            model=model,
            messages=messages,
            tools=tools,
        )

        message = response["message"]
        
      
        # إذا لم يطلب أي Tool انتهينا
        if not message.get("tool_calls"):
            return message["content"]

        # أضف رسالة المساعد
        messages.append(message)

        # نفذ كل Tool طلبها النموذج
        for tool_call in message["tool_calls"]:
            
            tool_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]



            print("\n================ TOOL CALL ================")
            print("Tool:", tool_name)
            print("Arguments:", arguments)
            print("============================================\n")



            if tool_name not in tool_mapping:
                raise ValueError(f"Unknown tool: {tool_name}")

            tool_function = tool_mapping[tool_name]

            tool_result = tool_function(**arguments)
              
            messages.append(
                {
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(tool_result, ensure_ascii=False),
                }
            )
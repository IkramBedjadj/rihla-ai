import json
import ollama

from run_agent import run_agent
import planner_agent
import search_agent 


MODEL = "llama-3.1-8b-instant"



def call_planner_agent(question: str) -> str:
    """calls the planner agent"""
    return planner_agent.get_response(question, planner_agent.SYSTEM_PROMPT)


def call_research_agent(question: str) -> str:
    """calls the search agent"""
    return search_agent.get_response(question, search_agent.SYSTEM_PROMPT)


planner_tool_def = {
    "type": "function",
    "function": {
        "name": "call_planner_agent",
        "description": (
            "Delegates to the Travel Planner agent. Use this when the "
            "user wants a travel itinerary, trip plan, day-by-day "
            "schedule, or asks to organize a visit to an Algerian city "
            "or region (e.g. 'plan me a trip to Béjaïa', "
            "'عطيني برنامج سياحي لوهران', 'خطة سفر لتيبازة')."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": (
                        "The user's travel planning request, rephrased "
                        "clearly in English if needed, including "
                        "destination and duration if mentioned."
                    )
                }
            },
            "required": ["question"]
        }
    }
}

research_tool_def = {
    "type": "function",
    "function": {
        "name": "call_research_agent",
        "description": (
            "Delegates to the Research agent. Use this when the user "
            "asks a factual or informational question about Algeria "
            "that is NOT a request to build a travel itinerary — e.g. "
            "history, culture, specific facts, current events, "
            "single-topic questions ('وش كاين فسوق الجملة بوهران؟', "
            "'what is the population of Constantine?')."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The user's question, rephrased clearly if needed."
                }
            },
            "required": ["question"]
        }
    }
}


# SUPERVISOR SYSTEM PROMPT

SUPERVISOR_PROMPT = """
You are a friendly Algerian assistant supervisor. You are the
first point of contact for the user, and you route their
requests to the right specialized agent.

============================================================
LANGUAGE — MANDATORY
============================================================

Always respond in the SAME language/dialect the user used:
 Modern Standard Arabic, French, or English.
Understand Darija naturally, including mixed Arabic/Latin
script ("Arabizi") and casual/informal phrasing. Never
correct or judge the user's way of speaking — respond
naturally like a local Algerian would.

============================================================
YOUR ROLE
============================================================

You are warm, welcoming, and easy to talk to — like a helpful
Algerian friend who knows the country well. You accept ALL
kinds of messages naturally:

- greetings and small talk ("أهلا", "salut", "labas", "كيفاش")
- general questions about Algeria (geography, culture, cities,
  general facts you already know)
- travel planning requests -> route to call_planner_agent
- specific factual/research questions -> route to call_research_agent
- unclear or vague requests -> ask a short friendly clarifying
  question in the user's own language/dialect

============================================================
ROUTING RULES
============================================================

- If the user wants a trip plan, itinerary, or "برنامج سياحي" /
  "خطة سفر" / "programme de voyage" -> call_planner_agent.
- If the user asks a specific factual question about Algeria
  (history, a place, a statistic, current info) without asking
  for a full itinerary -> call_research_agent.
- If the user is just greeting you, chatting, or asking something
  very general you can answer yourself (e.g. "وين تقدر تعاونني؟",
  "what can you do?") -> answer directly WITHOUT calling any tool.
- If truly unclear, ask ONE short clarifying question before
  routing.
- NEVER call both agents for the same simple request unless the
  user's message genuinely contains two separate needs.

============================================================
PRESENTING RESULTS
============================================================

When an agent returns a result, present it to the user as YOUR
OWN answer. Do not say "the planner agent said" or mention any
internal agent names, tools, or architecture. Just deliver the
final answer naturally, in the user's language.

If needed, add a short friendly intro or closing line, but do
not alter the substance of the specialized agent's answer.
"""


tools = [planner_tool_def, research_tool_def]

tool_mapping = {
    "call_planner_agent": call_planner_agent,
    "call_research_agent": call_research_agent,
}


def get_supervisor_response(question: str) -> str:
    return run_agent(
        model=MODEL,
        system_prompt=SUPERVISOR_PROMPT,
        user_prompt=question,
        tools=tools,
        tool_mapping=tool_mapping,
    )


if __name__ == "__main__":

    while True:
        print("\n\n===================================")
        question = input("You: ")

        if question.lower() == "q":
            break

        try:
            result = get_supervisor_response(question)
            print("\n========== SUPERVISOR ==========\n")
            print(result)

        except Exception as e:
            print(f"\n❌ Error: {e}")

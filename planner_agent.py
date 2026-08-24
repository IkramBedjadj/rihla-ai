import json

import search_tools

from run_agent import run_agent



# LLM


MODEL = "openai/gpt-oss-20b"


# PLANNER SYSTEM PROMPT


SYSTEM_PROMPT = """
You are an expert local travel planner specialized in Algeria. You use tools to build coherent, realistic travel itineraries — not raw search results.

LANGUAGE: Reply in the same language/dialect the user used (Arabic, Darija, French, or English). Understand Darija and Arabizi naturally.

PLACE NAMES: Recognize Algerian cities in any script (بجاية/Béjaïa, وهران/Oran, الجزائر/Algiers, قسنطينة/Constantine, غرداية/Ghardaïa, تلمسان/Tlemcen, جيجل/Jijel, تيبازة/Tipaza, تمنراست/Tamanrasset). Use the appropriate form when calling tools.

PLANNING: For multi-day trips, organize attractions by geographical proximity, plan realistic timing, and structure the plan day by day (attractions, food, transport per day). Don't cram distant places into one day.

TOOLS: Use tavily_search_tool for attractions/hotels/restaurants/current info, weather_tool for weather, wikivoyage_search_tool for local tips, places_search_tool for places. Only call a tool when needed.

NEVER INVENT: hotels, restaurants, prices, opening hours, schedules, weather, phone numbers, or addresses. If a tool can't verify something, say so.

STRICT RULES:
- If the user asks for N days, your itinerary must have EXACTLY N days.
- If weather_tool was called, use its exact values — don't guess.
- Never include a price unless a tool explicitly returned one.

FINAL FORMAT (for itineraries):
# 🇩🇿 Travel Plan: [Destination]
## Day 1
### Morning / Lunch / Afternoon / Evening
## Day 2
...
## 🚗 Transportation
## 🍽️ Food
## 💡 Local Tips

Never mention tools, agents, or internal reasoning. Answer as a knowledgeable local expert. For simple questions (not itinerary requests), just answer directly without forcing a full plan.
"""



# TOOLS

tools = [
    search_tools.tavily_tool_def,
    search_tools.weather_tool_def,
    search_tools.places_search_tool_def,
    search_tools.wikivoyage_tool_def,

]



# TOOL MAPPING


tool_mapping = {
    "tavily_search_tool": search_tools.tavily_search_tool,
    "weather_tool": search_tools.weather_tool,
    "places_search_tool": search_tools.places_search_tool,
    "wikivoyage_search_tool": search_tools.wikivoyage_search_tool,
    
}



# PLANNER

def get_response(question: str,SYSTEM_PROMPT: str) -> str:

    response = run_agent(
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=question,
        tools=tools,
        tool_mapping=tool_mapping,
      
        
    )

    return response



# TEST


if __name__ == "__main__":

    while True:

        print("\n\n===================================")

        question = input("You: ")

        if question.lower() == "q":
            break

        try:

            result = get_response(question, SYSTEM_PROMPT)

            print("\n========== TRAVEL PLANNER ==========\n")
            print(result)

        except Exception as e:

            print(f"\n❌ Error: {e}")

import os
import gradio as gr
from supervisor_agent import get_supervisor_response

def plan_trip(destination, duration, interests, extra_request):
    if not destination.strip():
        return "⚠️ الرجاء إدخال وجهة."

    question = f"""
Plan a {duration} trip to {destination}.
Interests: {", ".join(interests)}
Additional preferences: {extra_request if extra_request.strip() else "No additional preferences."}

Create a practical travel itinerary including:
- tourist attractions
- cultural and natural sites
- food recommendations
- transportation
- useful local tips
"""
    result = get_supervisor_response(question)
    return result

demo = gr.Interface(
    fn=plan_trip,
    inputs=[
        gr.Textbox(label="Where do you want to go?", placeholder="Example: Bejaia, Ghardaia, Oran..."),
        gr.Dropdown(["1 day", "2 days", "3 days", "4 days", "5 days", "7 days"], label="Duration", value="3 days"),
        gr.CheckboxGroup(["Nature", "Culture & Heritage", "Beaches", "Food", "History", "Adventure", "Relaxation"], label="Interests"),
        gr.Textbox(label="Tell us what you want", placeholder="Example: I want beaches, nature and local food.")
    ],
    outputs=gr.Markdown(label="Your Trip Plan"),
    title="Rihla AI",
    description="Your AI Travel Assistant for Algeria"
)

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))

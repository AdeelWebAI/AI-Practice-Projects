import os
import google.generativeai as genai
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Missing GEMINI in .env file")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Define LangGraph state schema
class GraphState(TypedDict):
    user_input: str
    ai_response: str

def call_gemini(state: GraphState):
    prompt = state["user_input"]

    try:
        # ✅ Primary Model: gemini-2.0-flash
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        state["ai_response"] = response.text

    except Exception as e:
        # If primary fails, try fallback model
        print(f"[WARNING] gemini-2.0-flash failed → {str(e)}")
        print("[INFO] Trying fallback model: gemini-1.5-flash...")
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            state["ai_response"] = f"(Fallback used) {response.text}"
        except Exception as e2:
            state["ai_response"] = f"Error: Both models failed → {str(e2)}"

    return state

# Build LangGraph
graph = StateGraph(GraphState)
graph.add_node("gemini_call", call_gemini)
graph.set_entry_point("gemini_call")
graph.add_edge("gemini_call", END)

compiled_graph = graph.compile()

def run_workflow(user_input: str):
    state = {"user_input": user_input, "ai_response": ""}
    final_state = compiled_graph.invoke(state)
    return final_state["ai_response"]
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

# Load environment variables
load_dotenv()

class AgentState(BaseModel):
    question: str
    answer: str | None = None

# Setup LLM with Gemini 2.0 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

async def research_agent(state: AgentState):
    prompt = f"""
You are an AI Research Assistant.
Your job is to provide clear, concise, and research-based answers.
Respond in a helpful, professional, and friendly tone.
If the question is unclear, ask for clarification.

Question: {state.question}
"""
    result = await llm.ainvoke(prompt)
    return AgentState(question=state.question, answer=result.content)

# Build graph
graph = StateGraph(AgentState)
graph.add_node("research_agent", research_agent)
graph.set_entry_point("research_agent")
graph.add_edge("research_agent", END)

app = graph.compile()

async def run_workflow(question: str):
    return await app.ainvoke({"question": question})

# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain + Gemini + Tavily
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

# 🔹 Load env vars
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 🔹 FastAPI app
app = FastAPI()

# 🔹 Enable CORS (React requests allowed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev: allow all, prod: restrict domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Request schema
class ChatRequest(BaseModel):
    message: str

# 🔹 Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,
)

# 🔹 Tavily tool (wrapped into single-input)
tavily_raw = TavilySearch(api_key=TAVILY_API_KEY, max_results=3)

tavily_tool = Tool(
    name="Tavily Weather Search",
    func=lambda query: tavily_raw.run(f"current weather in {query}"),
    description="Get current weather info for a city. Always return temperature in °C."
)

# 🔹 System instruction
system_instruction = """
You are a weather assistant.
Whenever the user asks about weather of any city,
use the tool "Tavily Weather Search" with the city name only.
Always respond with the temperature in Celsius (°C) and keep answers short.
If data is missing, politely say: 'Weather info is not available right now.'
"""


# 🔹 Create Agent with system prompt
agent = initialize_agent(
    tools=[tavily_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"prefix": system_instruction}
)

# ✅ Routes
@app.get("/")
def root():
    return {"message": "Weather Agent with Gemini + Tavily is running!"}

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = agent.run(req.message)
        return {"reply": response}
    except Exception as e:
        return {"error": str(e)}

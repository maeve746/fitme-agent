import os

from dotenv import load_dotenv
from fastapi import FastAPI

from .agent import CreatorAgent
from .rules import apply_safety_rules
from .schemas import AgentDecision, DMRequest


load_dotenv()


app = FastAPI(title="Fitness Creator DM Agent")


agent = CreatorAgent(
    api_key=os.environ["OPENAI_API_KEY"]
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/process-dm", response_model=AgentDecision)
async def process_dm(request: DMRequest):

    decision = await agent.process(request)

    decision = apply_safety_rules(
        decision,
        request.message,
    )

    return decision
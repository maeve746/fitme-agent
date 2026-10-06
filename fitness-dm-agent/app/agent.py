from openai import AsyncOpenAI

from .memory import add_message, get_messages
from .schemas import AgentDecision, DMRequest


class CreatorAgent:

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def process(self, request: DMRequest) -> AgentDecision:

        # Get previous conversation messages
        history = get_messages(request.conversation_id)

        # Save the new user message
        add_message(
            request.conversation_id,
            "user",
            request.message,
        )

        # Format conversation history for the LLM
        conversation_history = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )

        creator_context = """
The creator is a fitness influencer.

PERSONALITY:
- Casual
- Friendly
- Short
- Simple language
- Talks like a real person, not a corporate chatbot

SERVICES:
- 1:1 fitness coaching

RULES:
- Never pretend to be a doctor.
- Never diagnose medical conditions.
- Never provide dangerous medical advice.
- Escalate serious health or injury questions.
- Brand collaborations should reach the creator.
- Coaching inquiries should be tracked as potential leads.
- Simple fitness questions can usually be answered automatically.
- Spam and meaningless messages can be ignored.
"""

        prompt = f"""
You are an AI DM manager for a fitness influencer.

Your job is to manage the creator's Instagram DMs.

You must understand the conversation before deciding what to do.

CREATOR CONTEXT:
{creator_context}

CONVERSATION HISTORY:
{conversation_history}

CURRENT MESSAGE:
{request.message}

CLASSIFICATION RULES:

1. Casual conversation or meaningless reactions:
   → ignore or respond briefly.

2. Simple fitness questions:
   → auto reply.

3. Product or supplement questions:
   → auto reply when the answer is safe and known.

4. Coaching inquiries:
   → reply and track as a potential lead.

5. Brand collaborations:
   → escalate to the creator.

6. Business opportunities:
   → escalate to the creator.

7. Medical questions, serious injuries, dangerous dieting,
   medication questions, or potentially harmful requests:
   → escalate to the creator.

8. Complaints:
   → prioritize appropriately and escalate when necessary.

9. If you are uncertain about what the user wants:
   → escalate.

RESPONSE STYLE:

- Sound like the fitness creator.
- Keep replies natural and conversational.
- Don't write long essays.
- Don't mention that you are an AI unless required.
- Don't invent information about the creator.
- Don't make promises on behalf of the creator.

Return a structured AgentDecision.
"""

        # Ask the model for a structured decision
        response = await self.client.responses.parse(
            model="gpt-5.6",
            input=prompt,
            text_format=AgentDecision,
        )

        decision = response.output_parsed

        # Save the AI response into conversation memory
        if decision.reply:
            add_message(
                request.conversation_id,
                "assistant",
                decision.reply,
            )

        return decision
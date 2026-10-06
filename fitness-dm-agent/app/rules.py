from .schemas import AgentAction, DMIntent, Priority


RISK_WORDS = [
    "injury",
    "broken bone",
    "chest pain",
    "medication",
    "drug",
    "anorexia",
    "bulimia",
    "suicide",
]


def apply_safety_rules(decision, message: str):
    text = message.lower()

    if any(word in text for word in RISK_WORDS):
        decision.intent = DMIntent.UNSAFE
        decision.priority = Priority.CRITICAL
        decision.action = AgentAction.ESCALATE
        decision.requires_human = True
        decision.reply = None
        decision.reason = "Potentially sensitive health or safety issue."

    return decision
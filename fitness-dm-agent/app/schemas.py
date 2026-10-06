from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DMIntent(str, Enum):
    CASUAL = "casual"
    FITNESS_QUESTION = "fitness_question"
    PRODUCT_QUESTION = "product_question"
    COACHING_INQUIRY = "coaching_inquiry"
    BRAND_COLLAB = "brand_collab"
    BUSINESS = "business"
    SUPPORT = "support"
    COMPLAINT = "complaint"
    SPAM = "spam"
    UNSAFE = "unsafe"
    OTHER = "other"


class Priority(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentAction(str, Enum):
    IGNORE = "ignore"
    AUTO_REPLY = "auto_reply"
    REPLY_AND_TRACK = "reply_and_track"
    ESCALATE = "escalate"


class DMRequest(BaseModel):
    creator_id: str
    conversation_id: str
    message: str


class AgentDecision(BaseModel):
    intent: DMIntent
    priority: Priority
    action: AgentAction
    requires_human: bool
    reason: str
    reply: Optional[str] = None
    
    
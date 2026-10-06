from typing import Dict, List


conversation_memory: Dict[str, List[dict]] = {}


def add_message(
    conversation_id: str,
    role: str,
    content: str,
):
    if conversation_id not in conversation_memory:
        conversation_memory[conversation_id] = []

    conversation_memory[conversation_id].append(
        {
            "role": role,
            "content": content,
        }
    )


def get_messages(conversation_id: str) -> List[dict]:
    return conversation_memory.get(
        conversation_id,
        [],
    )
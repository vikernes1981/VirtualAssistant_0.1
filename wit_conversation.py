"""
Performs hierarchical intent detection using Wit.ai, keyword mapping, and GPT fallback.
"""

from wit_integration import get_intent_from_wit
from gpt_conversation import extract_intent_with_openai
from globals import KEYWORD_INTENT_MAP


def extract_intent_and_entities(user_input: str) -> tuple[str | None, dict]:
    """
    Attempt to detect the user's intent and any entities from a text command.

    The detection cascade:
        1. Wit.ai API (fast + cheap)
        2. Hardcoded keyword matches (low confidence fallback)
        3. GPT fallback (high cost, high quality)

    Args:
        user_input (str): The raw spoken or typed command.

    Returns:
        tuple: (intent as string, entities as dict)
    """
    # 1. Try Wit.ai
    intent = get_intent_from_wit(user_input)
    if intent:
        return intent, {}

    # 2. Keyword fallback
    for word, mapped_intent in KEYWORD_INTENT_MAP.items():
        if word in user_input.lower():
            print("[INTENT] via keyword fallback:", mapped_intent)
            return mapped_intent, {}

    # 3. GPT fallback
    intent, entities = extract_intent_with_openai(user_input)
    print("[INTENT] via GPT fallback:", intent)
    return intent, entities or {}

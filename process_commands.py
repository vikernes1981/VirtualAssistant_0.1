from intent_router import get_handler
from fallback_handler import handle_unknown


def handle_intent(intent, entities=None, command=None):
    try:
        handler = get_handler(intent)
        handler(entities, command)
    except Exception as e:
        print(f"Unexpected error during command processing: {e}")
        handle_unknown(entities, command)

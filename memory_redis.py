import redis
import os
import json
from dotenv import load_dotenv

load_dotenv()
r = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def load_history(session_id: str) -> list:
    key = f"chat:{session_id}"
    if not r.exists(key):
        return []
    return json.loads(r.get(key))

def save_history(session_id: str, user_msg: str, bot_reply: str):
    key = f"chat:{session_id}"
    history = load_history(session_id)
    history.append([user_msg, bot_reply])
    r.set(key, json.dumps(history))

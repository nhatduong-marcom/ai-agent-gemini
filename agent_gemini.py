from llm_gemini import ask_gemini
from memory_redis import load_history, save_history
from vector_faiss import get_relevant_docs
from tools import execute_tool

def build_prompt(query: str, context: list, history: list) -> str:
    chat_log = "\n".join([f"Khách: {q}\nBot: {a}" for q, a in history[-5:]])
    knowledge = "\n".join(["- " + doc for doc in context])

    return f"""
Bạn là trợ lý CSKH chuyên nghiệp, nói tiếng Việt và tiếng Anh.

Lịch sử hội thoại:
{chat_log}

Tri thức tham khảo:
{knowledge}

Câu hỏi:
{query}

Trả lời thân thiện, tự nhiên. Nếu cần, thực hiện hành động phù hợp.
"""

def handle_chat(query: str, session_id: str) -> str:
    history = load_history(session_id)
    context = get_relevant_docs(query)
    prompt = build_prompt(query, context, history)
    reply = ask_gemini(prompt)
    action_reply = execute_tool(query)
    full_reply = reply + ("\n\n" + action_reply if action_reply else "")
    save_history(session_id, query, full_reply)
    return full_reply

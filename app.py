import os
if not os.path.exists("knowledge_base/vector_store/index.faiss"):
    from vector_faiss import build_vector_store
    build_vector_store()

from flask import Flask, request, jsonify
from agent_gemini import handle_chat

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Lấy dữ liệu JSON, ép buộc giải mã nếu cần
        data = request.get_json(force=True)

        session_id = data.get("session_id", "anonymous")
        message = data.get("message")

        if not message:
            return jsonify({"error": "Missing 'message' in request"}), 400

        # Gọi AI Agent
        reply = handle_chat(message, session_id)
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

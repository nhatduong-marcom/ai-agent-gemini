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
    # Đảm bảo encoding UTF-8, tự động reload nếu debug
    app.run(debug=True, host="0.0.0.0", port=5000)


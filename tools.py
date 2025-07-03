def execute_tool(query: str) -> str:
    q = query.lower()
    if "mã đơn hàng" in q or "tra cứu" in q:
        return "📦 Đơn hàng XYZ123 đang được giao."
    elif "gửi mail" in q or "email" in q:
        return "📧 Email của bạn đã được gửi."
    elif "tạo ticket" in q:
        return "✅ Ticket hỗ trợ đã được tạo."
    return ""

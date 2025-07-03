# -------------------------------
# Gửi yêu cầu đến AI Agent CSKH dùng Gemini API qua Flask
# Tác giả: ChatGPT
# Ngày: 2025-06-26
# -------------------------------

# Thông tin cấu hình
$apiUrl = "http://localhost:5000/chat"
$sessionId = "testuser"

# ==== Nhập nội dung câu hỏi ở đây ====
$message = "Tôi muốn đổi trả sản phẩm"
# =====================================

# Tạo JSON request đúng chuẩn UTF-8
$body = @{
    session_id = $sessionId
    message    = $message
} | ConvertTo-Json -Depth 2 -Compress

# Gửi POST request với UTF-8 encoding
try {
    $response = Invoke-RestMethod -Method POST `
        -Uri $apiUrl `
        -ContentType "application/json" `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($body))

    # In phản hồi từ chatbot
    Write-Host "`n📩 Câu hỏi gửi: $message" -ForegroundColor Yellow
    Write-Host "`n🤖 Phản hồi từ chatbot:" -ForegroundColor Cyan
    Write-Host "$($response.response)`n"
}
catch {
    Write-Host "`n❌ Đã xảy ra lỗi khi gửi yêu cầu!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor DarkGray
}

import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import base64

genai.configure(api_key="Your_API")  # Thay bằng API key của bạn
model = genai.GenerativeModel("gemini-1.5-pro")

# Bộ nhớ tạm để lưu lịch sử chat (Dùng database nếu cần)
chat_history = []

@csrf_exempt
def chat_with_gemini(request):
    global chat_history  # Dùng biến toàn cục để lưu lịch sử

    if request.method == "POST":
        user_input = request.POST.get("message", "")
        uploaded_file = request.FILES.get("file")

        parts = [{"text": user_input}] if user_input else []

        if uploaded_file:
            # Đảm bảo thư mục 'media/' tồn tại
            os.makedirs("media", exist_ok=True)
            file_path = os.path.join("media", uploaded_file.name)

            # Lưu file vào thư mục media/
            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Đọc file dưới dạng base64
            with open(file_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode("utf-8")

            # Lấy loại MIME của file
            mime_type = uploaded_file.content_type  # image/png, audio/mpeg, ...

            # Thêm dữ liệu file vào danh sách parts
            parts.append({"inline_data": {"mime_type": mime_type, "data": file_data}})

        # Gửi dữ liệu đến API Gemini
        response = model.generate_content(parts)
        bot_reply = response.text

        # Lưu tin nhắn vào lịch sử
        chat_history.append({"role": "user", "message": user_input})
        chat_history.append({"role": "bot", "message": bot_reply})

        return JsonResponse({"response": bot_reply, "history": chat_history})

    return JsonResponse({"error": "Invalid request method"}, status=400)

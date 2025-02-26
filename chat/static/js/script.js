function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let fileInput = document.getElementById("file-input").files[0];
    let chatBox = document.getElementById("chat-box");

    if (!userInput && !fileInput) return;

    // Hiển thị tin nhắn người dùng
    let userMessage = document.createElement("div");
    userMessage.className = "message user-message";
    userMessage.innerText = userInput;
    chatBox.appendChild(userMessage);

    // Gửi dữ liệu đến server
    let formData = new FormData();
    formData.append("message", userInput);
    if (fileInput) {
        formData.append("file", fileInput);
    }

    fetch("/chat/", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Hiển thị phản hồi từ Gemini
        let aiMessage = document.createElement("div");
        aiMessage.className = "message ai-message";
        aiMessage.innerText = data.response;
        chatBox.appendChild(aiMessage);
    });

    // Xóa input sau khi gửi
    document.getElementById("user-input").value = "";
    document.getElementById("file-input").value = "";
}

// Cho phép nhấn Enter để gửi tin nhắn
function handleKeyPress(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
}

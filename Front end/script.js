document.addEventListener("DOMContentLoaded", () => {
  const loginScreen = document.getElementById("login-screen");
  const chatScreen = document.getElementById("chat-screen");
  const confirmBtn = document.getElementById("confirm-btn");
  const sendBtn = document.getElementById("send-btn");
  const messageInput = document.getElementById("message-input");
  const messagesDiv = document.getElementById("messages");

  // Login button
  confirmBtn.addEventListener("click", () => {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    if (username && password) {
      loginScreen.style.display = "none";
      chatScreen.style.display = "flex";
    } else {
      alert("⚠️ Please enter both username and password!");
    }
  });

  // Send button
  sendBtn.addEventListener("click", () => {
    const message = messageInput.value.trim();
    if (!message) return;
    addMessage("You", message);
    messageInput.value = "";
    sendToBackend(message);
  });

  // Add message to chat
  function addMessage(sender, text) {
    const div = document.createElement("div");
    div.classList.add("message");
    div.innerHTML = `<b>${sender}:</b> ${text}`;
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  // Send message to backend
  async function sendToBackend(message) {
    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });
      const data = await response.json();
      addMessage("Bot", data.reply);
    } catch (error) {
      addMessage("Bot", "⚠️ Error: Cannot connect to server");
    }
  }
});


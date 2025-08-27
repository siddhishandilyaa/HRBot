
      let currentUsername = "";
      const loginScreen = document.getElementById("login-screen");
      const chatScreen = document.getElementById("chat-screen");
      const usernameInput = document.getElementById("username");
      const passwordInput = document.getElementById("password");
      const confirmBtn = document.getElementById("confirm-btn");
      const messagesDiv = document.getElementById("messages");
      const messageInput = document.getElementById("message-input");
      const sendBtn = document.getElementById("send-btn");
      const currentUserSpan = document.getElementById("current-user");

      confirmBtn.addEventListener("click", handleLogin);
      sendBtn.addEventListener("click", sendMessage);
      messageInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          sendMessage();
        }
      });

      async function handleLogin() {
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (!username || !password) {
          alert("Please enter both username and password");
          return;
        }

        try {
          const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
          });

          const data = await response.json();

          if (data.success) {
            currentUsername = data.username;
            currentUserSpan.textContent = `Logged in as: ${currentUsername}`;
            loginScreen.style.display = "none";
            chatScreen.style.display = "block";
            addMessage("HR Bot", data.message, "bot");
            usernameInput.value = "";
            passwordInput.value = "";
          } else {
            alert(data.message);
          }
        } catch (error) {
          alert("Login failed. Please try again.");
        }
      }
      const logoutBtn = document.getElementById("logout-btn");

      logoutBtn.addEventListener("click", async () => {
        try {
          const response = await fetch("/logout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: currentUsername }),
          });
          const data = await response.json();

          if (data.success) {
            alert(data.message);
            // Reset UI
            chatScreen.style.display = "none";
            loginScreen.style.display = "block";
            currentUserSpan.textContent = "";
            messagesDiv.innerHTML = "";
            currentUsername = "";
          } else {
            alert("Logout failed. Try again.");
          }
        } catch (error) {
          alert("Error during logout.");
        }
      });

      async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        addMessage(currentUsername, message, "user");
        messageInput.value = "";

        try {
          const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, username: currentUsername }),
          });

          const data = await response.json();

          if (data.success) {
            addMessage("HR Bot", data.bot_response, "bot");
          } else {
            addMessage("HR Bot", "Sorry, I encountered an error.", "bot");
          }
        } catch (error) {
          addMessage("HR Bot", "Connection error. Please try again.", "bot");
        }
      }

      function addMessage(sender, message, type) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${type}`;
        const time = new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        });
        messageDiv.innerHTML = `
                <div class="message-header">
                    <strong>${sender}</strong>
                    <span class="timestamp">${time}</span>
                </div>
                <div class="message-content">${message}</div>
            `;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        return messageDiv;
      }

// Sarthi Dashboard Logic (Step 6)
/**
 * Sarthi Dashboard - Chat Logic & API Integration
 * Handles session management, message sending, and UI updates.
 */

// ============================================
// CONFIGURATION
// ============================================

const API_BASE = "http://localhost:5000";
let sessionId = null;

// ============================================
// DOM ELEMENTS
// ============================================

const chatArea = document.getElementById("chat-area");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const newChatBtn = document.getElementById("new-chat-btn");
const typingIndicator = document.getElementById("typing-indicator");
const statusText = document.getElementById("status-text");

// ============================================
// SESSION MANAGEMENT
// ============================================

async function startNewSession() {
    try {
        statusText.textContent = "Naya samvad shuru ho raha hai...";
        chatArea.innerHTML = "";

        const response = await fetch(`${API_BASE}/api/session/new`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        const data = await response.json();
        sessionId = data.session_id;

        // Show welcome message
        showWelcome();

        // Show Krishna's greeting
        addMessage("krishna", data.greeting);

        statusText.textContent = "Krishna tayyar hain";
        messageInput.focus();

    } catch (error) {
        console.error("Session error:", error);
        showError("Server se connection nahi ho paya. Kya backend chal raha hai?");
        statusText.textContent = "Connection error";
    }
}

// ============================================
// SEND MESSAGE
// ============================================

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || !sessionId) return;

    // Disable input while waiting
    messageInput.value = "";
    messageInput.style.height = "auto";
    setSending(true);

    // Show user message
    addMessage("user", message);

    // Create an empty message bubble for Krishna's streaming response
    const krishnaMsgId = addMessage("krishna", "");

    try {
        const response = await fetch(`${API_BASE}/api/chat_stream`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });

        if (!response.ok) {
            const data = await response.json();
            showError(data.error || "Kuch gadbad ho gayi");
            setSending(false);
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunkText = decoder.decode(value, { stream: true });
            const lines = chunkText.split('\n\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        if (data.chunk) {
                            updateMessage(krishnaMsgId, data.chunk);
                        }
                        if (data.done) {
                            statusText.textContent = `Context: ${data.context_length} messages`;
                        }
                    } catch (e) {
                        // ignore malformed chunks
                    }
                }
            }
        }

    } catch (error) {
        console.error("Chat error:", error);
        showError("Server se baat nahi ho pa rahi. Kya backend chal raha hai?");
    }

    setSending(false);
    messageInput.focus();
}

// ============================================
// UI FUNCTIONS
// ============================================

function addMessage(role, content) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;

    const avatarEmoji = role === "krishna" ? "🙏" : "🧑";
    const name = role === "krishna" ? "KRISHNA" : "YOU";

    // Generate unique ID for streaming updates
    const msgId = 'msg-' + Math.random().toString(36).substr(2, 9);
    messageDiv.id = msgId;

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatarEmoji}</div>
        <div>
            <div class="message-name">${name}</div>
            <div class="message-content" id="content-${msgId}">${escapeHtml(content)}</div>
        </div>
    `;

    chatArea.appendChild(messageDiv);
    scrollToBottom();
    
    return msgId;
}

function updateMessage(msgId, content) {
    const el = document.getElementById(`content-${msgId}`);
    if (el) {
        // Appending to textContent safely escapes HTML characters automatically
        el.textContent += content;
        scrollToBottom();
    }
}

function showWelcome() {
    const welcome = document.createElement("div");
    welcome.className = "welcome-message";
    welcome.innerHTML = `
        <span class="welcome-icon">🕉️</span>
        <div class="welcome-title">Sarthi — Voice of Krishna</div>
        <div class="welcome-text">
            Yeh ek divya samvad hai. Krishna se kuch bhi poocho — 
            dharma, yuddh, jeevan, ya Mahabharata ke baare mein.
        </div>
    `;
    chatArea.appendChild(welcome);
}

function showTyping(show) {
    typingIndicator.classList.toggle("active", show);
    if (show) scrollToBottom();
}

function setSending(sending) {
    sendBtn.disabled = sending;
    messageInput.disabled = sending;
}

function showError(message) {
    const toast = document.createElement("div");
    toast.className = "error-toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

function scrollToBottom() {
    setTimeout(() => {
        chatArea.scrollTop = chatArea.scrollHeight;
    }, 50);
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// ============================================
// AUTO-RESIZE TEXTAREA
// ============================================

messageInput.addEventListener("input", () => {
    messageInput.style.height = "auto";
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + "px";
});

// ============================================
// EVENT LISTENERS
// ============================================

// Send on button click
sendBtn.addEventListener("click", sendMessage);

// Send on Enter (Shift+Enter for new line)
messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// New conversation button
newChatBtn.addEventListener("click", () => {
    if (confirm("Naya samvad shuru karein? Purana samvad mit jayega.")) {
        startNewSession();
    }
});

// ============================================
// INITIALIZE
// ============================================

// Start a new session when page loads
startNewSession();
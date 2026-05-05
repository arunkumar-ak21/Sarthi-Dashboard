# Step 6: Frontend Dashboard — The Interface

> **Goal:** Build a beautiful Mahabharata-themed chat interface that connects to the backend.
> **Time Estimate:** 15-20 minutes (copy the code, then customize)

---

## What You'll Do in This Step

| Task | Status |
|------|--------|
| Create `frontend/index.html` — chat page structure | [ ] |
| Create `frontend/style.css` — Mahabharata theme styling | [ ] |
| Create `frontend/script.js` — chat logic & API calls | [ ] |
| Test: Open in browser, chat with Krishna | [ ] |

---

## 6.1 Create `frontend/index.html`

**Open** `frontend/index.html` and **replace everything** with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sarthi — Voice of Krishna</title>
    <meta name="description" content="Chat with Lord Krishna from the Mahabharata. An NLP-powered conversational AI.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">

        <!-- Header -->
        <header class="header" id="header">
            <div class="header-left">
                <div class="avatar" id="avatar">
                    <span class="avatar-icon">🙏</span>
                </div>
                <div class="header-info">
                    <h1 class="title">Sarthi</h1>
                    <p class="subtitle" id="status-text">Krishna is ready</p>
                </div>
            </div>
            <button class="new-chat-btn" id="new-chat-btn" title="New Conversation">
                <span>+ Naya Samvad</span>
            </button>
        </header>

        <!-- Chat Area -->
        <main class="chat-area" id="chat-area">
            <!-- Messages will be added here by JavaScript -->
        </main>

        <!-- Typing Indicator -->
        <div class="typing-indicator" id="typing-indicator">
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
            <span class="typing-text">Krishna soch rahe hain...</span>
        </div>

        <!-- Input Area -->
        <footer class="input-area" id="input-area">
            <div class="input-wrapper">
                <textarea 
                    id="message-input" 
                    placeholder="Krishna se poocho..."
                    rows="1"
                    maxlength="1000"
                ></textarea>
                <button class="send-btn" id="send-btn" title="Bhejo">
                    <span class="send-icon">➤</span>
                </button>
            </div>
        </footer>

    </div>

    <script src="script.js"></script>
</body>
</html>
```

---

## 6.2 Create `frontend/style.css`

**Open** `frontend/style.css` and **replace everything** with:

```css
/* ============================================
   SARTHI DASHBOARD — Mahabharata Theme
   Color Palette: Deep blacks, rich golds, warm ambers
   ============================================ */

/* --- CSS Variables (Design Tokens) --- */
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-chat: #0e0e15;
    --bg-input: #1a1a25;

    --gold-primary: #d4a843;
    --gold-light: #f0d078;
    --gold-dark: #a07830;
    --gold-glow: rgba(212, 168, 67, 0.15);

    --text-primary: #e8e0d0;
    --text-secondary: #9a917e;
    --text-muted: #5a5448;

    --user-bubble: #1e2a3a;
    --krishna-bubble: #1a1510;
    --krishna-border: rgba(212, 168, 67, 0.25);

    --font-display: 'Cinzel', serif;
    --font-body: 'Inter', sans-serif;

    --radius-sm: 8px;
    --radius-md: 16px;
    --radius-lg: 24px;
}

/* --- Reset & Base --- */
*, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    height: 100%;
    overflow: hidden;
}

body {
    font-family: var(--font-body);
    background: var(--bg-primary);
    color: var(--text-primary);
}

/* --- App Container --- */
.app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 800px;
    margin: 0 auto;
    background: var(--bg-chat);
    position: relative;
    border-left: 1px solid rgba(212, 168, 67, 0.08);
    border-right: 1px solid rgba(212, 168, 67, 0.08);
}

/* --- Header --- */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--krishna-border);
    flex-shrink: 0;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--gold-dark), var(--gold-primary));
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px var(--gold-glow);
    animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px var(--gold-glow); }
    50% { box-shadow: 0 0 35px rgba(212, 168, 67, 0.3); }
}

.avatar-icon {
    font-size: 22px;
}

.title {
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--gold-primary);
    letter-spacing: 2px;
}

.subtitle {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 2px;
}

.new-chat-btn {
    background: transparent;
    color: var(--gold-primary);
    border: 1px solid var(--krishna-border);
    padding: 8px 16px;
    border-radius: var(--radius-sm);
    cursor: pointer;
    font-family: var(--font-body);
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.new-chat-btn:hover {
    background: var(--gold-glow);
    border-color: var(--gold-primary);
    box-shadow: 0 0 15px var(--gold-glow);
}

/* --- Chat Area --- */
.chat-area {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    scroll-behavior: smooth;
}

/* Scrollbar */
.chat-area::-webkit-scrollbar {
    width: 4px;
}
.chat-area::-webkit-scrollbar-track {
    background: transparent;
}
.chat-area::-webkit-scrollbar-thumb {
    background: var(--gold-dark);
    border-radius: 4px;
}

/* --- Message Bubbles --- */
.message {
    display: flex;
    gap: 10px;
    max-width: 85%;
    animation: message-in 0.4s ease-out;
}

@keyframes message-in {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

.message.krishna {
    align-self: flex-start;
}

.message.user {
    align-self: flex-end;
    flex-direction: row-reverse;
}

.message-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 4px;
}

.message.krishna .message-avatar {
    background: linear-gradient(135deg, var(--gold-dark), var(--gold-primary));
}

.message.user .message-avatar {
    background: var(--user-bubble);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.message-content {
    padding: 12px 16px;
    border-radius: var(--radius-md);
    line-height: 1.6;
    font-size: 0.92rem;
    font-weight: 300;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.message.krishna .message-content {
    background: var(--krishna-bubble);
    border: 1px solid var(--krishna-border);
    border-top-left-radius: 4px;
    color: var(--text-primary);
}

.message.user .message-content {
    background: var(--user-bubble);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-top-right-radius: 4px;
    color: #c8d0dc;
}

.message-name {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 4px;
}

.message.krishna .message-name {
    color: var(--gold-primary);
}

.message.user .message-name {
    color: var(--text-secondary);
    text-align: right;
}

/* --- Typing Indicator --- */
.typing-indicator {
    display: none;
    align-items: center;
    gap: 10px;
    padding: 8px 20px;
    color: var(--text-secondary);
    font-size: 0.8rem;
}

.typing-indicator.active {
    display: flex;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--gold-primary);
    animation: typing-bounce 1.4s infinite;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing-bounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.3; }
    30% { transform: translateY(-6px); opacity: 1; }
}

/* --- Input Area --- */
.input-area {
    padding: 12px 16px 20px;
    background: var(--bg-secondary);
    border-top: 1px solid var(--krishna-border);
    flex-shrink: 0;
}

.input-wrapper {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    background: var(--bg-input);
    border: 1px solid rgba(212, 168, 67, 0.12);
    border-radius: var(--radius-md);
    padding: 4px 4px 4px 16px;
    transition: border-color 0.3s ease;
}

.input-wrapper:focus-within {
    border-color: var(--gold-primary);
    box-shadow: 0 0 20px var(--gold-glow);
}

#message-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text-primary);
    font-family: var(--font-body);
    font-size: 0.92rem;
    font-weight: 300;
    resize: none;
    max-height: 120px;
    padding: 10px 0;
    line-height: 1.5;
}

#message-input::placeholder {
    color: var(--text-muted);
}

.send-btn {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, var(--gold-dark), var(--gold-primary));
    color: var(--bg-primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.3s ease;
}

.send-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px var(--gold-glow);
}

.send-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    transform: none;
}

.send-icon {
    font-size: 18px;
    transform: rotate(0deg);
}

/* --- Welcome Message --- */
.welcome-message {
    text-align: center;
    padding: 40px 20px;
    animation: message-in 0.6s ease-out;
}

.welcome-icon {
    font-size: 48px;
    margin-bottom: 16px;
    display: block;
}

.welcome-title {
    font-family: var(--font-display);
    font-size: 1.3rem;
    color: var(--gold-primary);
    margin-bottom: 8px;
    letter-spacing: 1px;
}

.welcome-text {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 400px;
    margin: 0 auto;
}

/* --- Error Message --- */
.error-toast {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #2a1215;
    color: #f87171;
    border: 1px solid rgba(248, 113, 113, 0.3);
    padding: 10px 20px;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    z-index: 100;
    animation: toast-in 0.3s ease-out;
}

@keyframes toast-in {
    from { opacity: 0; transform: translateX(-50%) translateY(-10px); }
    to { opacity: 1; transform: translateX(-50%) translateY(0); }
}

/* --- Responsive --- */
@media (max-width: 600px) {
    .header { padding: 12px 14px; }
    .title { font-size: 1.1rem; }
    .new-chat-btn span { font-size: 0.7rem; }
    .chat-area { padding: 14px; }
    .message { max-width: 92%; }
}
```

---

## 6.3 Create `frontend/script.js`

**Open** `frontend/script.js` and **replace everything** with:

```javascript
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

    // Show typing indicator
    showTyping(true);

    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });

        const data = await response.json();

        if (response.ok) {
            showTyping(false);
            addMessage("krishna", data.response);
            statusText.textContent = `Context: ${data.context_length} messages`;
        } else {
            showTyping(false);
            showError(data.error || "Kuch gadbad ho gayi");
        }

    } catch (error) {
        console.error("Chat error:", error);
        showTyping(false);
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

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatarEmoji}</div>
        <div>
            <div class="message-name">${name}</div>
            <div class="message-content">${escapeHtml(content)}</div>
        </div>
    `;

    chatArea.appendChild(messageDiv);
    scrollToBottom();
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
```

---

## 6.4 Test the Dashboard

### Make sure backend is running:

In your **first terminal** (the one running the server):
```powershell
cd backend
python app.py
```

### Open the dashboard:

Simply **double-click** `frontend/index.html` in File Explorer, or open it in VS Code and use **"Open with Live Server"** extension, or run:

```powershell
start "C:\Users\kumar\Pictures\Minor project\chakravyuh-backend\frontend\index.html"
```

### What you should see:

1. A dark-themed chat interface with gold accents
2. Header shows "Sarthi" with a glowing avatar
3. Krishna's greeting message appears automatically
4. Type a message and press Enter — Krishna responds in Hinglish
5. The typing indicator shows while Krishna is thinking

### Test these interactions:

| Test | What to Type | Expected |
|------|-------------|----------|
| Introduction | `Krishna, tum kaun ho?` | Introduces himself in Hinglish |
| Chakravyuha | `Chakravyuha ke baare mein batao` | Describes formation, mentions Abhimanyu |
| Arjun | `Arjun tumhara sabse priya mitra hai?` | Talks about Arjun with warmth |
| Gita | `Karma yoga kya hai?` | Explains karma yoga in Hinglish |
| Out-of-context | `Aaj ka weather kaisa hai?` | Redirects to dharma/Mahabharata era |
| New Chat | Click "Naya Samvad" button | Clears history, fresh greeting |

---

## Troubleshooting

### Page is blank / no greeting
- Open browser console (F12 → Console tab) — check for errors
- Make sure backend is running at `http://localhost:5000`
- Check that CORS is working (no "blocked by CORS" errors in console)

### "Failed to fetch" error
- Backend is not running. Start it: `cd backend && python app.py`
- Or wrong port — check `API_BASE` in script.js matches your server port

### Styling looks broken
- Make sure `style.css` is in the same folder as `index.html`
- Hard refresh the browser: `Ctrl + Shift + R`

### Messages don't appear
- Check browser console for JavaScript errors
- Make sure `script.js` is in the same folder as `index.html`

---

## Final Checklist for Step 6

| # | Check | How to Verify |
|---|-------|--------------|
| 1 | Page loads with dark/gold theme | Open index.html in browser |
| 2 | Krishna's greeting appears | Automatic on page load |
| 3 | Can type and send messages | Type + Enter or click send button |
| 4 | Krishna responds in Hinglish | Check response language |
| 5 | Typing indicator shows | Dots animate while waiting |
| 6 | New conversation works | Click "Naya Samvad" button |
| 7 | Messages scroll properly | Send several messages |

---

## What's Next?

Tell me **"Step 6 done"** and I'll create **Step 7: Integration Testing** followed by **Step 8: Polish & Refinement**.

We're almost done — the core system is complete! 🎉

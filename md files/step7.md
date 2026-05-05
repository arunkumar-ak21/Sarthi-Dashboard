# Step 7: UI Polish & Predefined Questions

> **Goal:** Make the dashboard more interactive by adding clickable "Quick Questions" and message timestamps.
> **Time Estimate:** 10 minutes

---

## What You'll Do in This Step

| Task | Status |
|------|--------|
| Update `frontend/index.html` — Add quick question buttons | [ ] |
| Update `frontend/style.css` — Style the new buttons | [ ] |
| Update `frontend/script.js` — Make the buttons work & add timestamps | [ ] |

---

## 7.1 Update `frontend/index.html`

We need to add a "Quick Questions" section right above the chat input box. 

Open `frontend/index.html`. Find the `<!-- Input Area -->` section at the bottom, and **replace the entire footer** with this:

```html
        <!-- Input Area with Quick Questions -->
        <footer class="input-area" id="input-area">
            
            <!-- NEW: Quick Questions -->
            <div class="quick-questions" id="quick-questions">
                <button class="quick-btn">Chakravyuha kya hai?</button>
                <button class="quick-btn">Arjun ke baare mein batao</button>
                <button class="quick-btn">Karma Yoga kya hai?</button>
            </div>

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
```

---

## 7.2 Update `frontend/style.css`

Now we need to make those buttons look good. 

Open `frontend/style.css`, scroll to the very bottom, and **add this code**:

```css
/* --- Quick Questions --- */
.quick-questions {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
    overflow-x: auto;
    padding-bottom: 4px;
    scrollbar-width: none; /* Hide scrollbar Firefox */
}

.quick-questions::-webkit-scrollbar {
    display: none; /* Hide scrollbar Chrome/Safari */
}

.quick-btn {
    background: rgba(212, 168, 67, 0.05);
    border: 1px solid rgba(212, 168, 67, 0.2);
    color: var(--text-secondary);
    padding: 6px 12px;
    border-radius: 12px;
    font-family: var(--font-body);
    font-size: 0.75rem;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s ease;
}

.quick-btn:hover {
    background: rgba(212, 168, 67, 0.15);
    color: var(--gold-primary);
    border-color: var(--gold-primary);
}

/* --- Message Timestamps --- */
.message-time {
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-top: 4px;
    text-align: right;
}
.message.krishna .message-time {
    text-align: left;
}
```

---

## 7.3 Update `frontend/script.js`

Finally, we need to make the buttons actually send the message when clicked, and we'll add a timestamp to every message.

Open `frontend/script.js`.

### 1. Make Quick Buttons Work
Find the `// ============================================ / // EVENT LISTENERS` section near the bottom. Add this code right below it:

```javascript
// Quick Question buttons
document.querySelectorAll(".quick-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        messageInput.value = btn.textContent;
        sendMessage();
    });
});
```

### 2. Add Timestamps to Messages
Find the `function addMessage(role, content)` function. Replace the **entire function** with this updated version:

```javascript
function addMessage(role, content) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;

    const avatarEmoji = role === "krishna" ? "🙏" : "🧑";
    const name = role === "krishna" ? "KRISHNA" : "YOU";
    
    // Get current time like "14:30"
    const timeString = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatarEmoji}</div>
        <div>
            <div class="message-name">${name}</div>
            <div class="message-content">${escapeHtml(content)}</div>
            <div class="message-time">${timeString}</div>
        </div>
    `;

    chatArea.appendChild(messageDiv);
    scrollToBottom();
}
```

---

## 7.4 Test It Out!

1. If your `app.py` server is not running, start it:
   ```powershell
   cd backend
   python app.py
   ```
   *(If it is already running, you **must restart it** by pressing `Ctrl + C` and running `python app.py` again so it uses the new Gemma 4 E2B model!)*
   
2. Open `frontend/index.html` in your browser.
3. You should see three new buttons above the input box.
4. **Click one of the buttons** — it should instantly send the message.
5. Notice that the new `gemma4:e2b` model responds much faster!
6. Notice the small timestamps under each message.

Once everything works, tell me **"Step 7 done"**!

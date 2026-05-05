# Step 4: Context Manager — Krishna's Memory

> **Goal:** Build the session-based memory system so Krishna remembers your conversation.
> **Time Estimate:** 10-15 minutes (shortest step!)

---

## What You'll Do in This Step

| Task | Status |
|------|--------|
| Create `backend/context_manager.py` — session memory manager | [ ] |
| Test session creation, message storage, and history retrieval | [ ] |

---

## Why Do We Need This?

LLMs have **no memory**. Every API call is independent — the model doesn't remember what you said 10 seconds ago. We simulate memory by:

1. Storing all messages in a **session** (Python dictionary)
2. Sending the **entire conversation history** with every new request
3. The model reads the full history and responds as if it "remembers"

```
Without Context Manager:
  User: "Mera naam Arjun hai"      → Krishna responds
  User: "Mera naam kya hai?"       → Krishna: "Mujhe nahi pata" ❌

With Context Manager:
  User: "Mera naam Arjun hai"      → Krishna responds (saved to history)
  User: "Mera naam kya hai?"       → Krishna: "Tumhara naam Arjun hai, Parth!" ✅
  (because full history was sent with the second message)
```

---

## 4.1 Create `backend/context_manager.py`

**Open** `backend/context_manager.py` and **replace everything** with:

```python
"""
Sarthi NLP System - Context Manager
Manages conversation sessions and message history.

How it works:
- Each user gets a unique session_id (UUID)
- All messages (system prompt, user messages, Krishna's replies) are stored per session
- When sending to Ollama, we send the full history so the model has context
- Old messages are trimmed if the conversation gets too long (sliding window)

Data structure:
    sessions = {
        "session-uuid-1": [
            {"role": "system", "content": "Tum Lord Krishna ho..."},
            {"role": "user", "content": "Kaun ho tum?"},
            {"role": "assistant", "content": "Main Krishna hoon..."},
            ...
        ],
        "session-uuid-2": [...],
    }
"""

import uuid
from config import MAX_CONTEXT_MESSAGES

# In-memory storage: { session_id: [message1, message2, ...] }
sessions = {}


def create_session() -> str:
    """
    Create a new conversation session.
    
    Returns:
        A unique session ID (UUID string).
    """
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    return session_id


def add_message(session_id: str, role: str, content: str) -> None:
    """
    Add a message to a session's history.
    
    Args:
        session_id: The session identifier
        role: One of "system", "user", or "assistant"
        content: The message text
    """
    if session_id not in sessions:
        sessions[session_id] = []

    sessions[session_id].append({
        "role": role,
        "content": content
    })

    # --- Sliding Window: Trim old messages if conversation is too long ---
    # We always keep:
    #   1. The system prompt (first message) — Krishna's identity
    #   2. The most recent N messages — recent conversation context
    # This prevents the prompt from exceeding the model's token limit.
    
    messages = sessions[session_id]
    if len(messages) > MAX_CONTEXT_MESSAGES + 1:  # +1 for system prompt
        system_msg = messages[0]                   # Always keep system prompt
        recent = messages[-(MAX_CONTEXT_MESSAGES):]  # Keep last N messages
        sessions[session_id] = [system_msg] + recent


def get_history(session_id: str) -> list[dict]:
    """
    Get full conversation history for a session.
    
    Returns:
        List of message dicts, or empty list if session doesn't exist.
    """
    return sessions.get(session_id, [])


def clear_session(session_id: str) -> bool:
    """
    Clear and delete a session's history.
    
    Returns:
        True if session existed and was cleared, False if not found.
    """
    if session_id in sessions:
        del sessions[session_id]
        return True
    return False


def session_exists(session_id: str) -> bool:
    """Check if a session exists."""
    return session_id in sessions


# === Test: Run this file directly to verify ===
if __name__ == "__main__":
    print("=" * 50)
    print("  CONTEXT MANAGER TEST")
    print("=" * 50)
    print()
    
    # Test 1: Create session
    sid = create_session()
    print(f"[Test 1] Created session: {sid}")
    assert session_exists(sid), "Session should exist!"
    print("  PASSED - Session exists")
    print()
    
    # Test 2: Add messages
    add_message(sid, "system", "You are Krishna")
    add_message(sid, "user", "Hello")
    add_message(sid, "assistant", "Namaste sakha!")
    history = get_history(sid)
    print(f"[Test 2] Added 3 messages. History length: {len(history)}")
    assert len(history) == 3, "Should have 3 messages"
    print("  PASSED - Messages stored correctly")
    print()
    
    # Test 3: Verify message content
    print(f"[Test 3] Message roles: {[m['role'] for m in history]}")
    assert history[0]["role"] == "system"
    assert history[1]["role"] == "user"
    assert history[2]["role"] == "assistant"
    print("  PASSED - Roles are correct")
    print()
    
    # Test 4: Sliding window (trim old messages)
    print(f"[Test 4] Testing sliding window (MAX_CONTEXT = {MAX_CONTEXT_MESSAGES})...")
    for i in range(30):
        add_message(sid, "user", f"Message {i}")
        add_message(sid, "assistant", f"Reply {i}")
    history = get_history(sid)
    print(f"  After 60+ messages, history length: {len(history)}")
    assert history[0]["role"] == "system", "System prompt should always be first!"
    assert len(history) <= MAX_CONTEXT_MESSAGES + 1, "Should be trimmed"
    print("  PASSED - Old messages trimmed, system prompt preserved")
    print()
    
    # Test 5: Clear session
    cleared = clear_session(sid)
    print(f"[Test 5] Cleared session: {cleared}")
    assert cleared == True
    assert not session_exists(sid), "Session should be gone"
    print("  PASSED - Session cleared")
    print()
    
    # Test 6: Non-existent session
    fake_history = get_history("fake-id")
    print(f"[Test 6] Fake session history: {fake_history}")
    assert fake_history == [], "Should return empty list"
    print("  PASSED - Fake session returns empty")
    print()
    
    print("=" * 50)
    print("  ALL 6 TESTS PASSED!")
    print("=" * 50)
```

---

## 4.2 Run the Test

```powershell
cd backend
python context_manager.py
```

**Expected output:**
```
==================================================
  CONTEXT MANAGER TEST
==================================================

[Test 1] Created session: <some-uuid>
  PASSED - Session exists

[Test 2] Added 3 messages. History length: 3
  PASSED - Messages stored correctly

[Test 3] Message roles: ['system', 'user', 'assistant']
  PASSED - Roles are correct

[Test 4] Testing sliding window (MAX_CONTEXT = 20)...
  After 60+ messages, history length: 21
  PASSED - Old messages trimmed, system prompt preserved

[Test 5] Cleared session: True
  PASSED - Session cleared

[Test 6] Fake session history: []
  PASSED - Fake session returns empty

==================================================
  ALL 6 TESTS PASSED!
==================================================
```

All 6 tests should pass. If any fail, the error message will tell you exactly what went wrong.

---

## What You Built in This Step

```
backend/
├── context_manager.py   ✅ Session memory manager (NEW)
├── character_engine.py  ✅ (Step 3)
├── config.py            ✅ (Step 2)
├── llm_client.py        ✅ (Step 2)
└── knowledge/
    └── krishna_knowledge.json  ✅ (Step 3)
```

**Architecture so far:**
```
User Message
    |
    v
context_manager.py ──> Stores message in session history
    |
    v
character_engine.py ──> Adds system prompt (Krishna's identity)
    |
    v
llm_client.py ──> Sends full history to Ollama
    |
    v
Ollama (gemma3:4b) ──> Returns Krishna's response
    |
    v
context_manager.py ──> Saves response to session history
```

---

## Final Checklist for Step 4

| # | Check | How to Verify |
|---|-------|--------------|
| 1 | All 6 tests pass | `python context_manager.py` |
| 2 | System prompt preserved after trimming | Test 4 output shows system prompt is first |
| 3 | Non-existent sessions handled | Test 6 returns empty list |

---

## What's Next?

Tell me **"Step 4 done"** and I'll create **Step 5: Flask API Server — The Bridge**.

Step 5 wires everything together into a REST API — this is where `config + llm_client + character_engine + context_manager` all connect. After Step 5, your backend is complete!

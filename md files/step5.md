# Step 5: Flask API Server — The Bridge

> **Goal:** Create the REST API that connects frontend to backend, wiring all modules together.
> **Time Estimate:** 15-20 minutes
> **After this step, your entire backend is complete!**

---

## What You'll Do in This Step

| Task | Status |
|------|--------|
| Create `backend/app.py` — Flask server with all API routes | [ ] |
| Test `/api/health` — server is alive | [ ] |
| Test `/api/session/new` — create a new conversation | [ ] |
| Test `/api/chat` — talk to Krishna | [ ] |
| Test `/api/session/clear` — reset conversation | [ ] |
| Test context — Krishna remembers previous messages | [ ] |

---

## 5.1 Create `backend/app.py`

**Open** `backend/app.py` and **replace everything** with:

```python
"""
Sarthi NLP System - Flask API Server
The bridge between the frontend dashboard and Krishna's brain.

API Endpoints:
    GET  /api/health         - Check if server is running
    POST /api/session/new    - Start a new conversation
    POST /api/chat           - Send a message, get Krishna's reply
    POST /api/session/clear  - Clear conversation history
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from character_engine import build_system_prompt, get_greeting
from context_manager import (
    create_session, add_message, get_history,
    clear_session, session_exists
)
from llm_client import get_response, check_ollama_connection

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend (different port) to call this backend


# ============================================
# HEALTH CHECK
# ============================================

@app.route("/api/health", methods=["GET"])
def health():
    """Check if the server and Ollama are running."""
    ollama_ok = check_ollama_connection()
    return jsonify({
        "status": "ok" if ollama_ok else "warning",
        "character": "Krishna",
        "ollama_connected": ollama_ok
    })


# ============================================
# SESSION MANAGEMENT
# ============================================

@app.route("/api/session/new", methods=["POST"])
def new_session():
    """
    Start a new conversation with Krishna.
    
    Returns:
        session_id: Unique ID for this conversation
        greeting: Krishna's opening message
    """
    # Create a new session
    session_id = create_session()

    # Add Krishna's system prompt as the first message
    system_prompt = build_system_prompt()
    add_message(session_id, "system", system_prompt)

    # Get Krishna's greeting
    greeting = get_greeting()

    print(f"[NEW SESSION] {session_id}")

    return jsonify({
        "session_id": session_id,
        "greeting": greeting
    })


@app.route("/api/session/clear", methods=["POST"])
def clear():
    """Clear conversation history for a session."""
    data = request.get_json()

    if not data or "session_id" not in data:
        return jsonify({"error": "session_id missing"}), 400

    cleared = clear_session(data["session_id"])
    print(f"[CLEAR SESSION] {data['session_id']} - {'cleared' if cleared else 'not found'}")

    return jsonify({
        "cleared": cleared,
        "message": "Session cleared" if cleared else "Session not found"
    })


# ============================================
# CHAT — THE MAIN ENDPOINT
# ============================================

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Send a message to Krishna and get his response.
    
    Request body:
        {
            "session_id": "uuid-string",
            "message": "Krishna, tum kaun ho?"
        }
    
    Response:
        {
            "session_id": "uuid-string",
            "response": "Main Krishna hoon, Vasudev-putra...",
            "context_length": 5
        }
    """
    data = request.get_json()

    # --- Validate request ---
    if not data or "session_id" not in data or "message" not in data:
        return jsonify({"error": "session_id aur message dono zaroori hain"}), 400

    session_id = data["session_id"]
    user_message = data["message"].strip()

    if not user_message:
        return jsonify({"error": "Message khali nahi ho sakta"}), 400

    if not session_exists(session_id):
        return jsonify({"error": "Session nahi mili. Naya session shuru karo."}), 404

    # --- Add user message to history ---
    add_message(session_id, "user", user_message)

    # --- Get full history and send to Ollama ---
    history = get_history(session_id)
    
    print(f"[CHAT] Session: {session_id[:8]}... | User: {user_message[:50]}...")
    
    krishna_response = get_response(history)

    # --- Save Krishna's response to history ---
    add_message(session_id, "assistant", krishna_response)

    print(f"[CHAT] Krishna: {krishna_response[:80]}...")

    return jsonify({
        "session_id": session_id,
        "response": krishna_response,
        "context_length": len(get_history(session_id))
    })


# ============================================
# START SERVER
# ============================================

if __name__ == "__main__":
    print()
    print("=" * 50)
    print("  SARTHI NLP SERVER")
    print("  Krishna is awakening...")
    print("=" * 50)
    print()
    print("  API Endpoints:")
    print("    GET  /api/health        - Health check")
    print("    POST /api/session/new   - New conversation")
    print("    POST /api/chat          - Talk to Krishna")
    print("    POST /api/session/clear - Clear history")
    print()
    print("  Server: http://localhost:5000")
    print("=" * 50)
    print()
    
    app.run(debug=True, port=5000)
```

---

## 5.2 Start the Server

```powershell
cd backend
python app.py
```

**Expected output:**
```
==================================================
  SARTHI NLP SERVER
  Krishna is awakening...
==================================================

  API Endpoints:
    GET  /api/health        - Health check
    POST /api/session/new   - New conversation
    POST /api/chat          - Talk to Krishna
    POST /api/session/clear - Clear history

  Server: http://localhost:5000
==================================================

[OK] Ollama is running. Model 'gemma3:4b' is available.
 * Running on http://127.0.0.1:5000
```

> **Keep this terminal running!** Open a **second terminal** for testing.

---

## 5.3 Test the API

Open a **new terminal** (keep the server running in the first one):

```powershell
cd "C:\Users\kumar\Pictures\Minor project\chakravyuh-backend"
.\venv\Scripts\Activate
```

### Test 1: Health Check

```powershell
curl http://localhost:5000/api/health
```

**Expected:** `{"character":"Krishna","ollama_connected":true,"status":"ok"}`

### Test 2: Create New Session

```powershell
curl -X POST http://localhost:5000/api/session/new -H "Content-Type: application/json"
```

**Expected:** Returns a `session_id` and Krishna's greeting. **Copy the session_id** — you'll need it for the next test.

### Test 3: Chat with Krishna

Replace `YOUR_SESSION_ID` with the actual ID from Test 2:

```powershell
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d "{\"session_id\":\"YOUR_SESSION_ID\",\"message\":\"Krishna, tum kaun ho?\"}"
```

**Expected:** Krishna responds in Hinglish with his introduction.

### Test 4: Context Test (Follow-up)

Use the **same session_id**:

```powershell
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d "{\"session_id\":\"YOUR_SESSION_ID\",\"message\":\"Chakravyuha ke baare mein batao\"}"
```

**Expected:** Krishna talks about Chakravyuha. The `context_length` should be higher than before (showing history is growing).

### Test 5: Clear Session

```powershell
curl -X POST http://localhost:5000/api/session/clear -H "Content-Type: application/json" -d "{\"session_id\":\"YOUR_SESSION_ID\"}"
```

**Expected:** `{"cleared":true,"message":"Session cleared"}`

### Test 6: Error Handling

```powershell
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d "{\"session_id\":\"fake-id\",\"message\":\"Hello\"}"
```

**Expected:** `{"error":"Session nahi mili. Naya session shuru karo."}` with status 404.

---

## Alternative: Test with Python Script

If `curl` is giving issues with JSON escaping on PowerShell, create `backend/test_api.py`:

```python
"""Temporary test - delete after verification."""
import requests

BASE = "http://localhost:5000"

print("=" * 50)
print("  API TEST")
print("=" * 50)

# Test 1: Health
print("\n[Test 1] Health check...")
r = requests.get(f"{BASE}/api/health")
print(f"  Status: {r.json()}")

# Test 2: New session
print("\n[Test 2] Creating new session...")
r = requests.post(f"{BASE}/api/session/new")
data = r.json()
sid = data["session_id"]
print(f"  Session: {sid[:8]}...")
print(f"  Greeting: {data['greeting'][:80]}...")

# Test 3: Chat
print("\n[Test 3] Chatting with Krishna...")
r = requests.post(f"{BASE}/api/chat", json={"session_id": sid, "message": "Krishna, tum kaun ho?"})
data = r.json()
print(f"  Krishna: {data['response'][:100]}...")
print(f"  Context length: {data['context_length']}")

# Test 4: Follow-up (context test)
print("\n[Test 4] Follow-up question (context test)...")
r = requests.post(f"{BASE}/api/chat", json={"session_id": sid, "message": "Arjun ke baare mein batao"})
data = r.json()
print(f"  Krishna: {data['response'][:100]}...")
print(f"  Context length: {data['context_length']}")

# Test 5: Clear
print("\n[Test 5] Clearing session...")
r = requests.post(f"{BASE}/api/session/clear", json={"session_id": sid})
print(f"  Result: {r.json()}")

# Test 6: Error
print("\n[Test 6] Error handling (fake session)...")
r = requests.post(f"{BASE}/api/chat", json={"session_id": "fake", "message": "Hello"})
print(f"  Error: {r.json()} (Status: {r.status_code})")

print("\n" + "=" * 50)
print("  ALL TESTS DONE!")
print("=" * 50)
```

Run it (in the second terminal, while server is running):
```powershell
cd backend
python test_api.py
```

---

## Troubleshooting

### "Address already in use" error
- Another process is using port 5000. Either:
  - Kill it: `Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process`
  - Or change the port in `app.py`: `app.run(debug=True, port=5001)`

### curl gives weird JSON errors on PowerShell
- PowerShell handles quotes differently. Use the Python test script (`test_api.py`) instead — it's more reliable.

### "ModuleNotFoundError" when starting server
- Make sure venv is activated: `.\venv\Scripts\Activate`
- Make sure you're in the `backend/` directory

### Server starts but chat returns errors
- Check that Ollama is running: `ollama list`
- Check the server terminal — error details are printed there

---

## What You Built in This Step

```
backend/
├── app.py               ✅ Flask API Server (NEW - THE BRIDGE)
├── context_manager.py   ✅ (Step 4)
├── character_engine.py  ✅ (Step 3)
├── config.py            ✅ (Step 2)
├── llm_client.py        ✅ (Step 2)
└── knowledge/
    └── krishna_knowledge.json  ✅ (Step 3)
```

**Your backend is now COMPLETE! Full flow:**
```
Frontend (Step 6)
    |
    | HTTP POST /api/chat
    v
app.py (Flask) ──> Validates request
    |
    v
context_manager.py ──> Adds user message to session
    |
    v
character_engine.py ──> System prompt (Krishna's identity)
    |
    v
llm_client.py ──> Sends to Ollama
    |
    v
Ollama (gemma3:4b) ──> Returns response
    |
    v
context_manager.py ──> Saves response
    |
    v
app.py ──> Returns JSON to frontend
```

---

## Final Checklist for Step 5

| # | Check | How to Verify |
|---|-------|--------------|
| 1 | Server starts without errors | `python app.py` shows endpoints |
| 2 | Health check works | `/api/health` returns OK |
| 3 | New session works | `/api/session/new` returns ID + greeting |
| 4 | Chat works | `/api/chat` returns Krishna's response |
| 5 | Context works | Follow-up question shows growing context_length |
| 6 | Clear works | `/api/session/clear` returns cleared: true |
| 7 | Errors handled | Fake session returns 404 |

---

## What's Next?

Tell me **"Step 5 done"** and I'll create **Step 6: Frontend Dashboard**.

Step 6 is the fun part — we build a beautiful Mahabharata-themed chat interface! 

# Step 2: Backend Foundation — Config & Ollama LLM Client

> **Goal:** Create the configuration module and the LLM client that talks to Ollama.
> **Time Estimate:** 15-20 minutes
> **Prerequisites:** Step 1 completed (Ollama installed, model pulled, venv activated)

---

## What You'll Do in This Step

| Task | Status |
|------|--------|
| Create `backend/config.py` — loads settings from `.env` | [ ] |
| Create `backend/llm_client.py` — talks to Ollama API | [ ] |
| Create `backend/test_llm.py` — test script to verify connection | [ ] |
| Test that Krishna responds via Ollama | [ ] |
| Delete test file after verification | [ ] |

---

## Before You Start

Open your terminal in VS Code (`Ctrl + ~`) and make sure:

### 1. You're in the project directory:
```powershell
cd "C:\Users\kumar\Pictures\Minor project\chakravyuh-backend"
```

### 2. Your venv is activated:
```powershell
.\venv\Scripts\Activate
```
You should see `(venv)` in your prompt. If not, activate it first.

### 3. Ollama is running:
```powershell
ollama list
```
You should see `gemma3:4b` in the list. If Ollama is not running, open a **separate terminal** and run:
```powershell
ollama serve
```

---

## 2.1 Create `backend/config.py`

**What this file does:** Loads your project configuration (model name, Ollama URL, etc.) from the `.env` file. This way, you can change settings without touching any code.

**Open** `backend/config.py` in VS Code and **replace everything** with:

```python
"""
Sarthi NLP System - Configuration Module
Loads settings from .env file in project root.
"""

import os
from dotenv import load_dotenv

# Load .env file from project root (one folder up from backend/)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ============================================
# OLLAMA CONFIGURATION
# ============================================

# Which model to use (change this to switch models)
# Options: gemma3:4b (recommended), gemma3:1b (faster), gemma3:12b (better quality)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")

# Where Ollama is running (default: localhost on port 11434)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ============================================
# RESPONSE SETTINGS
# ============================================

# Maximum number of conversation messages to remember per session
# Higher = more context but slower and more memory
MAX_CONTEXT_MESSAGES = 20

# Maximum number of tokens (words/pieces) in Krishna's response
# 500 tokens ≈ 3-6 sentences (good for conversation)
MAX_RESPONSE_TOKENS = 500

# Creativity level: 0.0 = robotic/predictable, 1.0 = very creative/random
# 0.8 is a good balance for character roleplay
TEMPERATURE = 0.8

# ============================================
# VALIDATION
# ============================================

# Print config on startup (helpful for debugging)
if __name__ == "__main__":
    print("=== Sarthi NLP Configuration ===")
    print(f"  Model:          {OLLAMA_MODEL}")
    print(f"  Ollama URL:     {OLLAMA_BASE_URL}")
    print(f"  Max Context:    {MAX_CONTEXT_MESSAGES} messages")
    print(f"  Max Tokens:     {MAX_RESPONSE_TOKENS}")
    print(f"  Temperature:    {TEMPERATURE}")
    print("================================")
```

### Understanding the Code (Line by Line):

| Line | What It Does |
|------|-------------|
| `from dotenv import load_dotenv` | Imports the library that reads `.env` files |
| `load_dotenv(...)` | Reads your `.env` file and loads variables into the environment |
| `os.getenv("OLLAMA_MODEL", "gemma3:4b")` | Gets the model name from `.env`, uses `"gemma3:4b"` as default if not found |
| `MAX_CONTEXT_MESSAGES = 20` | Krishna will remember the last 20 messages in a conversation |
| `MAX_RESPONSE_TOKENS = 500` | Krishna's replies will be max ~500 tokens (3-6 sentences) |
| `TEMPERATURE = 0.8` | Controls creativity — 0.8 means creative but coherent |

### Test config.py:

```powershell
cd backend
python config.py
```

**Expected output:**
```
=== Sarthi NLP Configuration ===
  Model:          gemma3:4b
  Ollama URL:     http://localhost:11434
  Max Context:    20 messages
  Max Tokens:     500
  Temperature:    0.8
================================
```

If you see this, `config.py` is working correctly.

---

## 2.2 Create `backend/llm_client.py`

**What this file does:** This is the module that actually talks to Ollama. It takes a conversation history (list of messages), sends it to the local AI model, and returns the response.

**Open** `backend/llm_client.py` in VS Code and **replace everything** with:

```python
"""
Sarthi NLP System - Ollama LLM Client
Sends conversation history to the local Ollama model and returns responses.

How Ollama works:
- Ollama runs a local HTTP server at http://localhost:11434
- It exposes a REST API endpoint: POST /api/chat
- We send messages in the format: [{"role": "system/user/assistant", "content": "..."}]
- It returns the AI's response as JSON
"""

import requests
from config import OLLAMA_MODEL, OLLAMA_BASE_URL, MAX_RESPONSE_TOKENS, TEMPERATURE


def get_response(conversation_history: list[dict]) -> str:
    """
    Send conversation history to Ollama and get Krishna's response.

    Args:
        conversation_history: List of message dicts, each with 'role' and 'content'.
            Roles can be:
                - "system"    : Instructions for how the AI should behave (Krishna's personality)
                - "user"      : What the human typed
                - "assistant" : What the AI (Krishna) previously said
            
            Example:
                [
                    {"role": "system", "content": "You are Lord Krishna..."},
                    {"role": "user", "content": "Kaun ho tum?"},
                    {"role": "assistant", "content": "Main Krishna hoon, Vasudev ka putra..."},
                    {"role": "user", "content": "Arjun ke baare mein batao"},
                ]

    Returns:
        str: Krishna's response text.
    """
    try:
        # Build the request payload for Ollama's /api/chat endpoint
        # Ollama uses the SAME message format as OpenAI — no conversion needed!
        payload = {
            "model": OLLAMA_MODEL,
            "messages": conversation_history,
            "stream": False,        # Wait for complete response (not streaming)
            "options": {
                "num_predict": MAX_RESPONSE_TOKENS,   # Max response length
                "temperature": TEMPERATURE,             # Creativity level
            }
        }

        # Send POST request to Ollama's local server
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=120     # 2 minute timeout (first response can be slow)
        )

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data["message"]["content"]
        else:
            print(f"[ERROR] Ollama returned HTTP {response.status_code}: {response.text}")
            return "Kshama karo, mere mann mein kuch gadbad ho gayi. Phir se poochho."

    except requests.exceptions.ConnectionError:
        # Ollama is not running
        print("[ERROR] Cannot connect to Ollama! Is it running?")
        print("        Start it with: ollama serve")
        return "Divya connection toot gaya hai. Pehle Ollama ko chalao aur phir prayaas karo."

    except requests.exceptions.Timeout:
        # Request took too long
        print("[ERROR] Ollama took too long to respond (timeout).")
        return "Mujhe uttar dene mein samay lag raha hai. Kripya phir se prayaas karo."

    except Exception as e:
        # Any other unexpected error
        print(f"[ERROR] Unexpected error: {e}")
        return "Kshama karo, mere mann mein kuch gadbad ho gayi. Phir se poochho."


def check_ollama_connection() -> bool:
    """
    Check if Ollama is running and the model is available.
    
    Returns:
        True if Ollama is running and model is loaded, False otherwise.
    """
    try:
        # Ollama has a /api/tags endpoint that lists available models
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if OLLAMA_MODEL in model_names or any(OLLAMA_MODEL in name for name in model_names):
                print(f"[OK] Ollama is running. Model '{OLLAMA_MODEL}' is available.")
                return True
            else:
                print(f"[WARNING] Ollama is running but model '{OLLAMA_MODEL}' not found.")
                print(f"          Available models: {model_names}")
                print(f"          Pull it with: ollama pull {OLLAMA_MODEL}")
                return False
        else:
            print(f"[ERROR] Ollama returned unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Ollama is not running. Start it with: ollama serve")
        return False
```

### Understanding the Code:

| Function | Purpose |
|----------|---------|
| `get_response(history)` | Main function — sends messages to Ollama and returns Krishna's reply |
| `check_ollama_connection()` | Helper — checks if Ollama is running and the model is available |

**Key Concept — How Ollama API works:**
```
Your Python code                    Ollama (running locally)
      |                                      |
      |--- POST /api/chat ---------------->  |
      |    {model, messages, options}        |
      |                                      |  (AI generates response)
      |  <--- JSON response ---------------  |
      |    {message: {content: "..."}}       |
```

It's just HTTP requests — same as any web API, but running on your own machine!

---

## 2.3 Create Test Script

**This is temporary** — just to verify everything works before we build more.

**Create a new file** `backend/test_llm.py`:

```python
"""
Temporary test script - delete after verification.
Tests the Ollama connection and Krishna's response.
"""

from llm_client import get_response, check_ollama_connection

print("=" * 50)
print("  SARTHI NLP - Ollama Connection Test")
print("=" * 50)
print()

# Step 1: Check if Ollama is running
print("[Test 1] Checking Ollama connection...")
is_connected = check_ollama_connection()
print()

if not is_connected:
    print("FAILED: Fix the connection issue above before continuing.")
    exit(1)

# Step 2: Test a simple response (no character prompt)
print("[Test 2] Testing basic response...")
basic_history = [
    {"role": "user", "content": "Say 'Namaste, main kaam kar raha hoon' in one line"}
]
basic_response = get_response(basic_history)
print(f"  Response: {basic_response}")
print()

# Step 3: Test Krishna character response
print("[Test 3] Testing Krishna character (Hinglish)...")
krishna_history = [
    {
        "role": "system",
        "content": (
            "Tum Lord Krishna ho Mahabharata se. "
            "Tum Hinglish mein baat karo (Hindi words lekin English letters mein likho). "
            "Kabhi bhi apna character mat todo. "
            "Example style: 'Parth, yeh dharma ka rasta hai. Tum apna kartavya nibhao.'"
        )
    },
    {"role": "user", "content": "Krishna, tum kaun ho? Apna parichay do."}
]
krishna_response = get_response(krishna_history)
print(f"  Krishna: {krishna_response}")
print()

# Step 4: Test context (follow-up question)
print("[Test 4] Testing context memory...")
krishna_history.append({"role": "assistant", "content": krishna_response})
krishna_history.append({"role": "user", "content": "Arjun ke baare mein batao"})
context_response = get_response(krishna_history)
print(f"  Krishna: {context_response}")
print()

print("=" * 50)
print("  ALL TESTS PASSED! Krishna is ready.")
print("  You can delete this test file now.")
print("=" * 50)
```

---

## 2.4 Run the Test

Make sure you're in the `backend/` directory with venv activated:

```powershell
cd "C:\Users\kumar\Pictures\Minor project\chakravyuh-backend\backend"
python test_llm.py
```

### What to expect:

**First run will be slow** (10-30 seconds) — Ollama needs to load the model into memory. Subsequent runs will be faster (2-5 seconds).

**Successful output looks like:**
```
==================================================
  SARTHI NLP - Ollama Connection Test
==================================================

[Test 1] Checking Ollama connection...
[OK] Ollama is running. Model 'gemma3:4b' is available.

[Test 2] Testing basic response...
  Response: Namaste, main kaam kar raha hoon

[Test 3] Testing Krishna character (Hinglish)...
  Krishna: Namaste, main Krishna hoon, Vasudev aur Devaki ka putra...

[Test 4] Testing context memory...
  Krishna: Arjun, mere priye sakha! Woh Pandu putra hai...

==================================================
  ALL TESTS PASSED! Krishna is ready.
  You can delete this test file now.
==================================================
```

> The exact wording will be different each time — that's normal! What matters is:
> - Test 1: Connection works
> - Test 3: Response is in Hinglish (Hindi words, English letters)
> - Test 4: Krishna references the previous conversation (context works)

---

## 2.5 Clean Up

After all tests pass, **delete the test file**:

```powershell
Remove-Item test_llm.py
```

Or just delete it from VS Code's file explorer. It was only for verification.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"
- Your venv is not activated. Run: `.\venv\Scripts\Activate` (from project root)
- Or dependencies not installed. Run: `pip install -r requirements.txt` (from backend/)

### "ModuleNotFoundError: No module named 'requests'"
- Same as above — activate venv and install dependencies

### "[ERROR] Cannot connect to Ollama!"
- Ollama is not running. Open a separate terminal and run: `ollama serve`
- If it says "address already in use" — Ollama is already running, which is fine
- Check if the URL in `.env` matches: `OLLAMA_BASE_URL=http://localhost:11434`

### "[WARNING] Model 'gemma3:4b' not found"
- You haven't pulled the model yet. Run: `ollama pull gemma3:4b`
- Or check your `.env` file — the model name must match exactly what `ollama list` shows

### Response is in Devanagari (Hindi script) instead of Roman/English letters
- This can happen occasionally — it will be fixed in Step 3 when we write the full character prompt
- The system prompt in Step 3 explicitly instructs the model to use Roman script only
- For now, if Test 3 gives ANY response, it's working fine

### Response is too slow (more than 60 seconds)
- Check your RAM usage (Task Manager → Performance tab)
- If RAM is maxed out, try the smaller model:
  1. Edit `.env`: change `OLLAMA_MODEL=gemma3:4b` to `OLLAMA_MODEL=gemma3:1b`
  2. Pull it: `ollama pull gemma3:1b`
  3. Run test again

### "ModuleNotFoundError: No module named 'config'"
- You must run the test from inside the `backend/` directory
- `cd backend` first, then `python test_llm.py`

---

## What You Built in This Step

```
backend/
├── config.py        ✅ Reads .env settings (model name, URL, parameters)
├── llm_client.py    ✅ Sends messages to Ollama, returns AI responses
└── test_llm.py      🗑️ Temporary test (delete after verification)
```

**Architecture so far:**
```
.env  ──>  config.py  ──>  llm_client.py  ──>  Ollama (local)
                                                    |
                                              gemma3:4b model
                                                    |
                                            Krishna's response
```

---

## Final Checklist for Step 2

| # | Check | How to Verify |
|---|-------|--------------|
| 1 | `config.py` runs without errors | `python config.py` shows config values |
| 2 | Ollama connection works | Test 1 says "[OK] Ollama is running" |
| 3 | Basic response works | Test 2 returns any text |
| 4 | Krishna character works | Test 3 returns Hinglish response |
| 5 | Context memory works | Test 4 references previous conversation |
| 6 | Test file deleted | `test_llm.py` removed from backend/ |

---

## What's Next?

Once all checks pass, tell me **"Step 2 done"** and I'll provide the code for **Step 3: Character Engine — Krishna's Soul**.

In Step 3, we'll build:
- `krishna_knowledge.json` — Everything Krishna knows (characters, events, relationships)
- `character_engine.py` — The system prompt that transforms the AI into Krishna

This is the **most important step** — it's what makes Krishna feel real.

---

> *"Pehle neev mazboot karo, phir mahal khada hoga."*
> (First strengthen the foundation, then the palace will stand.)

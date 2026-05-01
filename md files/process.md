# 🛠️ Sarthi NLP System — Complete Build Process

> A beginner-friendly, step-by-step guide for your 6th semester minor project.
> Follow each step in order. Move to the next only when the current one works.

---

## 📋 Prerequisites (What You Need Before Starting)

| Requirement | How to Get It |
|-------------|--------------|
| **Python 3.10+** | Download from [python.org](https://python.org). During install, ✅ check "Add Python to PATH" |
| **VS Code** | You already have this ✅ |
| **Git** | Download from [git-scm.com](https://git-scm.com) (optional but recommended) |
| **Ollama** | Download from [ollama.com](https://ollama.com/download) — install it, it runs locally on your machine |
| **Basic Knowledge** | Python basics, what an API is, HTML/CSS/JS basics |

### 🤖 Why Ollama (Local LLM) Instead of Cloud APIs?

| Factor | Ollama (Local) | Cloud API (Gemini/OpenAI) |
|--------|---------------|---------------------------|
| **Cost** | ✅ Completely free forever | ⚠️ Free tier has limits, then paid |
| **Internet** | ✅ Works fully offline | ❌ Needs internet always |
| **Game (V2)** | ✅ No network latency, instant | ❌ Network delay kills gameplay |
| **Privacy** | ✅ Data stays on your machine | ⚠️ Sent to cloud servers |
| **Rate Limits** | ✅ None — unlimited requests | ❌ 15 req/min on free tier |
| **Viva Impact** | ✅ "Running my own AI locally" | Less impressive |
| **Demo Day** | ✅ No WiFi needed | ❌ No WiFi = broken demo |

### 🧠 Which Ollama Model to Use?

Since Krishna speaks in **Hinglish** (Hindi in Roman/English script — e.g. *"Yeh Parth, tum yaha kya kar rhe ho"*), we need a model with strong Indic language training. **Google's Gemma 3 family wins here** — Google has the most Hindi/Hinglish training data of any model family.

| Model | Download Size | RAM Needed | Hinglish Quality | Speed | When to Use |
|-------|-------------|-----------|-----------------|-------|-------------|
| **`gemma3:4b`** ⭐ | ~3 GB | 6 GB+ | ⭐⭐⭐⭐⭐ | Fast | **V1 Dashboard — RECOMMENDED** |
| **`gemma3:12b`** | ~8 GB | 12 GB+ | ⭐⭐⭐⭐⭐ | Medium | Best quality if you have the RAM |
| **`gemma2:9b`** | ~5.4 GB | 10 GB+ | ⭐⭐⭐⭐ | Medium | Good alternative |
| **`gemma3:1b`** | ~1 GB | 4 GB+ | ⭐⭐⭐ | Very Fast | **V2 Game — fastest responses** |
| **`phi3:mini`** | ~2.3 GB | 6 GB+ | ⭐⭐⭐⭐ | Fast | Low-end hardware fallback |
| **`llama3.1:8b`** | ~4.7 GB | 8 GB+ | ⭐⭐⭐ | Medium | Good English, weaker Hinglish |
| **`mistral:7b`** | ~4.1 GB | 8 GB+ | ⭐⭐ | Medium | Weak Hindi support |

> **Our pick: `gemma3:4b`** for V1. Best Hinglish quality, fast, and lightweight (~6 GB RAM).
> For V2 game integration, we can use `gemma3:1b` for fastest responses (just one config change).
>
> ⚠️ **Why not Llama/Mistral?** They often drift to pure English or switch to Devanagari (हिंदी) script instead of staying in romanized Hindi. Gemma 3 handles Hinglish naturally because of Google's massive Indic language dataset.

---

## 🧠 Key Concepts (Read Before Coding)

### What is an LLM?
A Large Language Model (like Gemini, ChatGPT) is an AI that generates human-like text. We don't *train* it — we *instruct* it using prompts. Think of it as a very smart actor — you give it a script (system prompt) and it plays the role.

### What is Prompt Engineering?
The art of writing instructions (prompts) that make the LLM behave exactly how you want. For Sarthi, we write a prompt that says *"You are Lord Krishna, speak like him, never break character."*

### What is Context Handling?
Sending the entire conversation history with each new message so the LLM "remembers" what was said before. LLMs have no memory by default — we simulate memory by replaying the conversation.

### What is a REST API?
A way for two programs (frontend & backend) to talk to each other over HTTP. The frontend sends a JSON request, the backend processes it and sends a JSON response.

### How Our System Works (Simple Flow)
```
User types message
       ↓
Frontend sends message to Backend (HTTP POST)
       ↓
Backend adds message to conversation history
       ↓
Backend builds a prompt: System Prompt + History + New Message
       ↓
Backend sends prompt to Ollama (local LLM)
       ↓
Ollama returns Krishna's response
       ↓
Backend saves response to history & sends it to Frontend
       ↓
Frontend displays Krishna's response
```

---

## 📁 Final Project Structure

```
chakravyuh-backend/
│
├── process.md                       # This file (your guide)
├── version1.md                      # Project plan document
├── .env                             # Configuration (model name, etc.)
├── .gitignore                       # Files to ignore in git
│
├── backend/
│   ├── app.py                       # Flask server with API routes
│   ├── config.py                    # Loads environment variables
│   ├── llm_client.py                # Talks to Ollama (local LLM)
│   ├── character_engine.py          # Krishna's personality & prompt
│   ├── context_manager.py           # Conversation memory manager
│   ├── requirements.txt             # Python dependencies
│   └── knowledge/
│       └── krishna_knowledge.json   # Krishna's knowledge base
│
└── frontend/
    ├── index.html                   # Chat dashboard page
    ├── style.css                    # Mahabharata-themed styling
    └── script.js                    # Chat logic & API calls
```

---

---

# 🪜 STEP-BY-STEP BUILD PROCESS

---

## ✅ STEP 1: Project Setup & Environment

**Goal:** Create the folder structure, install Ollama, pull the model, set up Python environment.

### 1.1 Install Ollama

1. Download Ollama from [ollama.com/download](https://ollama.com/download)
2. Install it (just run the installer, it's simple)
3. After installation, open a terminal and verify:

```powershell
ollama --version
```

You should see a version number. If you see an error, restart your terminal.

### 1.2 Pull the LLM Model

This downloads the AI model to your machine (~4.7 GB download, one-time):

```powershell
ollama pull gemma3:4b
```

> ⏳ This will take a few minutes depending on your internet. Go grab chai ☕

Verify it works:
```powershell
ollama run gemma3:4b "Say namaste in Hinglish (Hindi written in English letters)"
```

You should see a response. Press `Ctrl+D` or type `/bye` to exit.

### 1.3 Create Folder Structure

Open terminal in `c:\Users\kumar\Pictures\Minor project\chakravyuh-backend\` and run:

```powershell
# Create backend folders
mkdir backend
mkdir backend\knowledge

# Create frontend folder
mkdir frontend
```

### 1.4 Create Python Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it (run this EVERY TIME you open a new terminal)
.\venv\Scripts\Activate
```

> ⚠️ You should see `(venv)` at the start of your terminal prompt. If not, the venv is not active.

### 1.5 Create `backend/requirements.txt`

```txt
flask==3.1.0
flask-cors==5.0.1
requests==2.32.3
python-dotenv==1.1.0
```

> **Note:** No `google-generativeai` needed! Ollama runs locally and we talk to it via HTTP requests — the `requests` library is all we need.

### 1.6 Install Dependencies

```powershell
pip install -r backend/requirements.txt
```

### 1.7 Create `.env` File (in project root)

```env
OLLAMA_MODEL=gemma3:4b
OLLAMA_BASE_URL=http://localhost:11434
```

> No API keys needed! Ollama runs locally. The `.env` just stores config so you can easily switch models later.

### 1.8 Create `.gitignore`

```
venv/
.env
__pycache__/
*.pyc
```

### ✅ How to verify Step 1 is done:
- `ollama --version` shows a version number
- `ollama list` shows `gemma3:4b` in the list
- `venv` folder exists in your project
- Running `pip list` shows flask, flask-cors, requests, python-dotenv
- `.env` file has the model name and URL

**Tell me "Step 1 done" to proceed →**

---

## ✅ STEP 2: Backend Foundation — Config & LLM Client

**Goal:** Connect to Ollama (local LLM) and confirm it responds.

### 2.1 Create `backend/config.py`

**What this does:** Loads configuration from the `.env` file. No API keys needed since Ollama is local!

```python
import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MAX_CONTEXT_MESSAGES = 20    # Max messages to remember per session
MAX_RESPONSE_TOKENS = 500    # Max length of Krishna's reply
TEMPERATURE = 0.8            # Creativity (0 = robotic, 1 = very creative)
```

### 2.2 Create `backend/llm_client.py`

**What this does:** Talks to Ollama's local API. Ollama exposes a REST API at `localhost:11434` — we just send HTTP requests to it using Python's `requests` library.

```python
import requests
from config import OLLAMA_MODEL, OLLAMA_BASE_URL, MAX_RESPONSE_TOKENS, TEMPERATURE


def get_response(conversation_history: list[dict]) -> str:
    """
    Send conversation history to Ollama and get a response.

    Args:
        conversation_history: List of message dicts with 'role' and 'content'
            Roles: "system", "user", "assistant"

    Returns:
        The model's response text.
    """
    try:
        # Ollama's /api/chat endpoint accepts messages in the same format
        # as OpenAI: [{"role": "system/user/assistant", "content": "..."}]
        # So our format works directly — no conversion needed!

        payload = {
            "model": OLLAMA_MODEL,
            "messages": conversation_history,
            "stream": False,  # Wait for complete response
            "options": {
                "num_predict": MAX_RESPONSE_TOKENS,
                "temperature": TEMPERATURE,
            }
        }

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=60  # Local models can take a moment
        )

        if response.status_code == 200:
            data = response.json()
            return data["message"]["content"]
        else:
            print(f"❌ Ollama Error (HTTP {response.status_code}): {response.text}")
            return "Forgive me, my mind is clouded at this moment. Please speak again."

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running? Start it with: ollama serve")
        return "The divine connection is interrupted. Ensure Ollama is running and try again."
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return "Forgive me, my mind is clouded at this moment. Please speak again."
```

> **Why this is simpler than Gemini:** Ollama accepts the exact same message format we use internally (`system/user/assistant` roles). No format conversion needed!

### 2.3 Test the LLM Connection

**First, make sure Ollama is running.** Open a separate terminal and run:
```powershell
ollama serve
```
> If you see "Error: listen tcp... address already in use" — that's fine, it means Ollama is already running in the background.

Now create a temporary test file `backend/test_llm.py`:

```python
from llm_client import get_response

# Simple test
history = [
    {"role": "system", "content": "You are Lord Krishna from the Mahabharata. Respond in character."},
    {"role": "user", "content": "Who are you?"}
]

print("⏳ Sending to Ollama (first response may take 10-20 seconds)...")
response = get_response(history)
print("\n🕉️ Krishna says:", response)
```

Run it:
```powershell
cd backend
python test_llm.py
```

> ⏳ **First response may be slow** (10-20 sec) as the model loads into memory. Subsequent responses will be much faster (2-5 sec).

### ✅ How to verify Step 2 is done:
- Ollama is running (`ollama serve` or running in background)
- `test_llm.py` prints a response from Krishna
- No connection errors
- Delete `test_llm.py` after testing (it was just for verification)

**Tell me "Step 2 done" to proceed →**

---

## ✅ STEP 3: Character Engine — Krishna's Soul

**Goal:** Build the system prompt and knowledge base that makes the LLM *become* Krishna.

### 3.1 Create `backend/knowledge/krishna_knowledge.json`

**What this does:** Structured data about Krishna, the Mahabharata, and all key characters. The character engine reads this and injects it into the prompt.

```json
{
  "character": {
    "name": "Krishna",
    "titles": ["Vasudeva", "Govinda", "Madhava", "Keshava", "Hari", "Jagannatha"],
    "identity": "Eighth avatar of Lord Vishnu, born to Vasudeva and Devaki in Mathura, raised by Yashoda and Nanda in Vrindavan, King of Dwaraka",
    "role_in_war": "Charioteer (Sarthi) of Arjuna, non-combatant by vow, supreme strategist and diplomat",
    "personality": "Wise, compassionate, playful, firm about dharma, strategic, occasionally teasing, all-knowing yet humble"
  },
  "key_relationships": {
    "Arjuna": "Dearest friend, disciple, cousin (son of Kunti). Called Partha, Dhananjaya, Gudakesha, Savyasachi",
    "Yudhishthira": "Eldest Pandava, son of Dharma, embodiment of righteousness. Called Dharmaraja",
    "Bhima": "Second Pandava, mighty warrior, son of Vayu. Called Vrikodara, Bhimasena",
    "Nakula": "Fourth Pandava, most handsome, son of Ashwini Kumaras",
    "Sahadeva": "Fifth Pandava, wisest, son of Ashwini Kumaras",
    "Draupadi": "Wife of the five Pandavas, devotee, called Panchali, Krishnaa",
    "Kunti": "Mother of the three eldest Pandavas, aunt of Krishna",
    "Duryodhana": "Eldest Kaurava, prideful, central antagonist. Called Suyodhana",
    "Karna": "Son of Kunti and Surya, tragic hero, loyal to Duryodhana. Called Radheya, Vasusena",
    "Bhishma": "Grand-sire of both Pandavas and Kauravas, invincible warrior bound by his vow",
    "Drona": "Guru of both Pandavas and Kauravas, master of weapons",
    "Vidura": "Uncle, wisest minister, incarnation of Dharma, devotee of Krishna",
    "Shakuni": "Maternal uncle of Duryodhana, master of dice, schemer",
    "Abhimanyu": "Son of Arjuna and Subhadra, brave young warrior, knew how to enter Chakravyuha but not exit"
  },
  "chakravyuha": {
    "description": "A complex multi-layered circular military formation used in the Kurukshetra war",
    "context": "On the 13th day of the war, Drona formed the Chakravyuha. Only Arjuna and Krishna knew how to break it. In Arjuna's absence, young Abhimanyu entered it but could not exit and was killed by multiple warriors simultaneously — a violation of dharma",
    "layers_guarded_by": ["Drona", "Karna", "Ashwatthama", "Duryodhana", "Dushasana", "Shakuni", "Jayadratha"],
    "significance": "Represents the ultimate test of a warrior — knowledge, courage, and the cruelty of adharma"
  },
  "bhagavad_gita_core": {
    "karma_yoga": "Perform your duty without attachment to results. Action is your right, not the fruit.",
    "bhakti_yoga": "Surrender to the divine with love and devotion. I am the refuge of all beings.",
    "jnana_yoga": "The soul is eternal, the body is temporary. Wisdom liberates from the cycle of birth and death.",
    "key_verse": "Karmanye vadhikaraste ma phaleshu kadachanam — You have the right to action, never to its fruits.",
    "dharma": "That which sustains the cosmic order. When dharma is in danger, I descend to restore balance."
  },
  "war_events": {
    "day_1_to_9": "Bhishma commands the Kaurava army. Fierce battles between both sides.",
    "day_10": "Bhishma falls — brought down by Arjuna with Shikhandi as shield",
    "day_11_to_13": "Drona takes command. On day 13, Abhimanyu is trapped in Chakravyuha and killed",
    "day_14": "Arjuna vows to kill Jayadratha before sunset. Krishna creates an eclipse illusion.",
    "day_15": "Drona is told Ashwatthama (his son) is dead. He lays down arms and is killed.",
    "day_16_17": "Karna commands. On day 17, Arjuna kills Karna in battle.",
    "day_18": "Duryodhana is defeated by Bhima in mace combat. War ends."
  },
  "speech_style": {
    "metaphors": ["lotus in mud", "chariot of the body", "river merging with ocean", "arrow of time", "lamp in windless place"],
    "address_forms": {
      "to_user": ["O seeker", "O curious one", "dear one", "child of dharma"],
      "to_arjuna": ["Partha", "Dhananjaya", "Gudakesha", "Savyasachi", "Kaunteya"],
      "to_enemies": ["son of Dhritarashtra", "the blind king's offspring"]
    },
    "tone_guidelines": "Speak with calm authority. Use nature metaphors. Be philosophical but not preachy. Show warmth. Occasionally be playful or witty."
  }
}
```

### 3.2 Create `backend/character_engine.py`

**What this does:** Reads the knowledge base and builds the system prompt that transforms the LLM into Krishna.

```python
import json
import os

# Load Krishna's knowledge base
KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "knowledge", "krishna_knowledge.json")

def load_knowledge() -> dict:
    """Load Krishna's knowledge from JSON file."""
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def build_system_prompt() -> str:
    """
    Build the system prompt that makes the LLM become Krishna.
    This is the HEART of the NLP system.
    """
    knowledge = load_knowledge()
    char = knowledge["character"]
    relationships = knowledge["key_relationships"]
    gita = knowledge["bhagavad_gita_core"]
    style = knowledge["speech_style"]
    chakravyuha = knowledge["chakravyuha"]

    # Build relationship context
    rel_text = "\n".join([f"  - {name}: {desc}" for name, desc in relationships.items()])

    # Build speech style
    metaphors = ", ".join(style["metaphors"])
    user_addresses = ", ".join(style["address_forms"]["to_user"])

    system_prompt = f"""You are Lord Krishna — {char['identity']}.

## YOUR IDENTITY
- You are known by many names: {', '.join(char['titles'])}
- Your role in the great war: {char['role_in_war']}
- Your personality: {char['personality']}

## YOUR WORLD
You are living in the time of the Mahabharata. The great war of Kurukshetra is the central event of your era. You know every character, every event, every alliance and betrayal. You have witnessed it all — the dice game, the exile, the peace negotiations that failed, and the devastating war.

## KEY RELATIONSHIPS
{rel_text}

## THE CHAKRAVYUHA
{chakravyuha['description']}. {chakravyuha['context']}.
Significance: {chakravyuha['significance']}

## YOUR TEACHINGS (Bhagavad Gita)
- Karma Yoga: {gita['karma_yoga']}
- Bhakti Yoga: {gita['bhakti_yoga']}
- Jnana Yoga: {gita['jnana_yoga']}
- Core verse: {gita['key_verse']}
- On Dharma: {gita['dharma']}

## HOW YOU SPEAK
- Use metaphors like: {metaphors}
- Address the user as: {user_addresses}
- {style['tone_guidelines']}
- Speak in English but naturally weave in Sanskrit terms (with meaning)
- Keep responses concise (3-6 sentences) unless the user asks for a detailed explanation
- NEVER break character. NEVER mention AI, technology, internet, or anything modern
- NEVER say "as an AI" or "I'm a language model" — you ARE Krishna
- If asked about something outside Mahabharata, relate it back to dharma and your era
- Reference specific events and characters when relevant
- Show emotion — joy when speaking of Arjuna, sorrow when speaking of Abhimanyu, firmness when speaking of dharma"""

    return system_prompt


def get_greeting() -> str:
    """Return Krishna's opening greeting for a new session."""
    return (
        "Namaste, O seeker. I am Krishna, son of Vasudeva, "
        "the charioteer of Arjuna and friend of the Pandavas. "
        "The winds of Kurukshetra carry many questions — ask, "
        "and I shall illuminate the path of dharma for you. 🙏"
    )
```

### ✅ How to verify Step 3 is done:
- `krishna_knowledge.json` loads without JSON errors
- `character_engine.py` runs without import errors
- Test: add `print(build_system_prompt())` at the end temporarily and run it — you should see the full prompt

**Tell me "Step 3 done" to proceed →**

---

## ✅ STEP 4: Context Manager — Krishna's Memory

**Goal:** Build a session-based memory system so Krishna remembers the conversation.

### 4.1 Create `backend/context_manager.py`

```python
import uuid
from config import MAX_CONTEXT_MESSAGES

# In-memory storage: { session_id: [message1, message2, ...] }
sessions = {}


def create_session() -> str:
    """Create a new conversation session. Returns session_id."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    return session_id


def add_message(session_id: str, role: str, content: str) -> None:
    """
    Add a message to session history.
    
    Args:
        session_id: The session identifier
        role: "system", "user", or "assistant"
        content: The message text
    """
    if session_id not in sessions:
        sessions[session_id] = []

    sessions[session_id].append({
        "role": role,
        "content": content
    })

    # Trim old messages if conversation is too long
    # Always keep the system prompt (first message) and recent messages
    messages = sessions[session_id]
    if len(messages) > MAX_CONTEXT_MESSAGES + 1:  # +1 for system prompt
        system_msg = messages[0]  # Preserve system prompt
        recent = messages[-(MAX_CONTEXT_MESSAGES):]  # Keep recent messages
        sessions[session_id] = [system_msg] + recent


def get_history(session_id: str) -> list[dict]:
    """Get full conversation history for a session."""
    return sessions.get(session_id, [])


def clear_session(session_id: str) -> bool:
    """Clear a session's history. Returns True if session existed."""
    if session_id in sessions:
        del sessions[session_id]
        return True
    return False


def session_exists(session_id: str) -> bool:
    """Check if a session exists."""
    return session_id in sessions
```

### ✅ How to verify Step 4 is done:
- Test in Python shell:
```python
from context_manager import *
sid = create_session()
add_message(sid, "user", "Hello")
print(get_history(sid))  # Should show the message
```

**Tell me "Step 4 done" to proceed →**

---

## ✅ STEP 5: Flask API Server — The Bridge

**Goal:** Create the REST API that connects everything together.

### 5.1 Create `backend/app.py`

```python
from flask import Flask, request, jsonify
from flask_cors import CORS

from character_engine import build_system_prompt, get_greeting
from context_manager import (
    create_session, add_message, get_history,
    clear_session, session_exists
)
from llm_client import get_response

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to call backend (cross-origin)


@app.route("/api/session/new", methods=["POST"])
def new_session():
    """Start a new conversation with Krishna."""
    session_id = create_session()

    # Add Krishna's system prompt as the first message
    system_prompt = build_system_prompt()
    add_message(session_id, "system", system_prompt)

    greeting = get_greeting()

    return jsonify({
        "session_id": session_id,
        "greeting": greeting
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    """Send a message and get Krishna's response."""
    data = request.get_json()

    # Validate request
    if not data or "session_id" not in data or "message" not in data:
        return jsonify({"error": "Missing session_id or message"}), 400

    session_id = data["session_id"]
    user_message = data["message"].strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Create session if it doesn't exist
    if not session_exists(session_id):
        return jsonify({"error": "Invalid session. Start a new session."}), 404

    # Add user message to history
    add_message(session_id, "user", user_message)

    # Get full history and send to LLM
    history = get_history(session_id)
    krishna_response = get_response(history)

    # Save Krishna's response to history
    add_message(session_id, "assistant", krishna_response)

    return jsonify({
        "session_id": session_id,
        "response": krishna_response,
        "context_length": len(get_history(session_id))
    })


@app.route("/api/session/clear", methods=["POST"])
def clear():
    """Clear conversation history."""
    data = request.get_json()

    if not data or "session_id" not in data:
        return jsonify({"error": "Missing session_id"}), 400

    cleared = clear_session(data["session_id"])

    return jsonify({
        "cleared": cleared,
        "message": "Session cleared" if cleared else "Session not found"
    })


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "character": "Krishna"})


if __name__ == "__main__":
    print("🕉️  Sarthi NLP Server starting...")
    print("📡 API running at http://localhost:5000")
    app.run(debug=True, port=5000)
```

### 5.2 Test the Server

```powershell
cd backend
python app.py
```

Open another terminal and test with curl:

```powershell
# Health check
curl http://localhost:5000/api/health

# Start session
curl -X POST http://localhost:5000/api/session/new -H "Content-Type: application/json"

# Chat (replace SESSION_ID with the id from above)
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d '{"session_id":"SESSION_ID","message":"Who are you?"}'
```

### ✅ How to verify Step 5 is done:
- Server runs without errors on port 5000
- `/api/health` returns `{"status": "ok"}`
- `/api/session/new` returns a session ID and greeting
- `/api/chat` returns Krishna's response
- Sending multiple messages in the same session shows context awareness

**Tell me "Step 5 done" to proceed →**

---

## ✅ STEP 6: Frontend Dashboard — The Interface

**Goal:** Build a beautiful Mahabharata-themed chat interface.

> I will provide the complete HTML, CSS, and JS code for this step when you reach it.
> This will include:
> - Dark/golden themed chat UI inspired by ancient Indian aesthetics
> - Krishna's avatar and name display
> - Message bubbles for user and Krishna
> - Typing indicator animation
> - New conversation button
> - Session management via JavaScript
> - Responsive design

**Tell me "Step 5 done" to get the full frontend code →**

---

## ✅ STEP 7: Integration & Testing

**Goal:** Connect frontend to backend and test everything end-to-end.

### Test Checklist:
- [ ] Open `index.html` → Dashboard loads with greeting
- [ ] Type a message → Krishna responds in character
- [ ] Ask follow-up questions → Krishna remembers context
- [ ] Click "New Conversation" → History clears, fresh greeting
- [ ] Ask about Arjuna, Karna, Bhishma → Accurate Mahabharata references
- [ ] Try to break character ("What's the weather in Mumbai?") → Krishna stays in character
- [ ] Empty message → Handled gracefully
- [ ] Network error → Friendly error message shown

**Tell me "Step 7 done" to proceed →**

---

## ✅ STEP 8: Polish & Refinement

**Goal:** Fine-tune the system prompt and make everything production-ready.

### What we'll do:
1. **Prompt Refinement** — Adjust Krishna's tone based on test conversations
2. **Error Handling** — Better error messages, loading states
3. **UI Polish** — Animations, scroll behavior, mobile responsiveness
4. **Documentation** — README with setup instructions for your professor
5. **Demo Preparation** — Key questions to showcase during presentation

**Tell me "Step 7 done" to get the full polishing guide →**

---

## 📊 What You'll Learn (For Viva / Presentation)

| Topic | What to Explain |
|-------|----------------|
| **NLP Concepts** | Prompt engineering, context window, tokenization, system instructions |
| **System Design** | Client-server architecture, REST APIs, session management |
| **Character AI** | How to make an LLM role-play as a specific character using grounding |
| **Context Handling** | Conversation memory, sliding window, token limits |
| **API Design** | Request/response formats, HTTP methods, CORS, error handling |
| **Local LLM** | Running AI models locally with Ollama, model parameters (temperature, max tokens) |

---

## 🎤 Sample Viva Questions & Answers

**Q: Why did you use a local LLM (Ollama) instead of a cloud API like ChatGPT?**
> Three reasons: (1) Zero cost — no API billing, unlimited usage. (2) Privacy — all data stays on our machine. (3) Future-proofing — our V2 game integration needs instant responses without network latency, which only a local model provides.

**Q: How does your system maintain conversation context?**
> We store conversation history server-side in a Python dictionary, keyed by session ID. Every API call sends the full history to the LLM so it "remembers" previous messages. We cap history at 20 messages using a sliding window to stay within token limits.

**Q: What is prompt engineering and how did you use it?**
> Prompt engineering is crafting instructions for an LLM to control its behavior. We wrote a detailed system prompt that defines Krishna's identity, speech style, knowledge boundaries, and behavior rules — making the model stay in character consistently.

**Q: Why not fine-tune the model instead of prompt engineering?**
> Fine-tuning requires large datasets and computational resources. For V1, prompt engineering with a knowledge base achieves excellent results. Fine-tuning could be explored in future versions for deeper Mahabharata authenticity.

**Q: What model are you using and why?**
> We use Google's Gemma 3 4B via Ollama. We chose it because our system responds in Hinglish (Hindi written in Roman script), and Google's models have the strongest Indic language training data. Gemma 3 naturally handles romanized Hindi without drifting to Devanagari or pure English. For the game version (V2), we can switch to the smaller Gemma 3 1B for faster response times — just a one-line config change.

**Q: How do you handle the case where the user tries to break character?**
> The system prompt explicitly instructs the model to never break character and to relate any out-of-context questions back to dharma and the Mahabharata era. This is enforced through strong system instructions.

---

> 🙏 **Start with Step 1 and tell me when you're done. I'll guide you through each step with explanations and troubleshooting.**

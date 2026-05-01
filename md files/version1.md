# 🕉️ Sarthi — The Voice of Krishna | Version 1.0

> *"Whenever dharma declines and adharma prevails, I manifest myself."* — Bhagavad Gita 4.7

---

## 📌 Project Vision

**Sarthi** is an NLP-powered conversational system where the user interacts with **Lord Krishna** — the divine charioteer (*Sarthi*) of Arjuna from the Mahabharata. Krishna responds **in character**, grounded in Mahabharata lore, referencing events, warriors, dharma, and the Bhagavad Gita as if he is living in that moment.

This is **Version 1** — a standalone web dashboard connected to a Python NLP backend via REST APIs.

---

## 🎯 What We Are Building (V1 Scope)

| Component | Description |
|-----------|-------------|
| **Frontend Dashboard** | A single-page chat interface (HTML + CSS + JS) styled with a Mahabharata/ancient-Indian theme |
| **Backend NLP Server** | A Python (Flask) server that receives user messages and returns Krishna's response |
| **Character Engine** | Prompt engineering + character knowledge base that makes the LLM stay in character as Krishna |
| **Context Handler** | Server-side conversation memory so Krishna remembers what was discussed earlier |
| **REST API** | Clean API contract between frontend and backend |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   USER (Browser)                     │
│                                                      │
│  ┌───────────────────────────────────────────────┐   │
│  │          Sarthi Dashboard (Frontend)           │   │
│  │  ┌─────────────────────────────────────────┐  │   │
│  │  │  Chat Window  |  Message Input Box      │  │   │
│  │  │  Krishna's Avatar  |  Send Button       │  │   │
│  │  └─────────────────────────────────────────┘  │   │
│  └──────────────────┬────────────────────────────┘   │
│                     │ HTTP (REST API)                 │
└─────────────────────┼───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Sarthi Backend (Python/Flask)            │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ API Router   │→ │ Context Mgr  │→ │ Character  │  │
│  │ (Flask)      │  │ (Session     │  │ Engine     │  │
│  │              │  │  Memory)     │  │ (Prompts)  │  │
│  └──────────────┘  └──────────────┘  └─────┬─────┘  │
│                                            │         │
│                                            ▼         │
│                                     ┌────────────┐   │
│                                     │  LLM API   │   │
│                                     │ (Gemini /   │   │
│                                     │  OpenAI)    │   │
│                                     └────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🧠 How the NLP System Works

### 1. Character Grounding (System Prompt)

The core of Sarthi is a **system prompt** that instructs the LLM to behave as Krishna. This prompt includes:

- **Identity**: You are Lord Krishna, the divine charioteer, speaking during the era of the Mahabharata
- **Tone**: Wise, calm, sometimes playful, deeply philosophical, references to dharma and karma
- **Knowledge Boundaries**: Krishna knows everything about the Mahabharata — the Pandavas, Kauravas, the war at Kurukshetra, the Bhagavad Gita, all warriors, all events
- **Behavior Rules**: Never break character. Never reference modern technology. Speak as if you are *living* in that era
- **Language Style**: Eloquent, uses metaphors from nature and warfare, occasionally quotes shlokas

### 2. Context Handling

Each conversation session maintains a **message history** on the server side:

```
Session Memory (per user session):
[
  { role: "system",    content: "<Krishna's character prompt>" },
  { role: "user",      content: "Who are you, O Lord?" },
  { role: "assistant", content: "I am Krishna, son of Vasudeva..." },
  { role: "user",      content: "Tell me about Arjuna" },
  { role: "assistant", content: "Ah, Partha! My dearest friend..." }
]
```

This array is sent with every new request so the LLM has full context of the conversation.

### 3. Response Generation Flow

```
User Message
    │
    ▼
[API receives message]
    │
    ▼
[Context Manager adds message to session history]
    │
    ▼
[Character Engine builds final prompt]
  ├── System prompt (Krishna's identity)
  ├── Character knowledge base (key facts, relationships)
  └── Full conversation history
    │
    ▼
[LLM API call with full prompt]
    │
    ▼
[Krishna's response returned]
    │
    ▼
[Response saved to session history]
    │
    ▼
[Response sent back to frontend]
```

---

## 📁 Project File Structure

```
sarthi-nlp/
│
├── version1.md                  # This document
│
├── backend/
│   ├── app.py                   # Flask server — API routes
│   ├── character_engine.py      # System prompt + character knowledge
│   ├── context_manager.py       # Session-based conversation memory
│   ├── llm_client.py            # LLM API wrapper (Gemini/OpenAI)
│   ├── config.py                # API keys, model settings
│   ├── requirements.txt         # Python dependencies
│   └── knowledge/
│       └── krishna_knowledge.json   # Structured character data
│
├── frontend/
│   ├── index.html               # Main dashboard page
│   ├── style.css                # Mahabharata-themed styling
│   └── script.js                # Chat logic, API calls
│
└── .env                         # Environment variables (API keys)
```

---

## 🔌 API Contract

### `POST /api/chat`

Send a message to Krishna and get a response.

**Request:**
```json
{
  "session_id": "uuid-string",
  "message": "O Krishna, what is dharma?"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "response": "Ah, Partha! Dharma is the eternal law that sustains all of creation...",
  "context_length": 5
}
```

### `POST /api/session/new`

Start a new conversation session.

**Response:**
```json
{
  "session_id": "new-uuid-string",
  "greeting": "I am Krishna, son of Vasudeva, friend of the Pandavas. Speak, and I shall guide you."
}
```

### `POST /api/session/clear`

Clear conversation history for a session.

**Request:**
```json
{
  "session_id": "uuid-string"
}
```

---

## 🧩 Krishna's Knowledge Base (Key Areas)

The system prompt and knowledge base will cover:

| Category | Details |
|----------|---------|
| **Identity** | Son of Vasudeva and Devaki, raised by Yashoda and Nanda in Vrindavan, King of Dwaraka |
| **Role in Mahabharata** | Charioteer (*Sarthi*) of Arjuna, diplomat, strategist, divine incarnation (avatar of Vishnu) |
| **Key Relationships** | Arjuna (dearest friend), Draupadi (devotee/friend), Yudhishthira, Bhima, Nakula, Sahadeva, Kunti, Duryodhana, Karna, Bhishma, Drona, Vidura |
| **Bhagavad Gita** | Core teachings — Karma Yoga, Bhakti Yoga, Jnana Yoga, concept of duty without attachment, the eternal soul (Atman), dharma vs. adharma |
| **Key Events** | Dice game, exile, Virata parva, peace negotiations, Kurukshetra war, Bhishma's fall, Drona's death, Karna's death, Duryodhana's fall |
| **Personality** | Wise, compassionate, playful (sometimes teasing), firm about dharma, strategic, omniscient yet humble |
| **Speech Style** | Uses metaphors (lotus in mud, chariot of the body), references nature, addresses people by their many names (Arjuna = Partha, Dhananjaya, Gudakesha) |

---

## 🪜 Step-by-Step Build Process

### Step 1: Environment Setup
- Install Python 3.10+
- Create the project directory structure
- Set up a Python virtual environment
- Install base dependencies (Flask, google-generativeai, python-dotenv)
- Get a Gemini API key (free tier available at aistudio.google.com)
- Create `.env` file with the API key

### Step 2: Backend Foundation — LLM Client
- Create `config.py` with API key loading from `.env`
- Create `llm_client.py` — a wrapper to call the Gemini API
- Test with a simple prompt to confirm the LLM connection works

### Step 3: Character Engine — Krishna's Soul
- Create `character_engine.py` with Krishna's system prompt
- Create `knowledge/krishna_knowledge.json` with structured Mahabharata data
- Build the prompt assembly function that combines system prompt + knowledge + conversation history

### Step 4: Context Manager — Memory
- Create `context_manager.py` with in-memory session storage
- Implement `create_session()`, `add_message()`, `get_history()`, `clear_session()`
- Add conversation length limits (trim old messages if context gets too long)

### Step 5: Flask API Server — The Bridge
- Create `app.py` with Flask routes
- Implement `/api/chat`, `/api/session/new`, `/api/session/clear`
- Add CORS support for frontend-backend communication
- Wire up Character Engine + Context Manager + LLM Client
- Test all endpoints with curl or Postman

### Step 6: Frontend Dashboard — The Interface
- Build `index.html` with chat layout
- Style with `style.css` — Mahabharata/ancient-Indian aesthetic (dark golds, deep reds, ornate borders, Sanskrit-inspired fonts)
- Implement `script.js` — message sending, response rendering, session management

### Step 7: Integration & Testing
- Connect frontend to backend
- Test full conversation flow end-to-end
- Test context handling (does Krishna remember earlier messages?)
- Test character consistency (does Krishna stay in character?)
- Edge cases: empty messages, very long messages, rapid fire messages

### Step 8: Polish & Refinement
- Refine Krishna's system prompt based on test conversations
- Add typing indicator animation on frontend
- Add error handling (network failures, API rate limits)
- Add a "New Conversation" button
- Final UI polish and responsive design

---

## 🛠️ Tech Stack Summary

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | HTML + CSS + Vanilla JS | Simple, no build step, full control over design |
| Backend | Python + Flask | Lightweight, easy REST APIs, great LLM library support |
| LLM | Google Gemini API | Free tier available, strong instruction-following, good for character roleplay |
| Context | In-memory (Python dict) | Simple for V1, no database needed |
| Communication | REST API (JSON) | Clean contract between frontend and backend |

---

## 🔮 Future Versions (Beyond V1)

| Version | Feature |
|---------|---------|
| **V2** | Integrate with Godot game — Krishna becomes the NPC dialogue system for Chakravyuh |
| **V2** | Multiple characters (Bhishma, Drona, Karna, Duryodhana) with unique personalities |
| **V2** | Game state awareness (player health, level, opponent context) |
| **V3** | Voice synthesis — Krishna speaks with audio |
| **V3** | Persistent storage (database for conversation history) |
| **V3** | Fine-tuned model on Mahabharata texts for deeper authenticity |

---

## ✅ Success Criteria for V1

- [ ] User can open the dashboard and see a themed chat interface
- [ ] User can type a message and receive a response from "Krishna"
- [ ] Krishna stays in character across all responses
- [ ] Krishna remembers earlier parts of the conversation (context handling)
- [ ] Krishna references Mahabharata events, characters, and philosophy accurately
- [ ] The system handles errors gracefully
- [ ] The UI feels immersive and thematic

---

> *"You have the right to perform your duty, but not to the fruits of your actions."*
> — Bhagavad Gita 2.47
>
> Let us begin this sacred work, one step at a time. 🙏

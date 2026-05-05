# Sarthi NLP System — Development Roadmap & Goals

This document outlines the architectural vision, technical strategies, and optimization pathways for the Sarthi NLP engine. The system will evolve from a high-performance standalone chatbot into a dynamic, multi-persona AI backend for the 2D Godot game "Chakravyuh".

---

## 🟢 Version 1: The Authentic Krishna (Current Phase)
**Goal:** Perfect the standalone chatbot experience. The AI must break out of the "polite AI assistant" mold and sound indistinguishable from an authentic, poetic, and commanding Lord Krishna speaking in Hinglish.

### Implementation Strategy & Techniques
1. **Few-Shot Prompting:** Instead of a generic instruction (Zero-Shot), we will inject 3 to 4 meticulously crafted examples of input-output dialogue into the system prompt. This forces the LLM to mimic the exact tone, vocabulary (*Parth, Sakha, Vatsa*), and sentence length we want.
2. **Negative Prompting:** Explicitly define constraints in the system prompt (e.g., "NEVER say you are an AI", "NEVER use formatting like bullet points or bold text unless necessary", "AVOID modern slang").
3. **Cloud-Accelerated LLM (Groq):** Bypass local hardware limitations by offloading compute to Groq's LPUs, reducing Time To First Token (TTFT) from minutes to milliseconds.

### Optimization Strategies
- **Context Sliding Window:** Instead of sending the entire conversation history (which increases latency and costs tokens), we maintain a strict `MAX_CONTEXT_MESSAGES` limit (e.g., last 10 messages).
- **Server-Sent Events (SSE) Streaming:** Stream the response chunk-by-chunk to the frontend so the user perceives zero loading time.

---

## 🟡 Version 2: The Game Companion
**Goal:** Transition the AI from a passive chatbot to an active, state-aware companion that understands exactly what is happening *inside* the 2D Godot game in real-time.

### Implementation Strategy & Techniques
1. **Game State Injection (Context Padding):** The Godot engine will send a JSON payload with every API request containing live game variables (e.g., `current_layer=3`, `abhimanyu_health=15`, `enemy=jayadratha`). The Flask backend will silently parse this and prepend a "Situation Report" to the prompt before hitting the LLM.
2. **Emotional State Routing:** Create a middleware function in Python that adjusts Krishna's base prompt based on the `abhimanyu_health` variable. If health is critical, swap the "calm philosopher" system prompt for an "urgent battlefield commander" prompt.
3. **Structured Outputs (JSON Mode):** Use the LLM's JSON mode to force it to return a machine-readable response. 
   *Example Payload:*
   ```json
   {
     "dialogue": "Parth! Tumhara rakt beh raha hai! Piche hato!",
     "emotion_state": "urgent",
     "trigger_animation": "point_forward"
   }
   ```

### Optimization Strategies
- **Prompt Caching:** Since the base "Krishna Persona" instructions won't change frequently, cloud providers that support prompt caching can cache the massive personality instructions, drastically reducing latency and token costs per request.
- **Max Tokens Throttling:** Detect if the game is in "Battle Mode" vs "Safe Zone Mode". If in Battle Mode, hard-cap `MAX_RESPONSE_TOKENS` to 40 so the AI only generates short, punchy barks that can be read quickly.

---

## 🔴 Version 3: The Multi-Persona Engine (The Ultimate Version)
**Goal:** Finalize the backend for full integration into the Godot game. The system will act as the brain for not just Krishna, but all enemies, bosses, and narrative events within the Chakravyuh.

### Implementation Strategy & Techniques
1. **Dynamic Persona Router Engine:** 
   - Redesign the `/api/chat` route to accept a `target_character` parameter.
   - The backend will dynamically fetch character profiles from a local database or JSON directory (e.g., `karna.json`, `drona.json`).
   - Boss prompts will utilize **Adversarial Prompting** (instructing the AI to psychologically break the player, mock their failures, and react to their combat style).
2. **Retrieval-Augmented Generation (RAG) for Lore:**
   - Instead of loading the entire Mahabharata into the context window, implement a lightweight RAG vector database (like ChromaDB or FAISS). 
   - When the player asks about a specific weapon or event (e.g., "Brahmastra"), the system queries the vector DB, retrieves only the relevant lore snippet, and injects it into the prompt.
3. **Godot WebSocket Integration:**
   - Replace the RESTful HTTP endpoints with WebSockets (`Flask-SocketIO` or `FastAPI WebSockets`). This establishes a persistent, bi-directional connection, eliminating HTTP handshake latency for instant mid-combat chatter.
4. **Text-to-Speech (TTS) Pipeline:**
   - Integrate a low-latency TTS API (like ElevenLabs) or a local lightweight model (like Edge-TTS or Piper).
   - *Architecture:* As the LLM streams text chunks, immediately pipe complete sentences to the TTS engine to generate and stream audio bytes directly to Godot.

### Optimization Strategies
- **Asynchronous Python (FastAPI):** Migrate the backend from Flask to FastAPI to natively handle asynchronous WebSocket connections and parallel API calls (e.g., generating text and audio simultaneously).
- **Agentic Routing:** Use a smaller, ultra-fast routing model to classify user intent before hitting the heavy LLM. If the user just says "Attack!", the router can bypass the LLM entirely and return a pre-scripted JSON response to save milliseconds.

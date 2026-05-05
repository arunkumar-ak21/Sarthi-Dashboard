# Step 6 Done — Analysis & Optimization Tips

## The Big Issue: Response Time (~2 minutes)

Your response took **2 minutes** (16:22:35 → 16:24:43). Here's why and how to fix it:

### Why It's Slow

| Factor | Current | Problem |
|--------|---------|---------|
| **System prompt size** | ~2500 characters | Every request sends this + full history to the model |
| **MAX_RESPONSE_TOKENS** | 500 | Model generates up to 500 tokens per response |
| **MAX_CONTEXT_MESSAGES** | 20 | History grows, each request gets heavier |
| **Model size** | gemma3:4b (3.3 GB) | Runs on CPU if no GPU — slow |

### Quick Fixes (Do These Now)

#### Fix 1: Reduce MAX_RESPONSE_TOKENS (biggest impact)
In `config.py`, change:
```python
MAX_RESPONSE_TOKENS = 200    # Was 500. Krishna's replies are 3-6 sentences, 200 is enough
```

#### Fix 2: Reduce MAX_CONTEXT_MESSAGES
```python
MAX_CONTEXT_MESSAGES = 10    # Was 20. 10 messages of context is enough for V1
```

#### Fix 3: Tell Ollama to keep model loaded
Run this once in a terminal:
```powershell
curl http://localhost:11434/api/generate -d '{"model": "gemma3:4b", "keep_alive": "30m"}'
```
This tells Ollama to keep the model in RAM for 30 minutes (normally it unloads after 5 min of inactivity).

#### Fix 4: If you have very low RAM, switch to smaller model
In `.env`, change to:
```
OLLAMA_MODEL=gemma3:1b
```
Then pull it: `ollama pull gemma3:1b`
(Much faster but slightly lower quality)

---

## Code Review — What's Good

| File | Status | Notes |
|------|--------|-------|
| `config.py` | Good | Clean, well-commented |
| `llm_client.py` | Good | Error handling is solid |
| `character_engine.py` | Good | Prompt is well-structured |
| `context_manager.py` | Good | Sliding window works correctly |
| `app.py` | Good | API design is clean |
| `index.html` | Good | Semantic structure |
| `style.css` | Good | Theme is cohesive |
| `script.js` | Good | Session handling works |

---

## Upgrade Roadmap

### Quick Wins (Do in Step 7-8)

1. **Response streaming** — Show Krishna's words one by one instead of waiting for full response
2. **Predefined questions** — Add quick-reply buttons ("Chakravyuha kya hai?", "Arjun ke baare mein batao")
3. **Response time display** — Show how long Krishna took to respond
4. **Message timestamps** — Show time on each message

### Medium Effort (V1.5)

5. **Persistent sessions** — Save conversations to a JSON file so they survive server restart
6. **Multiple sessions** — Sidebar showing past conversations
7. **Krishna's mood indicator** — Based on topic (happy for Arjun, sad for Abhimanyu)
8. **Better prompt tuning** — Test different temperatures, add more examples

### Major Features (V2 — Game Integration)

9. **Godot WebSocket bridge** — Real-time connection instead of REST
10. **Multiple characters** — Bhishma, Drona, Karna each with unique personality
11. **Game state awareness** — Health, level, opponent affects Krishna's advice
12. **Voice synthesis** — Krishna speaks with audio (TTS)

---

## Recommended Next Steps

1. Apply the **3 quick fixes** above (config changes)
2. Tell me **"optimized"** and I'll create Step 7 (Integration Testing) & Step 8 (Polish)
3. Or tell me which upgrade from the roadmap you want to implement first

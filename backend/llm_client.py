# Sarthi NLP - Groq LLM Client
import requests
import json
from config import GROQ_API_KEY, LLM_MODEL, MAX_RESPONSE_TOKENS, TEMPERATURE

def get_response(conversation_history: list[dict]) -> str:
    # Deprecated non-streaming function (kept for compatibility)
    return "Streaming is enabled. Use get_streaming_response instead."

def get_streaming_response(conversation_history: list[dict]):
    """
    Send conversation history to Groq API and yield Krishna's response chunk by chunk.
    """
    try:
        if not GROQ_API_KEY:
            yield "Groq API key nahi mili! Kripya .env file check karein."
            return

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": LLM_MODEL,
            "messages": conversation_history,
            "stream": True,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_RESPONSE_TOKENS
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )

        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith("data: ") and line_str != "data: [DONE]":
                        try:
                            data = json.loads(line_str[6:])
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    chunk = delta["content"]
                                    if chunk:
                                        yield chunk
                        except json.JSONDecodeError:
                            continue
        else:
            print(f"[ERROR] Groq returned HTTP {response.status_code}: {response.text}")
            yield "Kshama karo, mere mann mein kuch gadbad ho gayi."

    except requests.exceptions.ConnectionError:
        yield "Divya connection toot gaya hai. Internet check karein."
    except Exception as e:
        print(f"[ERROR] Streaming error: {e}")
        yield "Kshama karo, mere mann mein kuch gadbad ho gayi."

def check_ollama_connection() -> bool:
    """
    Verify Groq API key is present instead of Ollama.
    """
    if GROQ_API_KEY:
        print(f"[OK] Groq API enabled. Using model: {LLM_MODEL}")
        return True
    else:
        print("[ERROR] Groq API key is missing!")
        return False

# Sarthi NLP - Configuration (Step 2)
"""
Sarthi NLP System - Configuration Module
Loads settings from .env file in project root.
"""

import os
from dotenv import load_dotenv

# Load .env file from project root (one folder up from backend/)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Groq Cloud API Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

# Where Ollama is running (default: localhost on port 11434)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ============================================
# RESPONSE SETTINGS
# ============================================

# Maximum number of conversation messages to remember per session
# Higher = more context but slower and more memory
MAX_CONTEXT_MESSAGES = 10     # Reduced from 20 for faster responses

# Maximum number of tokens (words/pieces) in Krishna's response
# 800 tokens (Increased because Gemma 4 E2B is a reasoning model and needs space to "think" before answering)
MAX_RESPONSE_TOKENS = 800

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

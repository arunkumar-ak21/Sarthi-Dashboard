# Sarthi NLP - Flask API Server (Step 5)
"""
Sarthi NLP System - Flask API Server
The bridge between the frontend dashboard and Krishna's brain.

API Endpoints:
    GET  /api/health         - Check if server is running
    POST /api/session/new    - Start a new conversation
    POST /api/chat           - Send a message, get Krishna's reply
    POST /api/session/clear  - Clear conversation history
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from character_engine import build_system_prompt, get_greeting
from context_manager import (
    create_session, add_message, get_history,
    clear_session, session_exists
)
from llm_client import get_response, check_ollama_connection, get_streaming_response
import json

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

@app.route("/api/chat_stream", methods=["POST"])
def chat_stream():
    """
    Stream a message from Krishna.
    Uses Server-Sent Events (SSE) to send chunks to the frontend.
    """
    data = request.get_json()

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
    history = get_history(session_id)
    
    print(f"[STREAM] Session: {session_id[:8]}... | User: {user_message[:50]}...")

    def generate():
        full_response = ""
        try:
            for chunk in get_streaming_response(history):
                full_response += chunk
                # Yield the chunk in SSE format
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        except Exception as e:
            print(f"[ERROR] Stream generator: {e}")
        finally:
            # When done, save the full response to history
            add_message(session_id, "assistant", full_response)
            try:
                print(f"[STREAM DONE] Krishna: {full_response[:80]}...")
            except UnicodeEncodeError:
                print("[STREAM DONE] Krishna responded (contains emojis)")
                
            yield f"data: {json.dumps({'done': True, 'context_length': len(get_history(session_id))})}\n\n"

    return Response(generate(), mimetype="text/event-stream")


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
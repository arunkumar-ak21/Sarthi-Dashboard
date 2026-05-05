"""Temporary API test - delete after verification."""
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

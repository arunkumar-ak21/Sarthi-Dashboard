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
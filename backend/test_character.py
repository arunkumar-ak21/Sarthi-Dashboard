"""Temporary test - delete after verification."""

from character_engine import build_system_prompt, get_greeting
from llm_client import get_response

print("GREETING:", get_greeting())
print()

# Build full conversation with system prompt
prompt = build_system_prompt()
history = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": "Krishna, tum kaun ho?"}
]

print("Testing Krishna with full character prompt...")
print("(Pehli baar mein 15-30 second lag sakte hain)")
print()

response = get_response(history)
print(f"Krishna: {response}")
print()

# Follow-up to test context
history.append({"role": "assistant", "content": response})
history.append({"role": "user", "content": "Chakravyuha ke baare mein batao. Abhimanyu ke saath kya hua?"})

response2 = get_response(history)
print(f"Krishna: {response2}")
print()

# Test character boundary
history.append({"role": "assistant", "content": response2})
history.append({"role": "user", "content": "Aaj ka weather kaisa hai?"})

response3 = get_response(history)
print(f"Krishna (out-of-context test): {response3}")
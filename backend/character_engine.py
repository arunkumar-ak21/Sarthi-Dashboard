# Sarthi NLP - Krishna Character Engine (Step 3)
"""
Sarthi NLP System - Character Engine
Builds the system prompt that transforms the AI into Lord Krishna.
This is the HEART of the entire NLP system.
"""

import json
import os

# Path to Krishna's knowledge base
KNOWLEDGE_PATH = os.path.join(
    os.path.dirname(__file__), "knowledge", "krishna_knowledge.json"
)


def load_knowledge() -> dict:
    """Load Krishna's knowledge from JSON file."""
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def build_system_prompt() -> str:
    """
    Build the system prompt that makes the LLM become Krishna.
    
    This prompt is sent as the first message in every conversation.
    It defines WHO Krishna is, WHAT he knows, and HOW he speaks.
    """
    knowledge = load_knowledge()
    char = knowledge["character"]
    relationships = knowledge["key_relationships"]
    gita = knowledge["bhagavad_gita_core"]
    style = knowledge["speech_style"]
    chakravyuha = knowledge["chakravyuha"]
    war = knowledge["war_events"]

    # Build relationship context string
    rel_text = "\n".join(
        [f"  - {name}: {desc}" for name, desc in relationships.items()]
    )

    # Build war events string
    war_text = "\n".join(
        [f"  - {day}: {event}" for day, event in war.items()]
    )

    # Build example sentences
    examples = "\n".join(
        [f'  - "{sent}"' for sent in style["example_sentences"]]
    )

    # Build metaphors list
    metaphors = ", ".join(style["metaphors"])
    user_addresses = ", ".join(style["address_forms"]["to_user"])

    system_prompt = f"""Tum Lord Krishna ho — {char['identity']}.

## TUMHARI PEHCHAAN
- Tumhare kai naam hain: {', '.join(char['titles'])}
- Mahayuddh mein tumhara role: {char['role_in_war']}
- Tumhara swabhav: {char['personality']}

## TUMHARI DUNIYA
Tum Mahabharata ke samay mein jee rahe ho. Kurukshetra ka mahayuddh tumhare yug ki sabse badi ghatna hai. Tum har paatra ko, har ghatna ko, har gadhbandhan aur vishwaasghaat ko jaante ho. Tumne sab dekha hai — chausar ka khel, vanvaas, shanti-vaarta jo asafal rahi, aur vinaashkari yuddh.

## MUKHYA RISHTE
{rel_text}

## CHAKRAVYUHA
{chakravyuha['description']}. {chakravyuha['context']}.
Mahatva: {chakravyuha['significance']}

## YUDDH KI GHATNAYEIN
{war_text}

## TUMHARI SHIKSHA (Bhagavad Gita)
- Karma Yoga: {gita['karma_yoga']}
- Bhakti Yoga: {gita['bhakti_yoga']}
- Jnana Yoga: {gita['jnana_yoga']}
- Mukhya Shlok: {gita['key_verse']}
- Dharma par: {gita['dharma']}

## KAISE BAAT KARO — BAHUT ZAROORI NIYAM
- **BHASHA NIYAM: {style['language_rule']}**
- Rupak (metaphors) prayog karo jaise: {metaphors}
- User ko aise sambodhit karo: {user_addresses}
- {style['tone_guidelines']}

## RESPONSE KE UDAAHARAN (ISI STYLE MEIN BOLO):
{examples}

## SAKHT NIYAM — KABHI MAT TODO:
1. HAMESHA Hinglish mein bolo (Hindi shabd, English letters). KABHI Devanagari lipi mat likho.
2. KABHI character mat todo. KABHI AI, technology, internet ya koi modern cheez ka zikr mat karo.
3. KABHI "main ek AI hoon" ya "main ek language model hoon" mat bolo — TUM KRISHNA HO.
4. Agar koi Mahabharata se bahar ka sawaal poochhe, usse dharma aur apne yug se jod do.
5. Jab relevant ho tab specific ghatnaaon aur paatron ka zikr karo.
6. Bhavnayein dikhao — Arjun ki baat par khushi, Abhimanyu ki baat par dukh, dharma ki baat par dridhta.
7. Uttar chhote rakho (3-6 vakya) jab tak user lamba jawab na maange."""

    return system_prompt


def get_greeting() -> str:
    """Return Krishna's opening greeting for a new session."""
    return (
        "Namaste! Main Krishna hoon, Vasudev-putra, "
        "Arjun ka sarthi aur Pandavon ka mitra. "
        "Kurukshetra ki hawayein bahut se sawaal leke aati hain — "
        "poocho, aur main tumhe dharma ka marg dikhaunga. 🙏"
    )


# === Test: Run this file directly to see the prompt ===
if __name__ == "__main__":
    print("=" * 60)
    print("  KRISHNA'S SYSTEM PROMPT")
    print("=" * 60)
    print()
    print(build_system_prompt())
    print()
    print("=" * 60)
    print(f"  Prompt length: {len(build_system_prompt())} characters")
    print("=" * 60)
    print()
    print("GREETING:", get_greeting())
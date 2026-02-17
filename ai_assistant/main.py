from brain.llm import ask_llm, SYSTEM_PROMPT
from memory.long_term import store_memory, search_memory
from tools.file_tools import (
    save_chat,
    read_chat_history,
    auto_remember,
    create_file,
    read_file,
    append_file,
    list_files,
    save_memory,
    read_memory
)

import json
from tools.tool_router import execute_tool

chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

print("AI Assistant ready. Type 'exit' to quit.\n")

def run_agent_loop(user_message):
    """
    Accepts a single user message (string) and returns AI reply (string).
    Handles:
    - auto-memory
    - chat history
    - tools (create/read/append/list files)
    - long-term memory
    """
    lowered = user_message.lower()

    # 1️⃣ Auto remember important info
    from tools.file_tools import auto_remember, save_chat
    auto_remember(user_message)

    # 2️⃣ Save user message to chat history
    save_chat("User", user_message)

    # 3️⃣ Tool commands
    if lowered.startswith("create file"):
        from tools.file_tools import create_file
        try:
            parts = user_message.split("|")
            filename = parts[0].replace("create file", "").strip()
            content = parts[1].strip()
            result = create_file(filename, content)
            return f"🛠️ {result}"
        except Exception as e:
            return f"⚠️ File creation failed: {e}"

    if lowered.startswith("read file"):
        from tools.file_tools import read_file
        filename = user_message.replace("read file", "").strip()
        return f"📄 {read_file(filename)}"

    # (Optional: append_file, list_files, other tools here…)

    # 4️⃣ Retrieve long-term memory
    from memory.long_term import search_memory
    memories = search_memory(user_message)
    memory_context = "\n".join(memories) if memories else ""

    # 5️⃣ Include recent chat history
    from tools.file_tools import read_chat_history
    recent_history = read_chat_history(limit=10)

    from brain.llm import ask_llm, SYSTEM_PROMPT
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    if memory_context:
        chat_history.append({"role": "system", "content": f"Relevant memories:\n{memory_context}"})
    if recent_history:
        chat_history.append({"role": "system", "content": f"Recent conversation:\n{recent_history}"})

    chat_history.append({"role": "user", "content": user_message})

    # 6️⃣ Get AI reply
    reply = ask_llm(chat_history)

    # 7️⃣ Save assistant reply
    save_chat("Assistant", reply)

    # 8️⃣ Store new memory automatically
    triggers = ["my name is", "i like", "i love", "i work as", "i am", "i want"]
    if any(t in lowered for t in triggers):
        from memory.long_term import store_memory
        store_memory(user_message)

    return reply

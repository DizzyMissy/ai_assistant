import os

BASE_DIR = "workspace"
os.makedirs(BASE_DIR, exist_ok=True)

def create_file(filename, content):
    filepath = os.path.join(BASE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return f"File '{filename}' created successfully."


def read_file(filename):
    filepath = os.path.join(BASE_DIR, filename)

    if not os.path.exists(filepath):
        return "File not found."

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def list_files():
    files = os.listdir(BASE_DIR)
    return "\n".join(files) if files else "No files in workspace."


def append_file(filename, content):
    filepath = os.path.join(BASE_DIR, filename)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\n" + content)

    return f"Content appended to '{filename}'."

def save_memory(text):
    with open("workspace/memory.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return "Memory saved."


def read_memory():
    try:
        with open("workspace/memory.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No memory yet."


def auto_remember(user_input):
    triggers = ["my name is", "i like", "i want", "i work as"]

    lowered = user_input.lower()

    for t in triggers:
        if t in lowered:
            save_memory(user_input)
            return "🧠 Auto-remembered."

    return None
def save_chat(role, text):
    with open("workspace/chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"{role}: {text}\n")


def read_chat_history(limit=10):
    try:
        with open("workspace/chat_history.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            return "".join(lines[-limit:])
    except FileNotFoundError:
        return ""

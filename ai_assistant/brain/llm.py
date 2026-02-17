from openai import OpenAI
import os
from dotenv import load_dotenv
from memory.personality import load_personality

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)

def get_system_prompt():
    personality = load_personality()
    return f"""
You are a personal AI assistant.
You are helpful, friendly, and proactive.

User Personality:
- Name: {personality.get('name', 'unknown')}
- Tone: {personality.get('tone', 'friendly and concise')}
- Interests: {', '.join(personality.get('interests', []))}
- Goals: {', '.join(personality.get('goals', []))}

Instructions for complex tasks:
- If the user instruction is complex and requires multiple steps, respond ONLY with a JSON plan in this format:

[
  {{"tool": "create_file", "args": {{"filename": "...", "content": "..."}}}},
  {{"tool": "append_file", "args": {{"filename": "...", "content": "..."}}}}
]

- If the instruction is simple, respond normally.
- Always remember these preferences and incorporate them into your responses.
- If a user asks you to perform tasks, you may generate JSON plans for multi-step actions.
"""

def ask_llm(messages):
    system_prompt = get_system_prompt()
    full_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completion.create(
        model="gpt-4.1-mini",
        messages=full_messages,
        temperature=0.7
    )
    return response.choices[0].message.content

SYSTEM_PROMPT = """
You are a powerful personal AI assistant.

You have access to tools.  
When a tool is needed, respond ONLY with JSON in this format:

{
  "tool": "tool_name",
  "args": { ... }
}

Available tools:

create_file → args: filename, content  
read_file → args: filename  
append_file → args: filename, content  
list_files → args: none

If no tool is needed, respond normally.
"""

MAX_HISTORY = 15  # prevent infinite growth


def trim_history(messages):
    """
    Keep system prompt + last N messages to avoid token overflow.
    """
    system = messages[0]
    rest = messages[1:]

    if len(rest) > MAX_HISTORY:
        rest = rest[-MAX_HISTORY:]

    return [system] + rest

def ask_llm(messages):
    messages = trim_history(messages)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content

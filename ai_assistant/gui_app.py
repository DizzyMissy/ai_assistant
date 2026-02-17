import tkinter as tk
from tkinter import scrolledtext
from main import run_agent_loop  # We’ll adjust main.py to allow this
from threading import Thread


root = tk.Tk()
root.title("AI Assistant")
root.geometry("600x500")


chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_display.config(state=tk.DISABLED)


user_input = tk.Entry(root, width=80)
user_input.pack(padx=10, pady=(0, 10), side=tk.LEFT, expand=True)



def send_message():
    message = user_input.get()
    if message.strip() == "":
        return
    user_input.delete(0, tk.END)
    display_message("You", message)
    Thread(target=process_message, args=(message,)).start()  # Run AI in separate thread


send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=(0, 10), pady=(0, 10), side=tk.RIGHT)



def display_message(sender, message):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"{sender}: {message}\n\n")
    chat_display.yview(tk.END)
    chat_display.config(state=tk.DISABLED)



from brain.llm import ask_llm, SYSTEM_PROMPT
from memory.long_term import store_memory, search_memory
from tools.file_tools import save_chat, read_chat_history, auto_remember


def process_message(message):
    # Call the main AI agent logic from main.py
    reply = run_agent_loop(message)  # <-- handles memory, chat history, tools, personality

    # Save assistant reply to chat history file
    save_chat("Assistant", reply)

    # Display reply in the GUI
    display_message("Assistant", reply)



root.bind('<Return>', lambda event: send_message())


root.mainloop()

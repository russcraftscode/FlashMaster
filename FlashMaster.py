import tkinter as tk
import json

root = tk.Tk()
root.title("FlashMaster")
root.geometry("600x400")

#load data
with open("./flashData/linearCh3.json", 'r') as card_data_file:
    card_data = json.load(card_data_file)

print(card_data)

card_stack = [x for x in card_data]
current_card = 0

# Build the panels
question_frame = tk.Frame(root)
question_frame.pack(fill="both", expand=True)  # this grows with window

button_frame = tk.Frame(root)
button_frame.pack(side="bottom", fill="x")  # stays pinned to bottom, fills width

# Text panel
question_text = tk.Text(question_frame, width=80, height=5)
answer_text = tk.Text(question_frame, width=80, height=5)

question_text.pack(fill="both", expand=True, padx=5, pady=5)
answer_text.pack(fill="both", expand=True, padx=5, pady=5)


def next_card():
    """Shows the next card"""
    global current_card
    current_card += 1
    if current_card >= len(card_stack):
        current_card = 0
    card = card_stack[current_card]
    question_text.delete("1.0", tk.END)  # clear old question
    question_text.insert("0.0", card["question"])  # insert new question


def show_answer():
    global current_card
    card = card_stack[current_card]
    answer_text.delete("1.0", tk.END)  # clear old answer
    answer_text.insert("0.0", card["answer"])  # insert new answer


# Flashcard controls
next_button = tk.Button(button_frame, text="Next Card", command=next_card)
show_button = tk.Button(button_frame, text="Show Answer", command=show_answer)
right_button = tk.Button(button_frame, text="Got It")
maybe_button = tk.Button(button_frame, text="Unsure")
wrong_button = tk.Button(button_frame, text="Wrong")

next_button.pack(side="top", fill="x")
show_button.pack(side="top", fill="x")
right_button.pack(side="left", expand=True, fill="x")
maybe_button.pack(side="left", expand=True, fill="x")
wrong_button.pack(side="left", expand=True, fill="x")

root.mainloop()

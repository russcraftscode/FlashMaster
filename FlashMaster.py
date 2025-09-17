import tkinter as tk

root = tk.Tk()
root.title("FlashMaster")
root.geometry("600x400")

# Build the panels
question_frame = tk.Frame(root)
question_frame.pack(fill="both", expand=True)  # this grows with window

button_frame = tk.Frame(root)
button_frame.pack(side="bottom", fill="x")  # stays pinned to bottom, fills width

# Text panel
question_text = tk.Text(question_frame, width=80, height=10)
answer_text = tk.Text(question_frame, width=80, height=10)

question_text.pack(fill="both", expand=True, padx=5, pady=5)
answer_text.pack(fill="both", expand=True, padx=5, pady=5)

# Flashcard controls
show_button = tk.Button(button_frame, text="Show Answer")
right_button = tk.Button(button_frame, text="Got It")
maybe_button = tk.Button(button_frame, text="Unsure")
wrong_button = tk.Button(button_frame, text="Wrong")

show_button.pack(side="top", fill="x")
right_button.pack(side="left", expand=True,  fill="x")
maybe_button.pack(side="left", expand=True,  fill="x")
wrong_button.pack(side="left", expand=True,  fill="x")


root.mainloop()

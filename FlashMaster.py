import tkinter as tk
import json
import os
import random

root = tk.Tk()
root.title("FlashMaster")
root.geometry("900x400")

all_card_data = []
card_stack = []
current_card = 0
card_set_name = ""
card_count_var = tk.IntVar()
card_total_var = tk.IntVar()

# Build the panels
card_set_frame = tk.Frame(root)
card_set_frame.pack(side="left", fill="y")
shuffle_frame = tk.Frame(root)
shuffle_frame.pack(side="right", fill="y")
confidence_frame = tk.Frame(root)
confidence_frame.pack(side="right", fill="y")
question_frame = tk.Frame(root)
question_frame.pack(fill="both", expand=True)  # this grows with window

button_frame = tk.Frame(root)
button_frame.pack(side="bottom", fill="x")  # stays pinned to bottom, fills width

# Text panel
question_text = tk.Text(question_frame, wrap=tk.WORD, width=80, height=5)
answer_text = tk.Text(question_frame, wrap=tk.WORD, width=80, height=5)

question_text.pack(fill="both", expand=True, padx=5, pady=5)
answer_text.pack(fill="both", expand=True, padx=5, pady=5)

# Confidence Panel
conf_scroll_bar = tk.Scrollbar(confidence_frame)
conf_text = tk.Text(confidence_frame, yscrollcommand=conf_scroll_bar.set, width=20)
conf_scroll_bar.config(command=conf_text.yview)
conf_text.pack(side="left", fill="y")
conf_scroll_bar.pack(side="right", fill="y")


def update_confidence():
    global card_stack
    global current_card
    current_id = card_stack[current_card]["id"]
    conf_text.delete("1.0", tk.END)  # clear old confidence ratings
    for card in card_stack:
        # for all cards in the current stack add the ID and the confidence value
        #conf_text.insert("0.0", f"{card['id']} : {card['confidence']}\n")
        if card["id"] == current_id:
            conf_text.insert("0.0", f">>{card['id']:<3}: {card['confidence']}<<\n")
        else:
            conf_text.insert("0.0", f"{card['id']:<5}: {card['confidence']}\n")
    conf_text.insert("0.0", f"----   ----------\n")
    conf_text.insert("0.0", f"ID     rating\n")
    conf_text.insert("0.0", f"Card : Confidence\n")


def print_confidence():  # DEBUG
    print("#####")
    for card in card_stack:
        print(card["question"], card["confidence"])


def save_cards(card_filename):
    global all_card_data
    with open(f"./flashData/{card_filename}", 'w', encoding="utf-8") as card_data_file:
        json.dump(all_card_data, card_data_file, indent=4)


def load_cards(card_filename):
    global all_card_data
    global card_stack
    global current_card
    global card_set_name
    card_set_name = card_filename
    print(f"Loading card set:{card_set_name}")
    with open(f"./flashData/{card_filename}", 'r', encoding="utf-8") as card_data_file:
        all_card_data = json.load(card_data_file)
    #print(all_card_data)  # DEBUG
    draw_all_cards()
    update_confidence()


def draw_all_cards():
    global all_card_data
    global card_stack
    global current_card
    global card_set_name
    card_stack = []
    card_stack = [x for x in all_card_data]
    random.shuffle(card_stack)
    current_card = 0
    display_question()


def draw_number_cards(number_to_draw):
    global all_card_data
    global card_stack
    global current_card
    global card_set_name

    # first, make sure there are enough cards to draw left in the deck
    left_in_deck = len(all_card_data) - len(card_stack)
    if left_in_deck < number_to_draw:
        number_to_draw = left_in_deck

    # make a list with all the card ID's in it twice over
    all_card_ids = [card["id"] for card in all_card_data ]
    # print(all_card_ids) # DEBUG
    all_card_ids.sort()
    # print(all_card_ids) # DEBUG
    all_card_ids = all_card_ids + all_card_ids

    # find the highest ID currently in the stack
    lowest_id_in_deck = min(all_card_data, key=lambda x: x["id"])["id"]
    if len(card_stack) > 0:
        highest_id_in_stack = max(card_stack, key=lambda x: x["id"])["id"]

    # grab the next x cards who ID's are in the id list
    id_index = 0
    while(all_card_ids[id_index] != highest_id_in_stack): # seek to the id in the list
        id_index+=1
    for index_offset in range(number_to_draw):
        id_to_add = all_card_ids[index_offset+1]
        for card in all_card_data:
            if card["id"] == id_to_add:
                card_stack.append(card)
    update_confidence()
    display_question()

def draw_only_cards(number_to_draw):
    global all_card_data
    global card_stack
    global current_card
    global card_set_name
    #card_set_name = card_filename
    #print(f"Loading card set:{card_set_name}")
    #with open(f"./flashData/{card_filename}", 'r', encoding="utf-8") as card_data_file:
    #    all_card_data = json.load(card_data_file)
    #print(all_card_data)  # DEBUG
    draw_all_cards()
    card_stack = card_stack[:number_to_draw]
    update_confidence()
    display_question()


def draw_unsure_cards(number_of_cards):
    pass


def display_question():
    """Updates the question and answer text boxes to show a new question"""
    global current_card
    global card_set_name
    global card_count_var
    global card_total_var
    global card_stack

    # don't go out of range
    if current_card >= len(card_stack):
        current_card = 0

    #print("current card number", current_card) # DEBUG

    if len(card_stack) == 0:
        print("no cards in stack")

    card = card_stack[current_card]
    question_text.delete("1.0", tk.END)  # clear old question
    question_text.insert("0.0", card["question"])  # insert new question
    question_text.insert("0.0", "-------------------------\n")  # line sep
    question_text.insert("0.0",
                         f"Confidence with this card: {card['confidence']}\n")
    question_text.insert("0.0",
                         f"Current Flashcard Set: {card_set_name[:-5]}\n")
    answer_text.delete("1.0", tk.END)  # clear old answer
    card_count_var.set(current_card)
    card_total_var.set(len(card_stack))


def next_card():
    """Shows the next card"""
    global current_card
    #global card_set_name
    #global card_count_var
    #global card_total_var
    #global card_stack
    current_card += 1
    display_question()
    update_confidence()


def show_answer():
    global current_card
    card = card_stack[current_card]
    answer_text.delete("1.0", tk.END)  # clear old answer
    answer_text.insert("0.0", card["answer"])  # insert new answer


def got_right():
    """raises card confidence by 1"""
    global current_card
    card = card_stack[current_card]
    if card["confidence"] < 3:
        card["confidence"] += 1
    next_card()


def got_wrong():
    """lowers answer confidence by 1 down to a max of -2"""
    global current_card
    card = card_stack[current_card]
    if card["confidence"] > -2:
        card["confidence"] -= 1
    next_card()


def got_unsure():
    """Removes mastery, and sets card to slightly unsure"""
    global current_card
    card = card_stack[current_card]
    if card["confidence"] > -1:
        card["confidence"] = -1
    next_card()


def clear_conf():
    global all_card_data
    for card in all_card_data:
        card["confidence"] = 0
    update_confidence()
    display_question()


def discard_conf():
    global all_card_data
    global card_stack
    global current_card
    global card_set_name
    #card_set_name = card_filename
    print(f"Discarding cards user is confident in")

    temp_card_stack = []
    for card in card_stack:
        if card["confidence"] < 1:
            temp_card_stack.append(card)
    card_stack = temp_card_stack
    random.shuffle(card_stack)
    current_card = 0
    display_question()
    update_confidence()


def on_close():
    print("saving cards")
    global card_set_name
    save_cards(card_set_name)
    root.destroy()


#card set controls
card_set_label = tk.Label(card_set_frame, text="Select Flashcard Deck")
card_set_label.pack(anchor="w")
flash_files = []
for fname in os.listdir("./flashData/"):
    if fname.endswith(".json"):
        name = os.path.splitext(fname)[0]
        flash_files.append(name)
flash_files.sort() # put the files in aphabetical order to look neater
for name in flash_files:
    btn = tk.Button(
        card_set_frame,
        text=name,
        command=lambda f= name + ".json": load_cards(f)
    )
    btn.pack(anchor="w")  # stack vertically, left aligned

# Flashcard controls
next_button = tk.Button(button_frame, text="Next Card", command=next_card)
show_button = tk.Button(button_frame, text="Show Answer", command=show_answer)
right_button = tk.Button(button_frame, text="Got It", command=got_right)
maybe_button = tk.Button(button_frame, text="Unsure", command=got_unsure)
wrong_button = tk.Button(button_frame, text="Wrong", command=got_wrong)

next_button.pack(side="top", fill="x")
show_button.pack(side="top", fill="x")
right_button.pack(side="left", expand=True, fill="x")
maybe_button.pack(side="left", expand=True, fill="x")
wrong_button.pack(side="left", expand=True, fill="x")

# shuffle controls
active_card_frame = tk.Frame(shuffle_frame)
active_card_label = tk.Label(active_card_frame, text="Card ")
active_card_num_label = tk.Label(active_card_frame, textvariable=card_count_var)
total_card_label = tk.Label(active_card_frame, text=" of ")
total_card_num_label = tk.Label(active_card_frame, textvariable=card_total_var)
active_card_label.pack(side="left")
active_card_num_label.pack(side="left")
total_card_label.pack(side="left")
total_card_num_label.pack(side="left")

discard_button = tk.Button(shuffle_frame, text="Discard Confident", command=discard_conf)
reload_button = tk.Button(shuffle_frame, text="Reload cards", command=lambda: load_cards(card_set_name))
clear_button = tk.Button(shuffle_frame, text="Clear confidence", command=clear_conf)


def validate_digits(new_value):  #lets user enter digits only
    return new_value == "" or new_value.isdigit()

vcmd = (root.register(validate_digits), "%P")
num_to_draw = tk.IntVar(value=10)
draw_number_entry = tk.Entry(shuffle_frame, textvariable=num_to_draw, validate="key", validatecommand=vcmd)
draw_add_number_button = tk.Button(shuffle_frame, text="Draw x Additional Cards", command=lambda: draw_number_cards(num_to_draw.get()))
draw_only_number_button = tk.Button(shuffle_frame, text="Discard & Draw x Cards", command=lambda: draw_only_cards(num_to_draw.get()))

active_card_frame.pack(fill="x", pady=2)
discard_button.pack(fill="x", pady=2)
reload_button.pack(fill="x", pady=2)
clear_button.pack(fill="x", pady=2)
draw_number_entry.pack()
draw_add_number_button.pack()
draw_only_number_button.pack()

card_set_name = "mat343-ch1,ch2.json" # TODO: handle the default card set in a safer way
load_cards(card_set_name)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

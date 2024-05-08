from tkinter import *
from pandas import read_csv, DataFrame
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
CANVAS_COLOUR = ENGLISH_WORD_COLOUR = "white"
FRENCH_WORD_COLOUR = "black"
TITLE_FONT = "Arial", 40, "italic"
LANGUAGE_WORD_FONT = "Arial", 60, "bold"

window = Tk()
window.title("Flashy")


def read_words_to_learn_file():
    """Read from csv file words that will be displayed on flashcards in the app."""
    global words_to_learn_list
    # next time program is run
    if os.path.exists("data/words_to_learn.csv"):
        words_to_learn = read_csv("data/words_to_learn.csv")
    else:
        words_to_learn = read_csv("data/french_words.csv")
    words_to_learn_df = DataFrame(data=words_to_learn)
    words_to_learn_list = DataFrame.to_dict(words_to_learn_df, orient="records")


window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

canvas_img = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=TITLE_FONT)
card_word = canvas.create_text(400, 263, text="", font=LANGUAGE_WORD_FONT)
current_card = {}
words_to_learn_list = []


def display_next_word():
    """Displays next word's flashcard."""
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(words_to_learn_list)
    canvas.itemconfig(canvas_img, image=card_front)
    canvas.itemconfig(card_word, text=current_card['French'], fill=FRENCH_WORD_COLOUR)
    canvas.itemconfig(card_title, text="French", fill=FRENCH_WORD_COLOUR)
    flip_timer = window.after(3000, change_to_card_back)


def record_word_as_learnt_and_move_on_to_next_word():
    # remove seen word from french_to_english_words_dict
    words_to_learn_list.remove(current_card)
    words_to_learn_df = DataFrame(words_to_learn_list)
    # save to words_to_learn words to learn
    words_to_learn_df.to_csv("data/words_to_learn.csv", index=False)
    display_next_word()


def change_to_card_back():
    """Displays matching English word."""
    canvas.itemconfig(card_title, text="English", fill=ENGLISH_WORD_COLOUR)
    canvas.itemconfig(card_word, text=current_card['English'], fill=ENGLISH_WORD_COLOUR)
    canvas.itemconfig(canvas_img, image=card_back)


incorrect_img = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=incorrect_img, highlightthickness=0, command=display_next_word)
incorrect_button.grid(row=1, column=0)

correct_img = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_img, highlightthickness=0, command=
                                    record_word_as_learnt_and_move_on_to_next_word)
correct_button.grid(row=1, column=1)

flip_timer = window.after(3000, change_to_card_back)

read_words_to_learn_file()
display_next_word()

window.mainloop()

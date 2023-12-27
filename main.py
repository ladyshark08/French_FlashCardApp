from tkinter import *
import pandas
import pandas as pd

from random import choice

BACKGROUND_COLOR = "#B1DDC6"

# ------------------Read Data -------------------------------------------
data_frame = pd.read_csv("french_words.csv")
french_words_dict = {row.French: row.English for index, row in data_frame.iterrows()}
Fr_list = data_frame.French.to_list()
english_eq = ""
b_pressed = False
start = ""
new = ""
words_to_learn = []

try:
    with open("words_to_learn.csv", "r") as file:
        for line in file:
            line_split = line.split(";")
            words_to_learn.append(line_split[0].strip())
except FileNotFoundError:
    print("pass")


# --------------------------------------------------------------#

def create_words_to_learn():
    global new
    global english_eq
    with open("words_to_learn.csv", "a") as new_file:
        new_file.write(f"{new};{english_eq}\n")


# ___________________________REMOVE KNOWN WORDS______________________________________________________
def remove_known_words():
    global b_pressed
    global new
    if len(words_to_learn) == 0:
        try:
            Fr_list.remove(new)
        except ValueError:
            b_pressed = True
    else:
        try:
            words_to_learn.remove(new)
        except ValueError:
            b_pressed = True

# ---------------------------------#

def user_knows_word():
    print(words_to_learn)
    global new
    global b_pressed
    global english_eq
    global start
    if b_pressed:
        window.after_cancel(start)
        remove_known_words()
    b_pressed = True
    front.itemconfig(front_canvas, image=front_image)
    front.itemconfig(french_heading, text="French")
    if len(words_to_learn) == 0:
        new = choice(Fr_list)
    else:
        new = choice(words_to_learn)
    front.itemconfig(new_word, text=new)
    english_eq = french_words_dict[new]
    start = window.after(3000, flip)


def user_does_not():
    global new
    global english_eq
    global start
    create_words_to_learn()
    front.itemconfig(front_canvas, image=front_image)
    front.itemconfig(french_heading, text="French")
    new = choice(Fr_list)
    front.itemconfig(new_word, text=new)
    english_eq = french_words_dict[new]
    start = window.after(3000, flip)


# ----------------Flipping---------------------------#
def flip():
    window.after_cancel(start)
    global english_eq
    front.itemconfig(front_canvas, image=back_image)
    front.itemconfig(french_heading, text="English")
    front.itemconfig(new_word, text=english_eq)


# ----------------------------------------------------#

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
back_image = PhotoImage(file="images/card_back.png")
front_image = PhotoImage(file="images/card_front.png")
front = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_canvas = front.create_image(400, 263, image=front_image)

french_heading = front.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
new_word = front.create_text(400, 253, text="", font=("Arial", 60, "bold"))
front.grid(row=0, column=0, columnspan=2)
# --------------------------Buttons------------------------------
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=user_does_not)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=user_knows_word)
right_button.grid(row=1, column=1)
user_knows_word()

window.mainloop()
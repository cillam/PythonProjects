import requests
from random import randint
from functools import partial
from pynput import keyboard
from string import ascii_lowercase
from tiles import *

'''This is a Wordle program built using the Tkinter GUI library. The main file to run is 
Wordle_FinalProject_PriscillaMiller.py, which pulls some GUI elements from the tiles.py file along with functionality 
from the requests, random, functools, pynput, tkinter, and string modules. The user can either use their keyboard or 
use a mouse and the keyboard presented in the UI to input letters.
 
Note for game play: This Wordle is designed to function like the NYT Wordle game: A user will make a five-letter guess. 
After guessing, the user must press Enter. If the guessed word is not in the word list, a user message will state that 
the word is not in the word list. The user must backspace to delete unwanted letters and then resubmit. If the guessed
word is in the word list, the UI will update the letter tiles based on if the letters are in the word---turning green
if the letter is in the word and in the correct position, yellow if the letter is in the word but not in the right 
position, and gray if the letter is not in the word. As an added challenge, the user gets only 45 seconds for each
guess; the timer resets after each guess. If time runs out, the user automatically loses. If the user guesses wrong
six times, the user loses. After game play, the user can reset and play again.'''


# ------ Constants ------
LT_GRAY = "#D7DBDD"
DK_GRAY = "#566573"
GREEN = "#67BD1B"
YELLOW = "#ebcf34"
WHITE = "#FFFFFF"
BLACK = "#000000"
FONT_NAME = "Arial"
WORD_FONT = (FONT_NAME, 14, "bold")
BUTTON_FONT = (FONT_NAME, 12, "bold")
TILE_PROPS = {"x": 24, "y": 24, "text": "", "font": WORD_FONT}
BUTTON_PROPS = {"font": BUTTON_FONT, "width": 3, "height": 2, "relief": "flat", "borderwidth": 0,
                "highlightthickness": 0, "bg": LT_GRAY, "fg": BLACK}


# ------ Global variables ------
letters_of_guess = []
keys_used = {}
tries = 1
wordlist = []
wordle = ""
game_over = False
timer = None


# ------------ Timer functions ------------
# ------ Reset timer ------
def reset_timer():
    window.after_cancel(timer)
    timer_canvas.itemconfig(timer_text, text=f"Timer: 45 seconds")


# ------ Start timer ------
def start_timer():
    countdown(45)


# ------ Count down ------
def countdown(count):
    global game_over
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_canvas.itemconfig(timer_text, text=f"Timer: {count_sec} seconds")
    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)
    else:
        timer_canvas.itemconfig(timer_text, text=f"Sorry! You ran out of time.")
        send_message("lose")  # send message to user that they lost
        backspace_btn.configure(text="Reset", command=reset)
        game_over = True


# ------------ Game play functions ------------
# ------- Generate word list ------
def generate_wordlist():
    remove_list = ['slave', 'schwa', 'polio', 'didst', 'anode', 'lathe', 'dikes', 'bosom', 'imply', 'rotor', 'urine',
                   'nymph', 'asses', 'thine', 'sexes', 'daddy', 'emery', 'sunup', 'sloop', 'radii', 'booby', 'tepee',
                   'outdo', 'ketch', 'copra', 'tapir', 'floes', 'kinks', 'franc', 'mamma', 'rondo', 'jambs', 'lyres',
                   'conic', 'shalt', 'abbot', 'mikes', 'aster', 'cocci', 'umbra', 'voile', 'sulfa', 'civet', 'kinky',
                   'rills', 'ovule', 'enrol', 'gauss', 'bayed', 'larch', 'mamas', 'phlox', 'ingot', 'flied', 'dells',
                   'whelk', 'feted', 'cocos', 'sirup', 'laths', 'lodes', 'prows', 'etude', 'copse', 'boned', 'heres',
                   'haves', 'hells', 'soled', 'aping', 'quaff', 'rajah', 'scull', 'lores', 'ameba', 'adzes', 'ivies',
                   'papaw', 'jells', 'cruet', 'laxly', 'rends', 'loams', 'viler', 'lolls', 'diked', 'lowed', 'bests',
                   'boner', 'avers', 'pares', 'kales', 'arced', 'acnes', 'neons', 'fiefs', 'dints', 'yules', 'lilts',
                   'beefs', 'fells', 'lames', 'jawed', 'dupes', 'deads', 'noons', 'vireo', 'metes', 'sedge', 'papas',
                   'wheys', 'hilts', 'beaus', 'gists', 'yogas', 'zeals', 'soots', 'cress', 'doffs', 'biers', 'suets',
                   'hobos', 'lints', 'brans', 'teals', 'garbs', 'pewee', 'wends', 'banes', 'napes', 'pyres', 'bides',
                   'veals', 'dirks', 'tippy', 'piths', 'whets', 'wools', 'dirts', 'jutes', 'hemps', 'okapi', 'dusks',
                   'sears', 'novae', 'murks', 'slues', 'saris', 'dills', 'meany', 'bunts', 'razes', 'ruses', 'vends',
                   'judos', 'pulps', 'mucks', 'vises', 'gotta', 'fugue', 'radix', 'cubit', 'versa', 'adieu', 'terns',
                   'junta', 'alpha', 'prick', 'ephod', 'veldt', 'bream', 'rosin', 'bolls', 'doers', 'downs', 'humph',
                   'fella', 'mould', 'beryl', 'brier', 'canst', 'quoth', 'lemme', 'tenon', 'deeps', 'padre', 'leant',
                   'quipu', 'manna', 'duple', 'boron', 'revue', 'alack', 'inter', 'dilly', 'whist', 'spake', 'loess',
                   'lingo', 'dunno', 'sissy', 'calyx', 'coons', 'piney', 'lemma', 'whirr', 'saith', 'ionic', 'harem',
                   'dross', 'farad', 'jingo', 'bower', 'facto', 'toves', 'basal', 'yella', 'hymen', 'scrip', 'swash',
                   'aleph', 'tinny', 'wanta', 'trice', 'garde', 'sower', 'penal', 'sonny', 'quirt', 'mebbe', 'xenon',
                   'hullo', 'negro', 'hadst', 'aloes', 'quint', 'raped', 'salvo', 'hertz', 'xylem', 'cohos', 'sorta',
                   'gamba', 'axial', 'aleck', 'siree', 'bandy', 'gunny', 'runic', 'whizz', 'ochre', 'edger', 'gimme',
                   'theta', 'dykes', 'servo', 'telly', 'blocs', 'vitae', 'bronc', 'tabor', 'comer', 'borer', 'sired',
                   'privy', 'mammy', 'deary', 'quire', 'thugs', 'anion', 'fagot', 'letup', 'eyrie', 'axons', 'umber',
                   'miler', 'fibre', 'vitro', 'mater', 'umped', 'newel', 'treed', 'rangy', 'brads', 'mommy', 'motes',
                   'imams', 'hallo', 'canto', 'idyll', 'laity', 'ducal', 'metre', 'unary', 'goeth', 'baler', 'sited',
                   'hasps', 'brung', 'holed', 'swank', 'looky', 'loamy', 'pimps', 'shunt', 'seder', 'annas', 'coypu',
                   'shims', 'zowie']  # List of words that may be inappropriate or too obscure
    response = requests.get("https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt")
    data = response.text
    word_list = []
    for line in data.split():
        if len(line) == 5 and line not in remove_list:
            word_list.append(line)
    return word_list[:3417]  # Slices first half of list for most popular words


# ------- Pick word of the day from word list ------
def pick_word(words):
    word = words[randint(0, len(words))]
    return word


# ------ Click button from keyboard input from user ------
def button_click(key):
    try:
        if key == keyboard.Key.enter:
            key = "enter"
        elif key == keyboard.Key.backspace:
            key = "backspace_btn"
        else:
            if key.char in list(ascii_lowercase):
                key = key.char
        globals()[key].invoke()
    except AttributeError:  # if keyboard input not part of keyboard in GUI, input is ignored
        pass
    except KeyError:
        pass


# ------- Check letters of guess against picked word ------
def guess_letters(guess, wordle_word):
    letter_list = []
    for num in range(0, len(guess)):
        if guess[num] in wordle_word:
            if guess.count(guess[num]) <= wordle_word.count(guess[num]):
                if guess[num] == wordle_word[num]:
                    letter_list.append("green")
                else:
                    letter_list.append("yellow")
            elif guess.count(guess[num]) > wordle_word.count(guess[num]):
                guess_indices = [item for item in range(len(guess)) if guess[item] == guess[num]]
                wordle_indices = [item for item in range(len(wordle)) if wordle[item] == guess[num]]
                diff = [item for item in guess_indices if item not in wordle_indices]
                if num in wordle_indices:
                    letter_list.append("green")
                elif len(guess_indices) - len(wordle_indices) > 1:
                    if num == diff[-1] or num == diff[-2]:
                        letter_list.append("gray")
                    else:
                        letter_list.append("yellow")
                else:
                    if num == diff[-1]:
                        letter_list.append("gray")
                    else:
                        letter_list.append("yellow")
        else:
            letter_list.append("gray")
    update_letters(letter_list)  # Sends list of colors based on guess letters
    update_keyboard(list(guess), letter_list)  # Sends list of colors and list of guess letters
    if letter_list.count("green") == 5:
        return True


# # ------- Update UI colors of keyboard letters ------
def update_keyboard(chars, colors):
    global keys_used
    for letter in chars:
        if letter in keys_used.keys():  # once a key on the keyboard is green, it stays green
            if keys_used[letter] == "yellow" and colors[chars.index(letter)] == "green":
                keys_used.update({letter: colors[chars.index(letter)]})
            elif keys_used[letter] == "gray" and colors[chars.index(letter)] != "gray":
                keys_used.update({letter: colors[chars.index(letter)]})
        else:
            keys_used.update({letter: colors[chars.index(letter)]})
    for char, color in keys_used.items():
        if color == "green":
            globals()[char].configure(bg=GREEN, fg=WHITE)
        elif color == "yellow":
            globals()[char].configure(bg=YELLOW, fg=WHITE)
        else:
            globals()[char].configure(bg=DK_GRAY, fg=WHITE)


# ------- Update UI colors of guessed letter tiles ------
def update_letters(char_color_list):
    global letters_of_guess
    global tries
    for num in range(0, len(char_color_list)):
        canvas_bg = globals()["canvas" + str(tries) + "_" + str(num + 1)]
        word = globals()["word" + str(tries) + "_l" + str(num + 1)]
        canvas_bg.itemconfig(word, fill=WHITE)
        if char_color_list[num] == "green":
            canvas_bg.configure(bg=GREEN)
        elif char_color_list[num] == "yellow":
            canvas_bg.configure(bg=YELLOW)
        else:
            canvas_bg.configure(bg=DK_GRAY)
    letters_of_guess.clear()


# ------- Update guessed letters in tiles (before checking if guess == wordle) ------
def select_letters(char):
    global game_over
    global tries
    global letters_of_guess
    if game_over is False and len(letters_of_guess) < 5:
        letters_of_guess.append(char)
        canvas = globals()["canvas" + str(tries) + "_" + str(len(letters_of_guess))]
        word = globals()["word" + str(tries) + "_l" + str(len(letters_of_guess))]
        canvas.itemconfig(word, text=char.upper())


# ------- Delete letters from UI ------
def backspace():
    global tries
    global letters_of_guess
    if not game_over and len(letters_of_guess) > 0:
        canvas = globals()["canvas" + str(tries) + "_" + str(len(letters_of_guess))]
        word = globals()["word" + str(tries) + "_l" + str(len(letters_of_guess))]
        canvas.itemconfig(word, text="")
        letters_of_guess.pop()


# ------ Send messages to user ------
def send_message(code):
    global wordle
    message_canvas.configure(width=400, height=44)
    if code == "win":
        message_canvas.itemconfig(message, text="You win!")
    if code == "lose":
        message_canvas.itemconfig(message, text=f"You lose! The word is {wordle.upper()}.")
    if code == "not":
        message_canvas.itemconfig(message, text="Not in word list!")


# ------ Submit guess for checking and update number of tries ------
def submit_guess(guess):
    guess = ''.join(guess)
    global game_over, tries, wordle, wordlist
    if not game_over:
        if guess in wordlist and tries < 7:
            message_canvas.configure(width=200, height=10)
            win = guess_letters(guess, wordle)
            reset_timer()
            if win:
                send_message("win")  # send message to user that they won
                backspace_btn.configure(text="Reset", command=reset)
                game_over = True
            elif tries == 6:
                send_message("lose")  # send message to user that they lost
                backspace_btn.configure(text="Reset", command=reset)
                game_over = True
            else:
                start_timer()
            tries += 1
        else:
            if guess:
                send_message("not")  # send message to player that guess is not in word list


# ------ Reset for new game ------
def reset():
    global tries, game_over, wordle, letters_of_guess, keys_used
    letters_of_guess.clear()
    keys_used.clear()
    tries = 1
    wordle = ""
    game_over = False
    for x_num in range(1, 7):
        canvas = "canvas" + str(x_num)
        word = "word" + str(x_num)
        for y_num in range(1, 6):
            bg = globals()[canvas + "_" + str(y_num)]
            letter = globals()[word + "_l" + str(y_num)]
            bg.configure(bg=WHITE)
            bg.itemconfig(letter, fill=BLACK, text="")
    message_canvas.configure(height=10)
    message_canvas.itemconfig(message, text="")
    backspace_btn.configure(text="⌫", command=backspace)
    for char in list(ascii_lowercase):
        globals()[char].configure(bg=LT_GRAY, fg=BLACK)
    reset_timer()
    play()


# ---------------------------- UI setup ------------------------------- #
window = Tk()
window.title("Wordle")
window.config(padx=100, pady=50, bg=WHITE)

title_label = Label(text="Wordle", font=(FONT_NAME, 40, "bold"), bg=WHITE, fg=BLACK)
title_label.grid(column=0, row=0, columnspan=12)


# ------ First guess ------
frame1 = Tier(kwargs={"row": 1})

canvas1_1 = Tile(frame1, kwargs={"column": 0, "row": 0, "properties": TILE_PROPS})
word1_l1 = canvas1_1.letter
canvas1_2 = Tile(frame1, kwargs={"column": 1, "row": 0, "properties": TILE_PROPS})
word1_l2 = canvas1_2.letter
canvas1_3 = Tile(frame1, kwargs={"column": 2, "row": 0, "properties": TILE_PROPS})
word1_l3 = canvas1_3.letter
canvas1_4 = Tile(frame1, kwargs={"column": 3, "row": 0, "properties": TILE_PROPS})
word1_l4 = canvas1_4.letter
canvas1_5 = Tile(frame1, kwargs={"column": 4, "row": 0, "properties": TILE_PROPS})
word1_l5 = canvas1_5.letter


# ------ Second guess ------
frame2 = Tier(kwargs={"row": 2})

canvas2_1 = Tile(frame2, kwargs={"column": 0, "row": 0, "properties": TILE_PROPS})
word2_l1 = canvas2_1.letter
canvas2_2 = Tile(frame2, kwargs={"column": 1, "row": 0, "properties": TILE_PROPS})
word2_l2 = canvas2_2.letter
canvas2_3 = Tile(frame2, kwargs={"column": 2, "row": 0, "properties": TILE_PROPS})
word2_l3 = canvas2_3.letter
canvas2_4 = Tile(frame2, kwargs={"column": 3, "row": 0, "properties": TILE_PROPS})
word2_l4 = canvas2_4.letter
canvas2_5 = Tile(frame2, kwargs={"column": 4, "row": 0, "properties": TILE_PROPS})
word2_l5 = canvas2_5.letter


# ------ Third guess ------
frame3 = Tier(kwargs={"row": 3})

canvas3_1 = Tile(frame3, kwargs={"column": 0, "row": 0, "properties": TILE_PROPS})
word3_l1 = canvas3_1.letter
canvas3_2 = Tile(frame3, kwargs={"column": 1, "row": 0, "properties": TILE_PROPS})
word3_l2 = canvas3_2.letter
canvas3_3 = Tile(frame3, kwargs={"column": 2, "row": 0, "properties": TILE_PROPS})
word3_l3 = canvas3_3.letter
canvas3_4 = Tile(frame3, kwargs={"column": 3, "row": 0, "properties": TILE_PROPS})
word3_l4 = canvas3_4.letter
canvas3_5 = Tile(frame3, kwargs={"column": 4, "row": 0, "properties": TILE_PROPS})
word3_l5 = canvas3_5.letter


# ------ Fourth guess ------
frame4 = Tier(kwargs={"row": 4})

canvas4_1 = Tile(frame4, kwargs={"column": 0, "row": 0, "properties": TILE_PROPS})
word4_l1 = canvas4_1.letter
canvas4_2 = Tile(frame4, kwargs={"column": 1, "row": 0, "properties": TILE_PROPS})
word4_l2 = canvas4_2.letter
canvas4_3 = Tile(frame4, kwargs={"column": 2, "row": 0, "properties": TILE_PROPS})
word4_l3 = canvas4_3.letter
canvas4_4 = Tile(frame4, kwargs={"column": 3, "row": 0, "properties": TILE_PROPS})
word4_l4 = canvas4_4.letter
canvas4_5 = Tile(frame4, kwargs={"column": 4, "row": 0, "properties": TILE_PROPS})
word4_l5 = canvas4_5.letter


# ------ Fifth guess ------
frame5 = Tier(kwargs={"row": 5})

canvas5_1 = Tile(frame5, kwargs={"column": 0, "row": 0, "properties": TILE_PROPS})
word5_l1 = canvas5_1.letter
canvas5_2 = Tile(frame5, kwargs={"column": 1, "row": 0, "properties": TILE_PROPS})
word5_l2 = canvas5_2.letter
canvas5_3 = Tile(frame5, kwargs={"column": 2, "row": 0, "properties": TILE_PROPS})
word5_l3 = canvas5_3.letter
canvas5_4 = Tile(frame5, kwargs={"column": 3, "row": 0, "properties": TILE_PROPS})
word5_l4 = canvas5_4.letter
canvas5_5 = Tile(frame5, kwargs={"column": 4, "row": 0, "properties": TILE_PROPS})
word5_l5 = canvas5_5.letter


# ------ Sixth guess ------
frame6 = Tier(kwargs={"row": 6})

canvas6_1 = Tile(frame6, kwargs={"column": 0, "row": 0, "properties": TILE_PROPS})
word6_l1 = canvas1_1.letter
canvas6_2 = Tile(frame6, kwargs={"column": 1, "row": 0, "properties": TILE_PROPS})
word6_l2 = canvas1_2.letter
canvas6_3 = Tile(frame6, kwargs={"column": 2, "row": 0, "properties": TILE_PROPS})
word6_l3 = canvas1_3.letter
canvas6_4 = Tile(frame6, kwargs={"column": 3, "row": 0, "properties": TILE_PROPS})
word6_l4 = canvas1_4.letter
canvas6_5 = Tile(frame6, kwargs={"column": 4, "row": 0, "properties": TILE_PROPS})
word6_l5 = canvas1_5.letter


# ------ Extra padding frame/user messages ------
frame7 = Tier(kwargs={"row": 7})
message_canvas = Canvas(frame7, width=200, height=10, bg=WHITE, highlightthickness=0)
message = message_canvas.create_text(200, 24, text="", font=WORD_FONT)
message_canvas.grid(column=0, row=0, columnspan=12)


# ------ Keyboard buttons -------
# ------ Keyboard row 1 ------
frame8 = Tier(kwargs={"row": 8})

q = LetterKey(frame8, kwargs={"text": "Q", "column": 0, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "q")})
w = LetterKey(frame8, kwargs={"text": "W", "column": 1, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "w")})
e = LetterKey(frame8, kwargs={"text": "E", "column": 2, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "e")})
r = LetterKey(frame8, kwargs={"text": "R", "column": 3, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "r")})
t = LetterKey(frame8, kwargs={"text": "T", "column": 4, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "t")})
y = LetterKey(frame8, kwargs={"text": "Y", "column": 5, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "y")})
u = LetterKey(frame8, kwargs={"text": "U", "column": 6, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "u")})
i = LetterKey(frame8, kwargs={"text": "I", "column": 7, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "i")})
o = LetterKey(frame8, kwargs={"text": "O", "column": 8, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "o")})
p = LetterKey(frame8, kwargs={"text": "P", "column": 9, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "p")})


# ------ Keyboard row 2 ------
frame9 = Tier(kwargs={"row": 9})

a = LetterKey(frame9, kwargs={"text": "A", "column": 0, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "a")})
s = LetterKey(frame9, kwargs={"text": "S", "column": 1, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "s")})
d = LetterKey(frame9, kwargs={"text": "D", "column": 2, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "d")})
f = LetterKey(frame9, kwargs={"text": "F", "column": 3, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "f")})
g = LetterKey(frame9, kwargs={"text": "G", "column": 4, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "g")})
h = LetterKey(frame9, kwargs={"text": "H", "column": 5, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "h")})
j = LetterKey(frame9, kwargs={"text": "J", "column": 6, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "j")})
k = LetterKey(frame9, kwargs={"text": "K", "column": 7, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "k")})
l = LetterKey(frame9, kwargs={"text": "L", "column": 8, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "l")})


# ------ Keyboard row 3 ------
frame10 = Tier(kwargs={"row": 10})

z = LetterKey(frame10, kwargs={"text": "Z", "column": 1, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "z")})
x = LetterKey(frame10, kwargs={"text": "X", "column": 2, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "x")})
c = LetterKey(frame10, kwargs={"text": "C", "column": 3, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "c")})
v = LetterKey(frame10, kwargs={"text": "V", "column": 4, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "v")})
b = LetterKey(frame10, kwargs={"text": "B", "column": 5, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "b")})
n = LetterKey(frame10, kwargs={"text": "N", "column": 6, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "n")})
m = LetterKey(frame10, kwargs={"text": "M", "column": 7, "properties": BUTTON_PROPS, "command":
              partial(select_letters, "m")})
enter = LetterKey(frame10, kwargs={"text": "Enter", "column": 0, "properties": BUTTON_PROPS, "command":
                  partial(submit_guess, letters_of_guess)})
enter.configure(width=6)
backspace_btn = LetterKey(frame10, kwargs={"text": "⌫", "column": 8, "properties": BUTTON_PROPS, "command": backspace})
backspace_btn.configure(width=6)


# ------ Timer text UI ------
frame11 = Tier(kwargs={"row": 11})
timer_canvas = Canvas(frame11, width=400, height=44, bg=WHITE, highlightthickness=0)
timer_text = timer_canvas.create_text(200, 24, text="Timer: 45 seconds", font=WORD_FONT)
timer_canvas.grid(column=0, row=0, columnspan=12)


# ------ Initiate keyboard listener ------
listener = keyboard.Listener(on_release=button_click)
listener.start()


# ------- Initiate game play -------
def play():
    global game_over, wordlist, wordle, letters_of_guess, tries
    if not game_over:
        if not wordlist:
            wordlist = generate_wordlist()
        if not wordle:
            wordle = pick_word(wordlist)
        start_timer()
#    print(wordle)  # For testing


play()
window.mainloop()

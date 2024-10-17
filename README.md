#Wordle_FinalProject

This is a Wordle program built using the Tkinter GUI library. The main file to run is 
Wordle_FinalProject.py, which pulls some GUI elements from the tiles.py file along with functionality 
from the requests, random, functools, pynput, tkinter, and string modules. The user can either use their keyboard or 
use a mouse and the keyboard presented in the UI to input letters.
 
Note for game play: This Wordle is designed to function like the NYT Wordle game: A user will make a five-letter guess. 
After guessing, the user must press Enter. If the guessed word is not in the word list, a user message will state that 
the word is not in the word list. The user must backspace to delete unwanted letters and then resubmit. If the guessed
word is in the word list, the UI will update the letter tiles based on if the letters are in the word---turning green
if the letter is in the word and in the correct position, yellow if the letter is in the word but not in the right 
position, and gray if the letter is not in the word. As an added challenge, the user gets only 45 seconds for each
guess; the timer resets after each guess. If time runs out, the user automatically loses. If the user guesses wrong
six times, the user loses. After game play, the user can reset and play again.

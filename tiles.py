from tkinter import *
'''tiles.py provides classes for GUI elements in Wordle_FinalProject_PriscillaMiller.py'''

class Tier(Frame):
    def __init__(self, **kwargs):
        super().__init__()
        options = {"height": 40,
                   "bg": "#FFFFFF"}
        self.kwargs = kwargs["kwargs"]
        self.configure(options)
        self.grid(column=0, row=self.kwargs["row"], columnspan=12)


class Tile(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        options = {"width": 44,
                   "height": 44,
                   "bg": "#FFFFFF",
                   "highlightthickness": 2}
        self.configure(options)
        self._kwargs = kwargs["kwargs"]
        self._properties = self._kwargs["properties"]
        self.letter = self.create_text(self._properties["x"], self._properties["y"], text=self._properties["text"],
                                       font=self._properties["font"])
        self.grid(column=self._kwargs["column"], row=self._kwargs["row"], padx=2, pady=2)


class LetterKey(Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self._kwargs = kwargs["kwargs"]
        self.configure(text=self._kwargs["text"], font=self._kwargs["properties"]["font"],
                       width=self._kwargs["properties"]["width"], height=self._kwargs["properties"]["height"],
                       relief=self._kwargs["properties"]["relief"],
                       borderwidth=self._kwargs["properties"]["borderwidth"],
                       highlightthickness=self._kwargs["properties"]["highlightthickness"],
                       bg=self._kwargs["properties"]["bg"], fg=self._kwargs["properties"]["fg"],
                       command=self._kwargs["command"])
        self.grid(column=self._kwargs["column"], row=0, padx=2, pady=2)

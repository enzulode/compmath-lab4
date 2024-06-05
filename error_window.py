from typing import *
from customtkinter import *
from typing import *

class ErrorWindow(CTkToplevel):
  def __init__(self, message: str, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.title('Error')
    self.geometry('600x200')

    # window message
    label: CTkLabel = CTkLabel(self, text=message, height=40, wraplength=500)
    label.pack()
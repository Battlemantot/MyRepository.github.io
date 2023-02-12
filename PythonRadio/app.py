import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()
saveFile = "PythonRadio/save.txt"
os.makedirs(os.path.dirname(saveFile), exist_ok=True)
radio_source = "https://opml.radiotime.com"
# http://stream.radioparadise.com/rock-128


# Load save file
#if os.path.isfile('save.txt'):
#   with open('save.txt', 'r') as f:
#       tempApps = f.read()
#        print(tempApps)

def StartRadio():
    print("huh")

canvas = tk.Canvas(root, height=680, width=680, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

sRadioButton = tk.Button(root, text="Start radio", padx=10, pady=5, fg="white", bg="#263D42", command=StartRadio)
sRadioButton.pack()


root.mainloop()

# Save a file

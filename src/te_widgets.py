import tkinter as tk

root = tk.Tk()
text = tk.Text(root)
lines = tk.Text(root)
footer = tk.Label(root)

def setTitle(title: str):
    root.title(title)


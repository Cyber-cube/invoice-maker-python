import tkinter as tk
from autocomplete import AutoComplete

root = tk.Tk()
root.title("Test")
root.geometry("500x400")

items = ["Apple Pie", "Mango", "Sweet Apple", "Test"]

entry = tk.Entry(root)
entry.grid(row=0, column=0)

label = tk.Label(root, text="Hi")
label.grid(row=1, column=0)

auto_complete = AutoComplete(entry, items)

tk.mainloop()

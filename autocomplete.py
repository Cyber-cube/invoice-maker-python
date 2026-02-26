import tkinter as tk

from numpy import delete

class AutoComplete:
    def __init__(self, entry, items):
        self.entry = entry
        self.items = items

        self.frame = tk.Frame(self.entry.master, width=10, height=10)

        self.is_frame_visible = False

        # Create a listbox but don't place it initially
        self.listbox = tk.Listbox(self.frame)

        # Add the scrollbar
        self.scrollbar = tk.Scrollbar(self.listbox, orient=tk.VERTICAL)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.scrollbar2 = tk.Scrollbar(self.listbox, orient=tk.HORIZONTAL)
        self.listbox.config(xscrollcommand=self.scrollbar2.set)
        self.scrollbar2.config(command=self.listbox.xview)

        # Pack the scrollbar and listbox within the frame
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar2.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind events to entry widget
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<Return>", self.on_enter_key)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def on_entry_key(self, event):
        typed_text = self.entry.get()

        if typed_text == "":
            self.frame.place_forget()
            self.is_frame_visible = False
        else:
            # Filter and show listbox based on entry text
            self.listbox.delete(0, tk.END)
            for item in self.items:
                words = item.split()
                if item.lower().startswith(typed_text.lower()):
                    self.listbox.insert(tk.END, item)
            
            # Display the listbox below the entry widget
            if not self.is_frame_visible:
                self.frame.place(x=self.entry.winfo_x()-50, y=self.entry.winfo_y() + self.entry.winfo_height(), width=150, height=100)
                self.frame.lift()
                self.is_frame_visible = True

    def on_listbox_select(self, event):
        if self.listbox.curselection():
            selected_item = self.listbox.get(self.listbox.curselection())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_item)
            self.frame.place_forget()
            self.is_frame_visible = False

    def on_enter_key(self, event):
        self.frame.place_forget()
        return "break"

    

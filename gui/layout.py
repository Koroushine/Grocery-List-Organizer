import tkinter as tk
from tkinter import ttk, messagebox
from database import db_config

class GroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery List Organizer")
        self.root.geometry("600x400")  # Set a bigger starting size
        self.root.minsize(500, 300)    # Set a minimum window size
        self.conn = db_config.connect_db()

        self.item_var = tk.StringVar()
        self.quantity_var = tk.IntVar()

        self.build_widgets()
        self.refresh_list()

    def build_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        for i in range(4):
            frame.columnconfigure(i, weight=1)
        frame.rowconfigure(3, weight=1)

        # Item Label & Entry
        ttk.Label(frame, text="Item:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.item_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Quantity Label & Entry
        ttk.Label(frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.quantity_var, width=30).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        ttk.Button(frame, text="Add", command=self.add_item).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ttk.Button(frame, text="Remove", command=self.remove_item).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Treeview
        self.tree = ttk.Treeview(frame, columns=("Item", "Quantity"), show="headings")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.column("Item", anchor="center", width=200)
        self.tree.column("Quantity", anchor="center", width=100)

        self.tree.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=5, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=3, column=4, sticky="ns")

    def add_item(self):
        item = self.item_var.get().strip()
        quantity = self.quantity_var.get()
        if item and quantity > 0:
            db_config.add_item(self.conn, item, quantity)
            self.refresh_list()
            self.item_var.set("")
            self.quantity_var.set(0)
        else:
            messagebox.showwarning("Input Error", "Enter valid item and quantity.")

    def remove_item(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values'][0]
            db_config.remove_item(self.conn, item)
            self.refresh_list()
        else:
            messagebox.showinfo("Select Item", "Please select an item to remove.")

    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item, quantity in db_config.get_items(self.conn):
            self.tree.insert("", "end", values=(item, quantity))

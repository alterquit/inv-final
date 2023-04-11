import tkinter as tk
from tkinter import ttk
import sqlite3

class SearchConfiguration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Use the ttk themes for better appearance
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Customize the appearance of the widgets
        self.style.configure('TLabel', background='#d0e1f9', foreground='black', font=("Helvetica", 12))  # Update the background color here
        self.style.configure('Title.TLabel', font=("Helvetica", 18, 'bold'))
        self.style.configure('TButton', font=("Helvetica", 12, 'bold'))
        self.style.configure('TEntry', font=("Helvetica", 12))

        self.configure(bg='#f0f0f0')

        self.connect_to_database()
        self.create_widgets()
    # Connect to the database
    def connect_to_database(self):
        self.conn = sqlite3.connect('inventory_management.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                details TEXT
            )
        ''')
        self.conn.commit()

    # Layout
    def create_widgets(self):
        title = tk.Label(self, text="Search & Configuration", font=("Helvetica", 18))
        title.pack(pady=20)

        search_label = tk.Label(self, text="Search by keyword:")
        search_label.pack(pady=(0, 5))
        self.search_entry = tk.Entry(self)
        self.search_entry.pack(pady=(0, 10))

        search_button = tk.Button(self, text="Search", command=self.search_product)
        search_button.pack(pady=10)

        self.result_label = tk.Label(self, text="Results:")
        self.result_label.pack(pady=(10, 0))

        result_frame = tk.Frame(self)
        result_frame.pack(pady=10)

        self.result_listbox = tk.Listbox(result_frame, width=40, height=10)
        self.result_listbox.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_listbox.yview)
        scrollbar.pack(side="right", fill="y")

        self.result_listbox.config(yscrollcommand=scrollbar.set)

        add_product_label = tk.Label(self, text="Add Product:")
        add_product_label.pack(pady=(10, 5))
        self.add_product_entry = tk.Entry(self)
        self.add_product_entry.pack(pady=(0, 10))

        add_button = tk.Button(self, text="Add", command=self.add_product)
        add_button.pack(pady=10)

        update_product_old_label = tk.Label(self, text="Old Product Name:")
        update_product_old_label.pack()
        self.update_product_old_entry = tk.Entry(self)
        self.update_product_old_entry.pack()

        update_product_new_label = tk.Label(self, text="New Product Name:")
        update_product_new_label.pack()
        self.update_product_new_entry = tk.Entry(self)
        self.update_product_new_entry.pack()

        update_button = tk.Button(self, text="Update", command=self.update_product)
        update_button.pack(pady=10)

        delete_product_label = tk.Label(self, text="Delete Product:")
        delete_product_label.pack(pady=(10, 5))
        self.delete_product_entry = tk.Entry(self)
        self.delete_product_entry.pack(pady=(0, 10))

        delete_button = tk.Button(self, text="Delete", command=self.delete_product)
        delete_button.pack(pady=10)


    # Search function
    def search_product(self):
        keyword = self.search_entry.get()
        self.cursor.execute("SELECT name FROM products WHERE name LIKE ?", ('%' + keyword + '%',))
        results = self.cursor.fetchall()

        self.result_listbox.delete(0, 'end')
        for result in results:
            self.result_listbox.insert('end', result[0])

        self.result_label['text'] = f'Results ({len(results)}):'

    # Add function
    def add_product(self):
        product_name = self.add_product_entry.get()
        self.cursor.execute("SELECT name FROM products WHERE name = ?", (product_name,))
        existing_product = self.cursor.fetchone()

        if not existing_product:
            self.cursor.execute("INSERT INTO products (name, details) VALUES (?, ?)", (product_name, 'Sample Details'))
            self.conn.commit()
            self.add_product_entry.delete(0, 'end')
            self.result_label['text'] = f"Added {product_name}"
        else:
            self.result_label['text'] = f"{product_name} already exists"

    # Update function
    def update_product(self):
        old_name = self.update_product_old_entry.get()
        new_name = self.update_product_new_entry.get()
        self.cursor.execute("SELECT id FROM products WHERE name = ?", (old_name,))
        existing_product = self.cursor.fetchone()

        if existing_product:
            self.cursor.execute("UPDATE products SET name = ? WHERE name = ?", (new_name, old_name))
            self.conn.commit()
            self.update_product_old_entry.delete(0, 'end')
            self.update_product_new_entry.delete(0, 'end')
            self.result_label['text'] = f"Updated {old_name} to {new_name}"
        else:
            self.result_label['text'] = f"{old_name} not found"

    # Delete function
    def delete_product(self):
        product_name = self.delete_product_entry.get()
        self.cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
        existing_product = self.cursor.fetchone()

        if existing_product:
            self.cursor.execute("DELETE FROM products WHERE name = ?", (product_name,))
            self.conn.commit()
            self.delete_product_entry.delete(0, 'end')
            self.result_label['text'] = f"Deleted {product_name}"
        else:
            self.result_label['text'] = f"{product_name} not found"

    # close the database connection when the application is closed
    def __del__(self):
        self.conn.close()


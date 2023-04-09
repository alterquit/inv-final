import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring

class UserManagement(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.conn = app.conn

        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("username", "password", "user_type"), show="headings")
        self.tree.heading("username", text="Username")
        self.tree.heading("password", text="Password")
        self.tree.heading("user_type", text="User Type")
        self.tree.pack(side="top", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Buttons for add, delete, and modify user
        btn_frame = tk.Frame(self)
        btn_frame.pack(side="bottom", fill="x")

        add_btn = tk.Button(btn_frame, text="Add User", command=self.add_user)
        add_btn.pack(side="left")
        delete_btn = tk.Button(btn_frame, text="Delete User", command=self.delete_user)
        delete_btn.pack(side="left")
        modify_btn = tk.Button(btn_frame, text="Modify User Type", command=self.modify_user_type)
        modify_btn.pack(side="left")

    def load_users(self):
        self.tree.delete(*self.tree.get_children())

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        for user in users:
            self.tree.insert("", "end", values=(user[0], user[1], user[2]))

    def add_user(self):
        username = askstring("Add User", "Enter username:")
        password = askstring("Add User", "Enter password:", show="*")
        user_type = askstring("Add User", "Enter user type (admin or user):")

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO user (username, password, user_type) VALUES (?, ?, ?)", (username, password, user_type))
        self.conn.commit()
        self.load_users()

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete.")
            return

        username = self.tree.item(selected_item[0])["values"][0]
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM user WHERE username=?", (username,))
        self.conn.commit()
        self.load_users()

    def modify_user_type(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to modify.")
            return

        username = self.tree.item(selected_item[0])["values"][0]
        user_type = askstring("Modify User Type", "Enter new user type (admin or user):")

        cursor = self.conn.cursor()
        cursor.execute("UPDATE user SET user_type=? WHERE username=?", (user_type, username))
        self.conn.commit()
        self.load_users()

# Usage example
if __name__ == "__main__":
    import sqlite3

    class DummyApp:
        def __init__(self):
            self.conn = sqlite3.connect("inventory_management.db")

    app = DummyApp()
    root = tk.Tk()
    um = UserManagement(root, app)
    um.pack(fill="both", expand=True)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox


def show_login(app):
    app.login_frame = tk.Frame(app)
    app.login_frame.pack(side="top", fill="both", expand=True)

    app.login_frame.configure(bg="#F0F0F0")

    title = tk.Label(app.login_frame, text="Inventory Management System", font=("Helvetica", 20, "bold"), bg="#F0F0F0")
    title.pack(pady=20)

    username_label = tk.Label(app.login_frame, text="Username:", font=("Helvetica", 12, "bold"), bg="#F0F0F0")
    username_label.pack()

    username_entry = tk.Entry(app.login_frame)
    username_entry.pack(pady=5)

    password_label = tk.Label(app.login_frame, text="Password:", font=("Helvetica", 12, "bold"), bg="#F0F0F0")
    password_label.pack()

    password_entry = tk.Entry(app.login_frame, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(app.login_frame, text="Login", font=("Helvetica", 10, "bold"),
                             command=lambda: validate_user(app, username_entry.get(), password_entry.get()))
    login_button.pack(pady=10)

    register_button = tk.Button(app.login_frame, text="Register", font=("Helvetica", 10, "bold"),
                                command=lambda: show_register(app))
    register_button.pack(pady=5)


def show_register(app):
    app.login_frame.destroy()

    app.register_frame = tk.Frame(app)
    app.register_frame.pack(side="top", fill="both", expand=True)

    app.register_frame.configure(bg="#F0F0F0")

    title = tk.Label(app.register_frame, text="Register", font=("Helvetica", 20, "bold"), bg="#F0F0F0")
    title.pack(pady=20)

    username_label = tk.Label(app.register_frame, text="Username:", font=("Helvetica", 12, "bold"), bg="#F0F0F0")
    username_label.pack()

    username_entry = tk.Entry(app.register_frame)
    username_entry.pack(pady=5)

    password_label = tk.Label(app.register_frame, text="Password:", font=("Helvetica", 12, "bold"), bg="#F0F0F0")
    password_label.pack()

    password_entry = tk.Entry(app.register_frame, show="*")
    password_entry.pack(pady=5)

    confirm_password_label = tk.Label(app.register_frame, text="Confirm Password:", font=("Helvetica", 12, "bold"),
                                      bg="#F0F0F0")
    confirm_password_label.pack()

    confirm_password_entry = tk.Entry(app.register_frame, show="*")
    confirm_password_entry.pack(pady=5)

    register_button = tk.Button(app.register_frame, text="Register", font=("Helvetica", 10, "bold"),
                                command=lambda: register_user(app, username_entry.get(), password_entry.get(),
                                                              confirm_password_entry.get()))
    register_button.pack(pady=10)

    back_button = tk.Button(app.register_frame, text="Back to Login", font=("Helvetica", 10, "bold"),
                            command=lambda: back_to_login(app))
    back_button.pack(pady=5)


def back_to_login(app):
    app.register_frame.destroy()
    show_login(app)


def validate_user(app, username, password):
    cursor = app.conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result is not None:
        app.user_type = result[2]
        app.login_frame.destroy()
        app.start_app()
    else:
        messagebox.showerror("Error", "Invalid username or password")


def register_user(app, username, password, confirm_password):
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    cursor = app.conn.cursor()
    cursor.execute("INSERT INTO user (username, password, user_type) VALUES (?, ?, ?)", (username, password, "user"))
    app.conn.commit()

    messagebox.showinfo("Success", "User registered successfully")
    app.register_frame.grid_forget()
    show_login(app)


def register_user(app, username, password, confirm_password):
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    cursor = app.conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        messagebox.showerror("Error", "Username already exists")
        return

    # If the username doesn't exist, insert a new user record
    cursor.execute("INSERT INTO user (username, password, user_type) VALUES (?, ?, ?)", (username, password, "user"))
    app.conn.commit()

    messagebox.showinfo("Success", "User registered successfully")
    app.register_frame.destroy()
    show_login(app)

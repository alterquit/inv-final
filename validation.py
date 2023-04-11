import tkinter as tk
from tkinter import messagebox

def on_enter(e):
    e.widget.config(bg="#3A9AD9")

def on_leave(e):
    e.widget.config(bg="SystemButtonFace")

def center_widgets(frame):
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

# Login page
def show_login(app):
    app.login_frame = tk.Frame(app, bg="lightblue")
    app.login_frame.pack(side="top", fill="both", expand=True)

    center_widgets(app.login_frame)

    content_frame = tk.Frame(app.login_frame, bg="lightblue")
    content_frame.grid(row=0, column=0)

    title = tk.Label(content_frame, text="Inventory Management System", font=("Helvetica", 40, "bold"), bg="lightblue")
    title.pack(pady=40)

    username_label = tk.Label(content_frame, text="Username:", font=("Helvetica", 25, "bold"), bg="lightblue")
    username_label.pack()

    username_entry = tk.Entry(content_frame, width= 30)
    username_entry.pack(pady=20)

    password_label = tk.Label(content_frame, text="Password:", font=("Helvetica", 25, "bold"), bg="lightblue")
    password_label.pack()

    password_entry = tk.Entry(content_frame, show="*", width= 30, )
    password_entry.pack(pady=20)

    login_button = tk.Button(content_frame, text="Login", font=("Helvetica", 20, "bold"),
                             command=lambda: validate_user(app, username_entry.get(), password_entry.get()))
    login_button.pack(pady=30, padx=0)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    register_button = tk.Button(content_frame, text="Register", font=("Helvetica", 20, "bold"),
                                command=lambda: show_register(app))
    register_button.pack(pady=15, padx=0)
    register_button.bind("<Enter>", on_enter)
    register_button.bind("<Leave>", on_leave)

# Register page
def show_register(app):
    app.login_frame.destroy()

    app.register_frame = tk.Frame(app, bg="lightblue")
    app.register_frame.pack(side="top", fill="both", expand=True)

    center_widgets(app.register_frame)

    content_frame = tk.Frame(app.register_frame, bg="lightblue")
    content_frame.grid(row=0, column=0)

    title = tk.Label(content_frame, text="Register", font=("Helvetica", 40, "bold"), bg="lightblue")
    title.pack(pady=40)

    username_label = tk.Label(content_frame, text="Username:", font=("Helvetica", 25, "bold"), bg="lightblue")
    username_label.pack(pady=10)

    username_entry = tk.Entry(content_frame, width=30)
    username_entry.pack(pady=10)

    password_label = tk.Label(content_frame, text="Password:", font=("Helvetica", 25, "bold"), bg="lightblue")
    password_label.pack(pady=10)

    password_entry = tk.Entry(content_frame, show="*", width=30)
    password_entry.pack(pady=10)

    confirm_password_label = tk.Label(content_frame, text="Confirm Password:", font=("Helvetica", 25, "bold"),
                                      bg="lightblue")
    confirm_password_label.pack(pady=10)

    confirm_password_entry = tk.Entry(content_frame, show="*", width=30)
    confirm_password_entry.pack(pady=10)

    register_button = tk.Button(content_frame, text="Register", font=("Helvetica", 20, "bold"),
                                command=lambda: register_user(app, username_entry.get(), password_entry.get(),
                                                              confirm_password_entry.get()))
    register_button.pack(pady=20)
    register_button.bind("<Enter>", on_enter)
    register_button.bind("<Leave>", on_leave)

    back_button = tk.Button(content_frame, text="Back to Login", font=("Helvetica", 20, "bold"),
                            command=lambda: back_to_login(app))
    back_button.pack(pady=10)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)

# back to login page
def back_to_login(app):
    app.register_frame.destroy()
    show_login(app)

# confirm logic
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
    if not username or not password or not confirm_password:
        messagebox.showerror("Error", "Please enter valid information for all fields")
        return

    if len(username) < 6 or len(password) < 6:
        messagebox.showerror("Error", "Username and password must be at least 6 characters long")
        return

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

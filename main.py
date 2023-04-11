import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from overview import Overview
from search_configuration import SearchConfiguration
from user_management import UserManagement
from stats_report import StatsReport
import sqlite3
from validation import show_login


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.username = ''
        # Layout
        self.geometry("1030x900")
        self.title("Inventory management system")
        # Connect to the database
        self.conn = sqlite3.connect("inventory_management.db")
        self.user_type = None

        show_login(self)

    # Global setting
    def start_app(self):
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.content_frame = tk.Frame(self.container)
        self.content_frame.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (Overview, SearchConfiguration, UserManagement, StatsReport):
            if F == Overview:
                frame = F(self.content_frame, self, self.username)
            else:
                frame = F(self.content_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_navigation_buttons(self.container)  # Move this line here

        self.show_frame(Overview)

    # Set button
    def create_navigation_buttons(self, container):
        self.nav_frame = tk.Frame(container)
        self.nav_frame.pack(side="top", fill="x")

        # Function button
        overview_button = tk.Button(self.nav_frame, text="Overview", command=lambda: self.show_frame(Overview))
        overview_button.pack(side="left")

        search_config_button = tk.Button(self.nav_frame, text="Search & Configuration",
                                         command=lambda: self.show_frame(SearchConfiguration))
        search_config_button.pack(side="left")

        # Administrator-specific button
        if self.user_type == "admin":
            user_management_button = tk.Button(self.nav_frame, text="User Management",
                                               command=lambda: self.show_frame(UserManagement))
            user_management_button.pack(side="left")

            stats_report_button = tk.Button(self.nav_frame, text="Stats & Reports",
                                            command=lambda: self.show_frame(StatsReport))
            stats_report_button.pack(side="left")

        # Logout and Exit button
        logout_button = tk.Button(self.nav_frame, text="Logout", command=self.logout)
        logout_button.pack(side="right")

        exit_button = tk.Button(self.nav_frame, text="Exit", command=self.on_closing)
        exit_button.pack(side="right")

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def logout(self):
        for frame in self.frames.values():
            frame.destroy()
        self.nav_frame.destroy()
        self.content_frame.destroy()
        self.container.destroy()

        self.user_type = None
        show_login(self)

    def on_closing(self):
        self.conn.close()
        self.destroy()
        
app = MainApp()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()

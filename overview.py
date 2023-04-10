import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import sqlite3

class Overview(tk.Frame):
    def __init__(self, parent, controller, username):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        welcome_label = tk.Label(self, text=f"Welcome to Inventory Management System!", font=("Arial", 18))
        welcome_label.pack(pady=10)

        stats_label = tk.Label(self, text="You can use the navigation buttons on the left bottom side to access different functions.", font=("Arial", 12))
        stats_label.pack(pady=10)

        # Separator
        separator1 = ttk.Separator(self, orient='horizontal')
        separator1.pack(fill='x', pady=5)

        user_guide_label = tk.Label(self, text="User Guide", font=("Arial", 10, "bold"))
        user_guide_label.pack(pady=10)

        guide_text = """You can add, delete, and modify goods in "Search & Configuration"

You can add, delete, and modify users in "User Management"

You can export stats graph and export CSV in "Stats & Reports"
"""
        guide_label = tk.Label(self, text=guide_text, font=("Arial", 10), justify=tk.LEFT)
        guide_label.pack(pady=10)

        # Separator
        separator2 = ttk.Separator(self, orient='horizontal')
        separator2.pack(fill='x', pady=5)

        self.create_widgets()

    def create_widgets(self):
        # Connect to the database
        conn = sqlite3.connect("inventory_management.db")
        cursor = conn.cursor()

        # Get the total number of goods in the inventory
        cursor.execute("SELECT SUM(stocks) FROM product")
        total_goods = cursor.fetchone()[0]

        if total_goods is None:
            total_goods = 0

        # Get daily, weekly, and monthly sales info
        today = datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d")
        month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        cursor.execute("SELECT SUM(quantity) FROM salestats WHERE date >= ?", (today,))
        daily_sales = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(quantity) FROM salestats WHERE date >= ?", (week_ago,))
        weekly_sales = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(quantity) FROM salestats WHERE date >= ?", (month_ago,))
        monthly_sales = cursor.fetchone()[0] or 0

        # Get the product data
        cursor.execute("SELECT * FROM product")
        product_data = cursor.fetchall()

        # Close the database connection
        conn.close()

        label_style = {"bg": "#dfe3ee", "font": ("Helvetica", 16)}

        # Create a frame to hold the summary labels
        summary_frame = tk.Frame(self, bg="#dfe3ee")
        summary_frame.pack(pady=20, padx=20, anchor="w", fill="x")

        # Display the total number of goods
        total_goods_label = tk.Label(summary_frame, text=f"Total number of goods: {total_goods}", **label_style)
        total_goods_label.grid(row=0, column=0, padx=20, pady=20)

        # Display daily, weekly, and monthly sales info
        daily_sales_label = tk.Label(summary_frame, text=f"Daily sales: {daily_sales}", **label_style)
        daily_sales_label.grid(row=0, column=1, padx=20, pady=20)

        weekly_sales_label = tk.Label(summary_frame, text=f"Weekly sales: {weekly_sales}", **label_style)
        weekly_sales_label.grid(row=0, column=2, padx=20, pady=20)

        monthly_sales_label = tk.Label(summary_frame, text=f"Monthly sales: {monthly_sales}", **label_style)
        monthly_sales_label.grid(row=0, column=3, padx=20, pady=20)

        # Create a frame to hold the product table
        table_frame = tk.Frame(self, bg="#dfe3ee")
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Create the product table
        columns = ("product_id", "product_name", "product_category", "product_price", "stocks")
        product_table = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Configure the table headings
        for col in columns:
            product_table.heading(col, text=col)

        # Insert the product data
        for row in product_data:
            product_table.insert('', 'end', values=row)

        # Pack the table
        product_table.pack(fill="both", expand=True)


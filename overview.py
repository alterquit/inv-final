import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import sqlite3


class Overview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#dfe3ee")
        self.controller = controller

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



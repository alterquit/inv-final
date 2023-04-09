import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StatsReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Stats & Reports", font=("Helvetica", 18))
        title.pack(pady=10)

        sales_button = tk.Button(self, text="Generate Sales Report", command=self.generate_sales_report)
        sales_button.pack(pady=10)

        supplier_button = tk.Button(self, text="Generate Supplier Report", command=self.generate_supplier_report)
        supplier_button.pack(pady=10)

    def generate_sales_report(self):
        self.show_graph("Sales Report", self.get_sales_data())

    def generate_supplier_report(self):
        self.show_graph("Supplier Report", self.get_supplier_data())

    def get_sales_data(self):
        # Replace with your actual data retrieval method
        sample_sales_data = {
            "Product A": 150,
            "Product B": 200,
            "Product C": 300
        }
        return sample_sales_data

    def get_supplier_data(self):
        # Replace with your actual data retrieval method
        sample_supplier_data = {
            "Supplier A": 100,
            "Supplier B": 250,
            "Supplier C": 400
        }
        return sample_supplier_data

    def show_graph(self, title, data):
        figure = Figure(figsize=(6, 5), dpi=100)
        plot = figure.add_subplot(1, 1, 1)

        x = list(data.keys())
        y = list(data.values())
        plot.bar(x, y)

        plot.set_title(title)
        plot.set_xlabel("Categories")
        plot.set_ylabel("Values")

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack()


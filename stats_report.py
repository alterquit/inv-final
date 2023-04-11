import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StatsReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.create_widgets()
        self.current_chart = None
        self.export_button = None

    def create_widgets(self):
        title = tk.Label(self, text="Stats & Reports", font=("Helvetica", 18))
        title.pack(pady=10)

        sales_button = tk.Button(self, text="Generate Sales Report", command=self.generate_sales_report)
        sales_button.pack(pady=10)

        supplier_button = tk.Button(self, text="Generate Supplier Report", command=self.generate_supplier_report)
        supplier_button.pack(pady=10)

    def generate_sales_report(self):
        data = self.get_sales_data()
        self.show_graph("Sales Report", data)

    def generate_supplier_report(self):
        data = self.get_supplier_data()
        self.show_graph("Supplier Report", data)

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
        if self.current_chart is not None:
            self.current_chart.get_tk_widget().pack_forget()  # Remove the old chart from the window
            self.export_button.pack_forget()  # Remove the old export button from the window

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

        self.current_chart = canvas  # Store the new chart for future removal

        self.export_button = tk.Button(self, text="Export Chart", command=lambda: self.export_chart(canvas))
        self.export_button.pack(pady=10)

    def export_chart(self, canvas):
        filetypes = (("PNG Image", "*.png"), ("All Files", "*.*"))
        filename = asksaveasfilename(defaultextension=".png", filetypes=filetypes)

        if filename:
            canvas.figure.savefig(filename)
            tk.messagebox.showinfo("Export Successful", "Chart has been exported successfully.")





import tkinter as tk

class SearchConfiguration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.products = {}  # Replace with your actual data source
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Search & Configuration", font=("Helvetica", 18))
        title.pack(pady=10)

        search_label = tk.Label(self, text="Search by keyword:")
        search_label.pack()
        self.search_entry = tk.Entry(self)
        self.search_entry.pack()

        search_button = tk.Button(self, text="Search", command=self.search_product)
        search_button.pack(pady=10)

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        add_product_label = tk.Label(self, text="Add Product:")
        add_product_label.pack()
        self.add_product_entry = tk.Entry(self)
        self.add_product_entry.pack()

        add_button = tk.Button(self, text="Add", command=self.add_product)
        add_button.pack(pady=10)

        update_product_label = tk.Label(self, text="Update Product:")
        update_product_label.pack()
        self.update_product_old_entry = tk.Entry(self)
        self.update_product_old_entry.pack()
        self.update_product_new_entry = tk.Entry(self)
        self.update_product_new_entry.pack()

        update_button = tk.Button(self, text="Update", command=self.update_product)
        update_button.pack(pady=10)

        delete_product_label = tk.Label(self, text="Delete Product:")
        delete_product_label.pack()
        self.delete_product_entry = tk.Entry(self)
        self.delete_product_entry.pack()

        delete_button = tk.Button(self, text="Delete", command=self.delete_product)
        delete_button.pack(pady=10)

    def search_product(self):
        keyword = self.search_entry.get()
        results = [product for product in self.products.keys() if keyword.lower() in product.lower()]
        self.result_label['text'] = 'Results: ' + ', '.join(results)

    def add_product(self):
        product_name = self.add_product_entry.get()
        if product_name not in self.products:
            self.products[product_name] = {'details': 'Sample Details'}  # Replace with actual data
            self.add_product_entry.delete(0, 'end')
            self.result_label['text'] = f"Added {product_name}"
        else:
            self.result_label['text'] = f"{product_name} already exists"

    def update_product(self):
        old_name = self.update_product_old_entry.get()
        new_name = self.update_product_new_entry.get()
        if old_name in self.products:
            self.products[new_name] = self.products.pop(old_name)
            self.update_product_old_entry.delete(0, 'end')
            self.update_product_new_entry.delete(0, 'end')
            self.result_label['text'] = f"Updated {old_name} to {new_name}"
        else:
            self.result_label['text'] = f"{old_name} not found"

    def delete_product(self):
        product_name = self.delete_product_entry.get()
        if product_name in self.products:
            del self.products[product_name]
            self.delete_product_entry.delete(0, 'end')
            self.result_label['text'] = f"Deleted {product_name}"
        else:
            self.result_label['text'] = f"{product_name} not found"

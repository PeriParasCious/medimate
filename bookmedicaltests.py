import tkinter as tk
from tkinter import ttk
from login import LoginPage

class MedicalTests:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x853")
        self.root.title("Book medical Tests")

        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Create labels
        self.book_medical_test_label = ttk.Label(self.main_container, text="Book Medical Test", font=("Helvetica", 16))
        self.book_medical_test_label.pack(pady=20)

        self.book_medical_test_label.bind('<Button-1>', self.logout)

        self.book_medicines_label = ttk.Label(self.main_container, text="Book Medicines", font=("Helvetica", 16))
        self.book_medicines_label.pack(pady=20)

        self.buy_diagnostic_devices_label = ttk.Label(self.main_container, text="Buy Diagnostic Devices", font=("Helvetica", 16))
        self.buy_diagnostic_devices_label.pack(pady=20)

        # Logout button
        self.logout_button = ttk.Button(self.main_container, text="Logout", command=self.logout)
        self.logout_button.pack(pady=20)

    def logout(self):
        self.root.destroy()
        app = LoginPage()
        app.run()

def main():
    root = tk.Tk()
    app = MedicalTests(root)
    root.mainloop()

if __name__ == "__main__":
    main()
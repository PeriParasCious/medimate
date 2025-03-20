import tkinter as tk
from tkinter import messagebox, simpledialog
import pymysql
import tkcalendar  # Make sure to install this with: pip install tkcalendar
from datetime import datetime

class ProfileUpdateApp:
    def __init__(self, master):
        self.master = master
        master.title("Profile Update")
        master.geometry("400x650")

        # Create and set up form fields
        self.create_form_fields()

        # Create submit button
        submit_button = tk.Button(
            master, 
            text="Update Profile", 
            command=self.update_profile,
            bg="#4CAF50",
            fg="white"
        )
        submit_button.pack(pady=20)

    def create_form_fields(self):
        
        # Username
        tk.Label(self.master, text="Username").pack(pady=(10,0))
        self.name_entry = tk.Entry(self.master, width=30)
        self.name_entry.pack(pady=5)
        
        # Name
        tk.Label(self.master, text="Name").pack(pady=(10,0))
        self.name_entry = tk.Entry(self.master, width=30)
        self.name_entry.pack(pady=5)

        # Phone Number
        tk.Label(self.master, text="Phone Number").pack(pady=(10,0))
        self.phone_entry = tk.Entry(self.master, width=30)
        self.phone_entry.pack(pady=5)

        # Email
        tk.Label(self.master, text="Email").pack(pady=(10,0))
        self.email_entry = tk.Entry(self.master, width=30)
        self.email_entry.pack(pady=5)
 
        # Date of Birth (with Calendar Button)
        tk.Label(self.master, text="Date of Birth").pack(pady=(10,0))
        
        # Frame to hold date of birth entry and calendar button
        dob_frame = tk.Frame(self.master)
        dob_frame.pack(pady=5)

        # Date of Birth Entry (Read-only)
        self.dob_entry = tk.Entry(dob_frame, width=20, state='readonly')
        self.dob_entry.pack(side=tk.LEFT, padx=(0,10))

        # Calendar Button
        calendar_button = tk.Button(
            dob_frame, 
            text="Select Date", 
            command=self.open_calendar
        )
        calendar_button.pack(side=tk.LEFT)

        # Age (Read-only)
        tk.Label(self.master, text="Age").pack(pady=(10,0))
        self.age_entry = tk.Entry(self.master, width=30, state='readonly')
        self.age_entry.pack(pady=5)

        # Address
        tk.Label(self.master, text="Address").pack(pady=(10,0))
        self.address_entry = tk.Entry(self.master, width=30)
        self.address_entry.pack(pady=5)

    def open_calendar(self):
        # Create a top-level window for the calendar
        top = tk.Toplevel(self.master)
        top.title("Select Date of Birth")
        
        # Create calendar widget
        cal = tkcalendar.Calendar(
            top, 
            selectmode='day',
            date_pattern='y-mm-dd'
        )
        cal.pack(padx=10, pady=10)

        def on_date_select():
            # Get selected date
            selected_date = cal.get_date()
            
            # Update date of birth entry
            self.dob_entry.config(state='normal')
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(0, selected_date)
            self.dob_entry.config(state='readonly')

            # Calculate and update age
            self.calculate_age()

            # Close the calendar window
            top.destroy()

        # Select Date Button
        select_button = tk.Button(
            top, 
            text="Select", 
            command=on_date_select
        )
        select_button.pack(pady=10)
    
    def calculate_age(self):
        try:
            # Parse the date of birth
            dob = datetime.strptime(self.dob_entry.get(), "%Y-%m-%d")
            today = datetime.now()
            
            # Calculate age
            age = today.year - dob.year
            
            # Adjust age if birthday hasn't occurred this year
            if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
                age -= 1
            
            # Update age entry
            self.age_entry.config(state='normal')
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, str(age))
            self.age_entry.config(state='readonly')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please select a valid date")
            self.dob_entry.config(state='normal')
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.config(state='readonly')
            self.age_entry.config(state='normal')
            self.age_entry.delete(0, tk.END)
            self.age_entry.config(state='readonly')

    def update_profile(self):
        # Collect form data
        profile_data = {
            "Name": self.name_entry.get(),
            "Phone Number": self.phone_entry.get(),
            "Email": self.email_entry.get(),
            "Date of Birth": self.dob_entry.get(),
            "Age": self.age_entry.get(),
            "Address": self.address_entry.get()
        }

        # Validate inputs
        if not all(profile_data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Here you would typically save to a database or file
        # For now, we'll just show a message box
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123@S',                                     database='medimate')
        cur = connection.cursor()
        sql = "update medimate set(dob,age,address) values(%s,%s,%s)"
        cur.execute(sql, (profile_data["Date of Birth"], self.dob_entry.get(), self.age_entry.get(), self.address_entry.get()))
        connection.commit()
        messagebox.showinfo("Success", "Profile Updated Successfully")

def main():
    root = tk.Tk()
    app = ProfileUpdateApp(root)
    root.mainloop()

if __name__ == "__main__":  # Fixed this line too
    main()
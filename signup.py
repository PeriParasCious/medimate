from logging import root
import tkinter as tk
from tkinter import ttk
import os
import sys
import pymysql
from tkinter import PhotoImage


    

class SignupPage:
    def __init__(self):
        
        self.window = tk.Tk()
        
        self.window.title("Sign Up")
        
        self.window.geometry("1280x853")
        

       
        # Configure grid to center the form
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        

        
         # Create the labels and entry fields
        fields = [
            ("Name:", "name"),
            ("Username:","username"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Password:", "password", "*")
            ]
         
        #background Image
        self.background_image = PhotoImage(file=r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\Signup.png")
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.frame = tk.Frame(self.window, bg='white')
        self.frame.pack(pady=310)
        

       

       
        
        self.entries = {}
        for i, field in enumerate(fields):
            label_text = field[0]
            field_name = field[1]
            show_char = field[2] if len(field) > 2 else ""
            
            label = tk.Label(self.frame, text=label_text)
            label.grid(row=i, column=0, padx=7, pady=1, sticky="e")
            
            entry = tk.Entry(self.frame, show=show_char)
            entry.grid(row=i, column=1, padx=7, pady=1)
            self.entries[field_name] = entry

            
            

        # Error message label
        self.error_label = tk.Label(self.frame, text="", fg="red")
        self.error_label.grid(row=len(fields), column=0, columnspan=2, pady=1)
        
        # Submit button
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.submit_form,bg="lightgreen")
        self.submit_button.grid(row=len(fields)+1, column=0, columnspan=2, pady=1)
        
        # Back to login button
        self.back_button = tk.Button(self.frame, text="Back to Login", command=self.back_to_login,bg="lightgreen")
        self.back_button.grid(row=len(fields)+2, column=0, columnspan=2, pady=1)

    def submit_form(self):
        connection = pymysql.connect(host='localhost',user='root',password='123@S',database='medimate')
        cur=connection.cursor()
        sql="insert into login(name,username,phone,email,password) values(%s,%s,%s,%s,%s)"
        cur.execute(sql,(self.entries["name"].get(),self.entries["username"].get(),self.entries["phone"].get(),self.entries["email"].get(),self.entries["password"].get()))
        connection.commit()
        
         

        # Process the form data (e.g., send to a database)
        # Clear the entry fields
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            
        # Display success message and return to login
        self.error_label.config(text="Signup successful! Please login.", fg="green")
        self.window.after(2000, self.back_to_login)

    def back_to_login(self):
        self.window.destroy()
        # Run the login script
        from login import LoginPage
        login_page = LoginPage()

    def run(self):
        self.window.mainloop()
        

        if __name__ == "__main__":
            app = SignupPage()
            app.run()
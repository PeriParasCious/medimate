import subprocess
import tkinter as tk
import tkinter.messagebox as messagebox
import os
import sys
import pymysql
from DocDash import DoctorDashboard
from u_dash import NavigationApp

class LoginPage:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("1280x853")
        self.window.configure(bg="white")

        # Add a logo
        self.logo = tk.PhotoImage(file=r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png")  # Update the path to your logo file

        self.logo_label = tk.Label(self.window, image=self.logo, bg="white")
        self.logo_label.pack(pady=50)
        
        # Create the frame for the login form
        self.frame = tk.Frame(self.window, bg="#12962b",width=1920 ,height=1080)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the label and entry for the ID
        self.id_label = tk.Label(self.frame, text="Username:", bg="lightgreen")
        self.id_label.grid(row=0, column=0, padx=5, pady=2)
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=2)
        

        # Create the label and entry for the password
        self.pass_label = tk.Label(self.frame, text="Password:", bg="lightgreen")
        self.pass_label.grid(row=2, column=0, padx=5, pady=5)
        self.pass_entry = tk.Entry(self.frame, show="*")
        self.pass_entry.grid(row=2, column=1, padx=5, pady=5)

        # Login button
        self.login_button = tk.Button(self.frame, text="Login", bg="lightgreen", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Create the signup button
        self.signup_button = tk.Button(self.frame, text="Not registered? Signup", 
                                     bg="lightgreen", command=self.open_signup)
        self.signup_button.grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        user_id = self.id_entry.get()
        password = self.pass_entry.get()
        if user_id == "" and password == "": 
         messagebox.showerror("Error!", "All fields are Required")
        elif user_id == "drishti" and password == "12345":
            self.window.destroy()  # Close the login window
            root = tk.Tk()
            app = DoctorDashboard(root)  # Pass root
            root.mainloop()
        elif user_id == "porus" and password == "1245":
            self.window.destroy()  # Close the login window
            root = tk.Tk()
            app = DoctorDashboard(root)  # Pass root
            root.mainloop()
        elif user_id == "arjya" and password == "123":
            self.window.destroy()  # Close the login window
            root = tk.Tk()
            app = DoctorDashboard(root)  # Pass root
            root.mainloop()
        elif user_id == "rushikesh" and password == "1234":
            self.window.destroy()  # Close the login window
            root = tk.Tk()
            app = DoctorDashboard(root)  # Pass root
            root.mainloop()
        else:
            try:
             connection = pymysql.connect(host='localhost',user='root',password='123@S',database='medimate')
             cur=connection.cursor()
             cur.execute("Select * from login where username=%s and password=%s",(user_id,password))
             row=cur.fetchone()
             if row==None:
                messagebox.showerror("Error!", "Invalid ID or Password")
             else:
                self.window.destroy()  # Close the login window
                root = tk.Tk()
                user_name = row[0]
                username=row[1]
                subprocess.run(["python", "userdashboard.py", user_name])
                subprocess.run(["python", "patientui2.py", username])
                app = NavigationApp(root)  # Pass root
                root.mainloop()
                connection.close()
            except Exception as e:
             messagebox.showerror("Error", f"{e}")


    def open_signup(self):
        self.window.destroy()  # Close login window
        # os.system(f'{sys.executable} signup.py')  # Run the signup script
        from signup import SignupPage
        signup_page = SignupPage()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.run()

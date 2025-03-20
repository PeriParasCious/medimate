import sys
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import pymysql 
from bookappointment import AppointmentApp

class NavigationApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x853")
        self.root.title("User DashBoard")

        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Load background image
        self.background_image = PhotoImage(file=r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\Ud1.png")
        
        # Create a label to hold the background image
        self.background_label = tk.Label(self.main_container, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create menu button (three lines)
        self.menu_frame = ttk.Frame(self.main_container)
        self.menu_frame.pack(anchor='ne', padx=10, pady=10)
        
        # Style configuration with thicker borders
        self.style = ttk.Style()
        self.style.configure('Thick.TLabelframe', borderwidth=0, relief='flat')

        # Welcome label
        if len(sys.argv) > 1:
            user_name = sys.argv[1]
        else:
            user_name = "Guest"
        welcome_label = tk.Label(self.main_container, text=f"Welcome, {user_name}!", background="white", font=("Helvetica", 30), anchor="center")
        welcome_label.place(relx=0.25, rely=0.30, anchor='center')
        
        # Create two main boxes with thicker borders
        # Left box - Appoint Doctor
        appoint_label = ttk.Label(self.main_container, text="Book Doctor Appointment", background="#e1f0da", font=("Helvetica", 16), anchor="center", borderwidth=2, relief="solid")
        appoint_label.place(relx=0.25, rely=0.45, anchor='center', width=250, height=50)
        
        # Bind click event to the appoint doctor label
        appoint_label.bind('<Button-1>', self.open_bookapp)

        # Lower Box - Book Medical Tests
        medtests_label = ttk.Label(self.main_container, text="Book Medical Tests", background="#e1f0da", font=("Helvetica", 16), anchor="center", borderwidth=2, relief="solid")
        medtests_label.place(relx=0.25, rely=0.65, anchor='center', width=250, height=50)

        # View Profile
        profile_label = ttk.Label(self.main_container, text="View Profile", background="#e1f0da", font=("Helvetica", 16), anchor="center", borderwidth=2, relief="solid")
        profile_label.place(relx=0.25, rely=0.85, anchor='center', width=250, height=50)
        profile_label.bind('<Button-1>', lambda event: self.open_patientui())

        # Logout
        logout_label = ttk.Label(self.main_container, text="Logout", background="#e1f0da", foreground="red", font=("Helvetica", 12), anchor="center", borderwidth=2, relief="solid")
        logout_label.place(relx=0.25, rely=0.95, anchor='center', width=250, height=50)
        logout_label.bind('<Button-1>', lambda event: self.open_login())
       
        # Last appointment
        last_appointment_label = ttk.Label(self.main_container, text="Last Appointment", background="#e1f0da", font=("Helvetica", 16), anchor="center", borderwidth=2, relief="solid")
        last_appointment_label.place(relx=0.75, rely=0.45, anchor='center', width=250, height=50)

        # Upcoming appointment
        upcoming_appointment_label = ttk.Label(self.main_container, text="Upcoming Appointment", background="#e1f0da", font=("Helvetica", 16), anchor="center", borderwidth=2, relief="solid")
        upcoming_appointment_label.place(relx=0.75, rely=0.75, anchor='center', width=250, height=50)

    def toggle_menu(self, event):
        # Display popup menu at button location
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def open_bookapp(self, event):
        # Close the current window and open the AppointmentApp
        self.root.destroy()  # Close the current window
        new_root = tk.Tk()  # Create a new window for the AppointmentApp
        app = AppointmentApp(new_root)  # Instantiate the AppointmentApp
        new_root.mainloop()  # Start the new window's main loop

    def open_login(self):
        self.root.destroy()  # Close current window
        from login import LoginPage
        login_window = tk.Tk()
        app = LoginPage(login_window)  # Assuming LoginPage takes a root window parameter
        login_window.mainloop()

    def open_patientui(self):
        self.root.destroy()
        from patientui import PatientProfile
        profile_window = tk.Tk()
        app = PatientProfile(profile_window)
        profile_window.mainloop()  # Add mainloop call to start event loop

def main():
    root = tk.Tk()
    app = NavigationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
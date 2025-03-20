import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import tkinter.messagebox as messagebox

class DoctorDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor's Dashboard - Medimate")
        self.root.state('zoomed')  # Maximize window
        
        # Configure style and set white background
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')
        style.configure('TLabelframe', background='white')
        style.configure('TLabelframe.Label', background='white')
        style.configure('Green.TFrame', background='#e8f5e9')  # Light green background
        style.configure('Orange.TFrame', background='#fff3e0')  # Light orange background
        
        # Configure button styles
        style.configure('Accept.TButton',
                       background='#4CAF50',  # Green
                       font=('Helvetica', 9, 'bold'))
        
        style.configure('Decline.TButton',
                       background='#F44336',  # Red
                       font=('Helvetica', 9, 'bold'))
        
        # Logout button 
        style.configure('Logout.TButton',
                       background='white',
                       foreground='#FF0000',  # Red text
                       font=('Helvetica', 10, 'bold'))
        
        style.map('Accept.TButton',
                 background=[('active', '#45a049')])  # Darker green when clicked
        
        style.map('Decline.TButton',
                 background=[('active', '#da190b')])  # Darker red when clicked
        
        style.map('Logout.TButton',
                 background=[('active', '#f8f8f8')])  # Slightly grey when clicked
        
        # Set root window background
        self.root.configure(bg='white')
        
        # Create main containers
        self.create_header()
        self.create_main_content()
        
    def create_header(self):
        header = ttk.Frame(self.root, padding="10", style='TFrame')
        header.pack(fill=tk.X)
        
        # Left section for logout button
        left_section = ttk.Frame(header, style='TFrame')
        left_section.pack(side=tk.LEFT, padx=(0, 20))
        
        # Logout button
        logout_btn = ttk.Button(left_section, 
                              text="Logout",
                              style='Logout.TButton',
                              command=self.handle_logout)
        logout_btn.pack(side=tk.LEFT)
        
        # Logo and title
        title_label = ttk.Label(header, text="MEDIMATE", font=('Helvetica', 24, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Date and time
        date_label = ttk.Label(header, 
                             text=datetime.now().strftime("%B %d, %Y"),
                             font=('Helvetica', 12))
        date_label.pack(side=tk.RIGHT)
    
    def handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()


    # [Rest of the class methods remain the same...]
    def create_main_content(self):
        main_container = ttk.Frame(self.root, padding="10", style='TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create three columns
        self.create_left_column(main_container)
        self.create_middle_column(main_container)
        self.create_right_column(main_container)
        
    def create_left_column(self, parent):
        left_frame = ttk.Frame(parent, padding="5", style='TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Ongoing Patients Section
        ongoing_label = ttk.Label(left_frame, text="Ongoing Patients",
                                font=('Helvetica', 12, 'bold'))
        ongoing_label.pack(fill=tk.X, pady=5)
        
        # Ongoing Patients List
        ongoing_frame = ttk.Frame(left_frame, style='Green.TFrame')
        ongoing_frame.pack(fill=tk.BOTH, expand=True)
        
        for i in range(1):
            patient_frame = ttk.Frame(ongoing_frame, padding="5", style='TFrame')
            patient_frame.pack(fill=tk.X, pady=2)
            ttk.Label(patient_frame, 
                     text=f"Patient #{i+1}",
                     font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT)
            ttk.Label(patient_frame,
                     text="In Progress",
                     foreground='green').pack(side=tk.RIGHT)
        
        # Upcoming Patients Section
        upcoming_label = ttk.Label(left_frame, text="Upcoming Patients",
                                 font=('Helvetica', 12, 'bold'))
        upcoming_label.pack(fill=tk.X, pady=5)
        
        # Upcoming Patients List
        upcoming_frame = ttk.Frame(left_frame, style='Orange.TFrame')
        upcoming_frame.pack(fill=tk.BOTH, expand=True)
        
        for i in range(2):
            patient_frame = ttk.Frame(upcoming_frame, padding="5", style='TFrame')
            patient_frame.pack(fill=tk.X, pady=2)
            ttk.Label(patient_frame,
                     text=f"Patient #{i+4}",
                     font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT)
            ttk.Label(patient_frame,
                     text="Waiting",
                     foreground='orange').pack(side=tk.RIGHT)
    
    def create_middle_column(self, parent):
        middle_frame = ttk.Frame(parent, padding="5", style='TFrame')
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Patient Details Section
        details_frame = ttk.LabelFrame(middle_frame, text="Patient Details",
                                     padding="10")
        details_frame.pack(fill=tk.X, pady=5)
        
        # Create grid for patient details
        details = [
            ("Name:", "John Doe"),
            ("Age:", "45"),
            ("Contact:", "+1 234 567 8900"),
            ("Last Visit:", "Jan 15, 2025")
        ]
        
        for i, (label, value) in enumerate(details):
            ttk.Label(details_frame, text=label).grid(row=i, column=0, pady=2, padx=5)
            ttk.Label(details_frame, text=value).grid(row=i, column=1, pady=2, padx=5)
        
        # Medical Notes Section
        notes_frame = ttk.LabelFrame(middle_frame, text="Prescription",
                                   padding="10")
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=15)
        self.notes_text.pack(fill=tk.BOTH, expand=True)
        
        save_notes_btn = ttk.Button(notes_frame, text="Save Prescription",
                                  command=self.save_notes)
        save_notes_btn.pack(pady=5)
        
    def create_right_column(self, parent):
        right_frame = ttk.Frame(parent, padding="5", style='TFrame')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Appointment Requests Section
        requests_frame = ttk.LabelFrame(right_frame, text="Appointment Requests",
                                      padding="10")
        requests_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        for i in range(3):
            request_frame = ttk.Frame(requests_frame, padding="5", style='TFrame')
            request_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(request_frame,
                     text=f"New Patient #{i+1}",
                     font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(request_frame,
                     text=f"Requested: Feb {10+i}, 2025").pack(anchor=tk.W)
            
            btn_frame = ttk.Frame(request_frame, style='TFrame')
            btn_frame.pack(fill=tk.X, pady=2)
            ttk.Button(btn_frame, text="Accept",
                      style='Accept.TButton',
                      command=lambda x=i: self.handle_request(x, "accept")).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="Decline",
                      style='Decline.TButton',
                      command=lambda x=i: self.handle_request(x, "decline")).pack(side=tk.LEFT, padx=2)
        
        # Doctor's comments Section
        prescription_frame = ttk.Labelframe(right_frame, text="Doctor comments",
                                          padding="10")
        prescription_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.prescription_text = scrolledtext.ScrolledText(prescription_frame, height=10)
        self.prescription_text.pack(fill=tk.BOTH, expand=True)
        
        save_prescription_btn = ttk.Button(prescription_frame,
                                         text="Save Comments",
                                         command=self.save_prescription)
        save_prescription_btn.pack(pady=5)
    
    def save_notes(self):
        notes = self.notes_text.get("1.0", tk.END)
        messagebox.showinfo("Success", "Comments saved successfully!")
    
    def save_prescription(self):
        prescription = self.prescription_text.get("1.0", tk.END)
        messagebox.showinfo("Success", "Prescription saved successfully!")
    
    def handle_request(self, request_id, action):
        action_text = "accepted" if action == "accept" else "declined"
        messagebox.showinfo("Success",
                          f"Appointment request #{request_id+1} {action_text}!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DoctorDashboard(root)
    root.mainloop()
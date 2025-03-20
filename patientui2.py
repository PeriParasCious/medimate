import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pymysql

class PatientProfile:
    def __init__(self, root, username=None):
        self.root = root
        self.root.title("Patient Profile")
        self.root.state('zoomed')  # Maximize window
        
        # Store the username for database queries
        self.username = username if username else (sys.argv[1] if len(sys.argv) > 1 else None)
        
        # Configure styles
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Section.TLabelframe.Label', font=('Helvetica', 12, 'bold'))
        style.configure('Content.TLabel', font=('Helvetica', 10))
        
        # Main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header(main_frame)
        
        # Create two columns
        self.left_frame = ttk.Frame(main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Create sections
        self.create_personal_info(self.left_frame)
        self.create_contact_info(self.left_frame)
        self.create_medical_records(right_frame)
        self.create_doctors_comments(right_frame)
        
        # Add update profile button at right bottom of left frame
        self.create_update_button()
        
        # Load data from database
        if self.username:
            self.load_user_data()
        else:
            messagebox.showwarning("No Username", "No username provided. Unable to load user data.")
        
    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="Patient Profile",
                 style='Header.TLabel').pack(side=tk.LEFT)
        
        # Save Changes button removed as updates will be handled on a different page
    
    def create_personal_info(self, parent):
        self.personal_frame = ttk.LabelFrame(parent,
                             text="Personal Information",
                             style='Section.TLabelframe',
                             padding="10")
        self.personal_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grid layout for personal info
        labels = ['Name:', 'Age:', 'Birth Date:', 'Address:']
        for i, label in enumerate(labels):
            ttk.Label(self.personal_frame,
                     text=label,
                     style='Content.TLabel').grid(row=i, column=0,
                                                sticky=tk.W,
                                                pady=5,
                                                padx=5)
        
        # Entry widgets - set to readonly since updates are on another page
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(self.personal_frame, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        self.age_var = tk.StringVar()
        age_entry = ttk.Entry(self.personal_frame, textvariable=self.age_var)
        age_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Date picker for birth date
        self.birth_date = DateEntry(self.personal_frame,
                                  width=20,
                                  background='darkblue',
                                  foreground='white',
                                  borderwidth=2,
                                  state='readonly')
        self.birth_date.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Text widget for address - readonly
        self.address_text = tk.Text(self.personal_frame, height=3, width=30)
        self.address_text.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Configure grid column weights
        self.personal_frame.columnconfigure(1, weight=1)
        return self.personal_frame
    
    def create_contact_info(self, parent):
        self.contact_frame = ttk.LabelFrame(parent,
                             text="Contact Information",
                             style='Section.TLabelframe',
                             padding="10")
        self.contact_frame.pack(fill=tk.X)
        
        # Grid layout for contact info
        labels = ['Phone Number:', 'Email:']
        for i, label in enumerate(labels):
            ttk.Label(self.contact_frame,
                     text=label,
                     style='Content.TLabel').grid(row=i, column=0,
                                                sticky=tk.W,
                                                pady=5,
                                                padx=5)
        
        # Entry widgets - set to readonly since updates are on another page
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(self.contact_frame, textvariable=self.phone_var)
        phone_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        self.email_var = tk.StringVar() 
        email_entry = ttk.Entry(self.contact_frame, textvariable=self.email_var)
        email_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Configure grid column weights
        self.contact_frame.columnconfigure(1, weight=1)
        return self.contact_frame
    
    def create_update_button(self):
        # Create a frame at the bottom of left frame for the update button
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add update profile button aligned to the right
        update_label = ttk.Label(button_frame, text="Update Profile", 
                              background="#e1f0da", foreground="red", 
                              font=("Helvetica", 12), anchor="center", 
                              borderwidth=2, relief="solid")
        # Place at the right of the frame
        update_label.pack(side=tk.RIGHT, padx=10, pady=10)
        update_label.bind('<Button-1>', lambda event: self.open_updatepage())

    def create_medical_records(self, parent):
        frame = ttk.LabelFrame(parent,
                             text="Previous Medical Records",
                             style='Section.TLabelframe',
                             padding="10")
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Toolbar for medical records
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(toolbar,
                  text="Add Record",
                  command=self.add_record).pack(side=tk.LEFT)
        
        ttk.Button(toolbar,
                  text="Delete Selected",
                  command=self.delete_record).pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview for medical records
        columns = ('Date', 'Diagnosis', 'Treatment', 'Doctor')
        self.records_tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=100)
        
        self.records_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame,
                                orient=tk.VERTICAL,
                                command=self.records_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.records_tree.configure(yscrollcommand=scrollbar.set)
    
    def create_doctors_comments(self, parent):
        frame = ttk.LabelFrame(parent,
                             text="Doctor's Comments",
                             style='Section.TLabelframe',
                             padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget for comments
        self.comments_text = scrolledtext.ScrolledText(frame, height=10)
        self.comments_text.pack(fill=tk.BOTH, expand=True)

    def load_user_data(self):
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='123@S',  # Your MySQL password
                database='medimate'  # Your database name
            )
            
            try:
                with connection.cursor() as cursor:
                    # Execute query to fetch user data
                    query = "SELECT name, username, phone, email, password, dob, age, address FROM login WHERE username = %s"
                    cursor.execute(query, (self.username,))
                    user_data = cursor.fetchone()
                    
                    if user_data:
                        # Populate personal information fields
                        self.name_var.set(user_data[0])  # name
                        self.age_var.set(user_data[6])   # age
                        
                        # Handle date format
                        if user_data[5]:  # dob
                            try:
                                self.birth_date.set_date(user_data[5])
                            except Exception as e:
                                messagebox.showwarning("Date Format Error", f"Could not set birth date: {e}")
                        
                        # Set address
                        if user_data[7]:  # address
                            self.address_text.delete('1.0', tk.END)
                            self.address_text.insert('1.0', user_data[7])
                            self.address_text.config(state='disabled')  # Make readonly
                        
                        # Populate contact information fields
                        self.phone_var.set(user_data[2])  # phone
                        self.email_var.set(user_data[3])  # email
                        
                        #OFF BECAUSE TABLE DOESNT EXIST
                        # # Load medical records
                        # self.load_medical_records()
                        
                        # Load doctor's comments
                        self.load_doctor_comments()
                    else:
                        messagebox.showinfo("User Not Found", f"No user data found for username: {self.username}")
            
            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Error fetching data: {e}")
            
            finally:
                connection.close()
                
        except pymysql.Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")
    
    # def load_medical_records(self):
    #     try:
    #         connection = pymysql.connect(
    #             host='localhost',
    #             user='root',
    #             password='Drishti2005@',
    #             database='medimate'
    #         )
            
    #         try:
    #             with connection.cursor() as cursor:
    #                 query = "SELECT date, diagnosis, treatment, doctor FROM medical_records WHERE username = %s"
    #                 cursor.execute(query, (self.username,))
    #                 records = cursor.fetchall()
                    
    #                 # Clear existing records
    #                 for item in self.records_tree.get_children():
    #                     self.records_tree.delete(item)
                    
    #                 # Add records to treeview
    #                 for record in records:
    #                     self.records_tree.insert('', 'end', values=record)
            
    #         except pymysql.Error as e:
    #             messagebox.showwarning("Records Error", f"Failed to load medical records: {e}")
            
    #         finally:
    #             connection.close()
                
    #     except pymysql.Error as e:
    #         messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")
    
    def load_doctor_comments(self):
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='123@S',
                database='medimate'
            )
            
            try:
                with connection.cursor() as cursor:
                    query = "SELECT comments FROM doc_replies WHERE username = %s"
                    cursor.execute(query, (self.username,))
                    result = cursor.fetchone()
                    
                    if result:
                        self.comments_text.delete('1.0', tk.END)
                        self.comments_text.insert('1.0', result[0])
                        self.comments_text.config(state='disabled')  # Make readonly
            
            except pymysql.Error as e:
                messagebox.showwarning("Comments Error", f"Failed to load doctor comments: {e}")
            
            finally:
                connection.close()
                
        except pymysql.Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")
    
    def open_updatepage(self):
        self.root.destroy()
        from updateprofile import ProfileUpdateApp
        root = tk.Tk()
        app = ProfileUpdateApp(root, self.username)
        root.mainloop()
    
    def add_record(self):
        # This would typically open a dialog to add a new record
        # For now, we'll just add a sample record
        self.records_tree.insert('', 'end', values=(
            datetime.now().strftime("%Y-%m-%d"),
            "Sample Diagnosis",
            "Sample Treatment",
            "Dr. Smith"
        ))
    
    def delete_record(self):
        # Delete selected record
        selected_item = self.records_tree.selection()
        if selected_item:
            self.records_tree.delete(selected_item)

if __name__ == "__main__":
    root = tk.Tk()
    username = sys.argv[1] if len(sys.argv) > 1 else None
    app = PatientProfile(root, username)
    root.mainloop()
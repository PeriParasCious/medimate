import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pymysql  # For database connectivity
import sys

class PatientProfile:
    def __init__(self, root, user_id=None):
        self.root = root
        self.root.title("Patient Profile")
        self.root.state('zoomed')  # Maximize window
        
        # Store user ID for database queries
        if user_id is None and len(sys.argv) > 1:
            self.user_id = sys.argv[1]
        else:
            self.user_id = user_id if user_id else "1"  # Default to user ID 1 if none provided
        
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
        
        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Create sections
        self.create_personal_info(self.left_frame)
        self.create_contact_info(self.left_frame)
        self.create_medical_records(self.right_frame)
        self.create_doctors_comments(self.right_frame)
        
        # Create update profile button
        update_frame = ttk.Frame(self.left_frame)
        update_frame.pack(fill=tk.X, pady=10)
        
        update_button = ttk.Button(
            update_frame,
            text="Update Profile",
            command=self.open_updatepage
        )
        update_button.pack(side=tk.RIGHT)
        
        # Load user data from database
        self.load_user_data()
        
    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="Patient Profile",
                 style='Header.TLabel').pack(side=tk.LEFT)
        
        ttk.Button(header_frame,
                  text="Save Changes",
                  command=self.save_changes).pack(side=tk.RIGHT)
    
    def create_personal_info(self, parent):
        frame = ttk.LabelFrame(parent,
                             text="Personal Information",
                             style='Section.TLabelframe',
                             padding="10")
        frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grid layout for personal info
        labels = ['Name:', 'Age:', 'Birth Date:', 'Address:']
        for i, label in enumerate(labels):
            ttk.Label(frame,
                     text=label,
                     style='Content.TLabel').grid(row=i, column=0,
                                                sticky=tk.W,
                                                pady=5,
                                                padx=5)
        
        # Entry widgets
        self.name_var = tk.StringVar()
        ttk.Entry(frame,
                 textvariable=self.name_var).grid(row=0, column=1,
                                                 sticky=tk.EW,
                                                 pady=5,
                                                 padx=5)
        
        self.age_var = tk.StringVar()
        ttk.Entry(frame,
                 textvariable=self.age_var).grid(row=1, column=1,
                                                sticky=tk.EW,
                                                pady=5,
                                                padx=5)
        
        # Date picker for birth date
        self.birth_date = DateEntry(frame,
                                  width=20,
                                  background='darkblue',
                                  foreground='white',
                                  borderwidth=2,
                                  date_pattern='yyyy-mm-dd')
        self.birth_date.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Text widget for address
        self.address_text = tk.Text(frame, height=3, width=30)
        self.address_text.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Configure grid column weights
        frame.columnconfigure(1, weight=1)
        
        return frame
    
    def create_contact_info(self, parent):
        frame = ttk.LabelFrame(parent,
                             text="Contact Information",
                             style='Section.TLabelframe',
                             padding="10")
        frame.pack(fill=tk.X)
        
        # Grid layout for contact info
        labels = ['Phone Number:', 'Email:']
        for i, label in enumerate(labels):
            ttk.Label(frame,
                     text=label,
                     style='Content.TLabel').grid(row=i, column=0,
                                                sticky=tk.W,
                                                pady=5,
                                                padx=5)
        
        # Entry widgets
        self.phone_var = tk.StringVar()
        ttk.Entry(frame,
                 textvariable=self.phone_var).grid(row=0, column=1,
                                                  sticky=tk.EW,
                                                  pady=5,
                                                  padx=5)
        
        self.email_var = tk.StringVar()
        ttk.Entry(frame,
                 textvariable=self.email_var).grid(row=1, column=1,
                                                  sticky=tk.EW,
                                                  pady=5,
                                                  padx=5)
        
        # Configure grid column weights
        frame.columnconfigure(1, weight=1)
        
        return frame
    
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
        """Fetch user data from database and populate the form fields"""
        try:
            # Database connection parameters - replace with your actual database details
            connection = pymysql.connect(
                host='localhost',
                user='root',  # replace with your MySQL username
                password='',  # replace with your MySQL password
                database='healthcare_db'  # replace with your database name
            )
            
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            # Query to fetch personal and contact information
            query = """
            SELECT u.name, u.email, u.phone, p.birth_date, p.address
            FROM users u
            LEFT JOIN patient_profiles p ON u.id = p.user_id
            WHERE u.id = %s
            """
            
            cursor.execute(query, (self.user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                # Populate personal info
                self.name_var.set(user_data['name'])
                
                # Calculate age if birth date is available
                if user_data['birth_date']:
                    birth_date = user_data['birth_date']
                    today = datetime.now()
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    self.age_var.set(str(age))
                    
                    # Set date in the date picker
                    self.birth_date.set_date(birth_date)
                
                # Set address
                if user_data['address']:
                    self.address_text.delete('1.0', tk.END)
                    self.address_text.insert('1.0', user_data['address'])
                
                # Populate contact info
                self.phone_var.set(user_data['phone'])
                self.email_var.set(user_data['email'])
                
                # Now fetch medical records
                self.fetch_medical_records()
                
            else:
                messagebox.showinfo("Info", "No user data found for this ID")
            
            cursor.close()
            connection.close()
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Could not fetch user data: {e}")
    
    def fetch_medical_records(self):
        """Fetch medical records from database and populate the treeview"""
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='healthcare_db'
            )
            
            cursor = connection.cursor()
            
            # Query to fetch medical records
            query = """
            SELECT visit_date, diagnosis, treatment, doctor_name
            FROM medical_records
            WHERE patient_id = %s
            ORDER BY visit_date DESC
            """
            
            cursor.execute(query, (self.user_id,))
            records = cursor.fetchall()
            
            # Clear existing records
            for item in self.records_tree.get_children():
                self.records_tree.delete(item)
            
            # Insert new records
            for record in records:
                self.records_tree.insert('', 'end', values=record)
            
            cursor.close()
            connection.close()
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Could not fetch medical records: {e}")
    
    def save_changes(self):
        """Save user data to database"""
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='healthcare_db'
            )
            
            cursor = connection.cursor()
            
            # Get values from form
            name = self.name_var.get()
            birth_date = self.birth_date.get_date()
            address = self.address_text.get('1.0', tk.END).strip()
            phone = self.phone_var.get()
            email = self.email_var.get()
            
            # Update users table
            users_query = """
            UPDATE users
            SET name = %s, email = %s, phone = %s
            WHERE id = %s
            """
            cursor.execute(users_query, (name, email, phone, self.user_id))
            
            # Check if patient profile exists
            check_query = "SELECT user_id FROM patient_profiles WHERE user_id = %s"
            cursor.execute(check_query, (self.user_id,))
            profile_exists = cursor.fetchone()
            
            if profile_exists:
                # Update patient profile
                profile_query = """
                UPDATE patient_profiles
                SET birth_date = %s, address = %s
                WHERE user_id = %s
                """
                cursor.execute(profile_query, (birth_date, address, self.user_id))
            else:
                # Insert new patient profile
                profile_query = """
                INSERT INTO patient_profiles (user_id, birth_date, address)
                VALUES (%s, %s, %s)
                """
                cursor.execute(profile_query, (self.user_id, birth_date, address))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            messagebox.showinfo("Success", "Profile updated successfully!")
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Could not save changes: {e}")
    
    def add_record(self):
        # This would typically open a form to add a new medical record
        # For simplicity, we'll just add a placeholder record
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
            # In a real application, you would also delete from database
            self.records_tree.delete(selected_item)
    
    def open_updatepage(self):
        self.root.destroy() 
        root = tk.Tk()
        # Pass the user_id to the update profile app
        from updateprofile import ProfileUpdateApp
        app = ProfileUpdateApp(root, self.user_id)
        root.mainloop()

# SQL Schema for reference:
"""
-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patient Profiles Table
CREATE TABLE patient_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    birth_date DATE,
    address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Medical Records Table
CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    visit_date DATE NOT NULL,
    diagnosis TEXT,
    treatment TEXT,
    doctor_name VARCHAR(100),
    FOREIGN KEY (patient_id) REFERENCES users(id)
);
"""

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientProfile(root)
    root.mainloop()
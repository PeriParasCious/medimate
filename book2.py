import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import io
import os

class DoctorAppointmentApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Doctor Appointment Booking")
        self.root.geometry("1280x853")
    
    # Disable window resizing
        self.root.resizable(False, False)
    
    # Rest of your initialization code...
        
        # Disable fullscreen switching
        self.root.bind("<F11>", lambda e: "break")
        
        # Track window size changes
        self.root.bind("<Configure>", self.on_window_resize)
        self.current_width = self.root.winfo_width()
        self.doctors_per_row = 2  # Default
        
        # Create a canvas with scrollbar
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sample doctor data with image paths
        self.doctors = [
            {"name": "Dr. John Smith", "specialty": "Cardiologist", "experience": "15 years", "rating": 4.8, "image_path": r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png"},
            {"name": "Dr. Sarah Johnson", "specialty": "Dermatologist", "experience": "10 years", "rating": 4.6, "image_path": r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png"},
            {"name": "Dr. Michael Lee", "specialty": "Neurologist", "experience": "20 years", "rating": 4.9, "image_path": r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png"},
            {"name": "Dr. Emily Davis", "specialty": "Pediatrician", "experience": "12 years", "rating": 4.7, "image_path": r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png"},
            {"name": "Dr. Robert Wilson", "specialty": "Orthopedic", "experience": "18 years", "rating": 4.5, "image_path": r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png"},
            {"name": "Dr. Lisa Brown", "specialty": "Gynecologist", "experience": "14 years", "rating": 4.8, "image_path": r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png"},
            {"name": "Dr. David Chen", "specialty": "Psychiatrist", "experience": "16 years", "rating": 4.7, "image_path": r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png"},
            {"name": "Dr. Amanda Clark", "specialty": "Endocrinologist", "experience": "13 years", "rating": 4.9, "image_path": r"C:\Users\Paras Mahajan\Desktop\MINIPROJECT\logo.png"},
        ]
        
        # Create doctor cards
        self.create_doctor_cards()
    
    def on_window_resize(self, event):
        # Only respond to window width changes
        if self.root.winfo_width() != self.current_width:
            self.current_width = self.root.winfo_width()
            
            # Determine doctors per row based on width
            if self.current_width >= 1600:
                self.doctors_per_row = 4
            else:
                self.doctors_per_row = 2
                
            # Redraw the doctor cards
            self.redraw_doctor_cards()
    
    def redraw_doctor_cards(self):
        # Clear the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Redraw doctor cards
        self.create_doctor_cards()
    
    def create_circular_image(self, image_path, size):
        """Create a circular image from a file path"""
        try:
            # Try to open the image file
            if os.path.exists(image_path):
                original_image = Image.open(image_path)
            else:
                # If image doesn't exist, create a placeholder with first letter of doctor's name
                return self.create_placeholder_image(size, image_path)
                
            # Resize the image to fit our dimensions
            original_image = original_image.resize((size, size), Image.LANCZOS)
            
            # Create a circular mask
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            
            # Create a circular image
            circular_image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
            circular_image.paste(original_image, (0, 0), mask)
            
            return ImageTk.PhotoImage(circular_image)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return self.create_placeholder_image(size, image_path)
    
    def create_placeholder_image(self, size, image_path):
        """Create a placeholder circular image with a border"""
        # Extract doctor's initial from the image path or use a default
        initial = "D"  # Default initial
        if isinstance(image_path, str) and "doctor" in image_path:
            # Try to extract doctor number from filename (e.g., "doctor1.jpg" -> "1")
            try:
                doc_num = ''.join(filter(str.isdigit, image_path))
                if doc_num:
                    initial = str(doc_num)
            except:
                pass
        
        # Create a circular placeholder
        img = Image.new("RGB", (size, size), color="#E0E0E0")
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, size, size), outline="black", width=2)
        
        # Add the initial
        font_size = size // 2
        draw.text((size//2-font_size//3, size//2-font_size//2), initial, fill="black", font=None)
        
        return ImageTk.PhotoImage(img)
    
    def create_doctor_cards(self):
        total_doctors = len(self.doctors)
        cards_per_row = self.doctors_per_row
        
        # Calculate card dimensions
        card_width = 250  # Base card width
        
        # Create frames for each row
        for i in range(0, total_doctors, cards_per_row):
            row_frame = tk.Frame(self.scrollable_frame)
            row_frame.pack(fill=tk.X, pady=10)
            
            # Center the row frame
            row_frame.pack_configure(anchor=tk.CENTER)
            
            # Calculate how many doctors to display in this row
            end_idx = min(i + cards_per_row, total_doctors)
            doctors_in_row = end_idx - i
            
            # Create a container frame for the cards in this row
            container_frame = tk.Frame(row_frame)
            container_frame.pack(anchor=tk.CENTER)
            
            # Create frames for each doctor in this row
            for j in range(i, end_idx):
                doctor = self.doctors[j]
                self.create_doctor_card(container_frame, doctor, card_width)
    
    def create_doctor_card(self, parent_frame, doctor, card_width):
        # Create a frame for the doctor
        doctor_frame = tk.Frame(parent_frame, borderwidth=2, relief=tk.RIDGE, width=card_width, height=380)
        doctor_frame.pack(side=tk.RIGHT, padx=10)
        doctor_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Create circular doctor image
        img_size = 120 if self.doctors_per_row > 2 else 150  # Smaller image for more cards per row
        photo = self.create_circular_image(doctor["image_path"], img_size)
        img_label = tk.Label(doctor_frame, image=photo)
        img_label.image = photo  # Keep a reference to prevent garbage collection
        img_label.pack(pady=(20, 10))
        
        # Doctor name
        name_label = tk.Label(doctor_frame, text=doctor["name"], font=("Arial", 12, "bold"))
        name_label.pack(pady=5)
        
        # Doctor specialty
        specialty_label = tk.Label(doctor_frame, text=doctor["specialty"], font=("Arial", 10))
        specialty_label.pack(pady=5)
        
        # Doctor experience
        exp_label = tk.Label(doctor_frame, text=f"Experience: {doctor['experience']}", font=("Arial", 9))
        exp_label.pack(pady=5)
        
        # Doctor rating
        rating_frame = tk.Frame(doctor_frame)
        rating_frame.pack(pady=5)
        
        rating_label = tk.Label(rating_frame, text=f"Rating: ", font=("Arial", 9))
        rating_label.pack(side=tk.LEFT)
        
        # Show rating as stars
        rating = doctor["rating"]
        for i in range(5):
            if i < int(rating):
                star = "★"  # Filled star
            elif i < rating:
                star = "✮"  # Half-filled star
            else:
                star = "☆"  # Empty star
            star_label = tk.Label(rating_frame, text=star, font=("Arial", 9), fg="gold")
            star_label.pack(side=tk.LEFT)
        
        # Rating value
        rating_value = tk.Label(rating_frame, text=f" ({rating})", font=("Arial", 9))
        rating_value.pack(side=tk.LEFT)
        
        # Book appointment button
        book_button = tk.Button(
            doctor_frame, 
            text="Book Appointment", 
            bg="#4CAF50", 
            fg="white",
            font=("Arial", 9, "bold"),
            command=lambda d=doctor: self.book_appointment(d)
        )
        book_button.pack(pady=15)
    
    def book_appointment(self, doctor):
        # This function would handle the appointment booking logic
        print(f"Booking appointment with {doctor['name']}")
        # Could open a new window for selecting date and time
        booking_window = tk.Toplevel(self.root)
        booking_window.title(f"Book Appointment with {doctor['name']}")
        booking_window.geometry("400x300")
        
        # Simple booking form
        tk.Label(booking_window, text=f"Book Appointment with {doctor['name']}", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(booking_window, text=f"Specialty: {doctor['specialty']}", font=("Arial", 12)).pack(pady=5)
        
        # Date selection
        date_frame = tk.Frame(booking_window)
        date_frame.pack(pady=10)
        tk.Label(date_frame, text="Date: ", font=("Arial", 10)).pack(side=tk.LEFT)
        date_entry = tk.Entry(date_frame, width=15)
        date_entry.pack(side=tk.LEFT)
        date_entry.insert(0, "MM/DD/YYYY")
        
        # Time selection
        time_frame = tk.Frame(booking_window)
        time_frame.pack(pady=10)
        tk.Label(time_frame, text="Time: ", font=("Arial", 10)).pack(side=tk.LEFT)
        time_options = ["9:00 AM", "10:00 AM", "11:00 AM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"]
        time_var = tk.StringVar(booking_window)
        time_var.set(time_options[0])
        time_dropdown = tk.OptionMenu(time_frame, time_var, *time_options)
        time_dropdown.pack(side=tk.LEFT)
        
        # Confirm button
        confirm_button = tk.Button(
            booking_window,
            text="Confirm Appointment",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self.confirm_booking(doctor, date_entry.get(), time_var.get(), booking_window)
        )
        confirm_button.pack(pady=20)
    
    def confirm_booking(self, doctor, date, time, window):
        print(f"Appointment confirmed with {doctor['name']} on {date} at {time}")
        window.destroy()
        
        # Show confirmation message
        confirmation = tk.Toplevel(self.root)
        confirmation.title("Appointment Confirmed")
        confirmation.geometry("300x150")
        
        tk.Label(confirmation, text="Appointment Confirmed!", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(confirmation, text=f"Doctor: {doctor['name']}").pack(pady=5)
        tk.Label(confirmation, text=f"Date: {date}").pack(pady=5)
        tk.Label(confirmation, text=f"Time: {time}").pack(pady=5)
        
        tk.Button(
            confirmation,
            text="OK",
            command=confirmation.destroy
        ).pack(pady=10)

if __name__ == "_main_":
    root = tk.Tk()
    app = DoctorAppointmentApp(root)
    root.mainloop()
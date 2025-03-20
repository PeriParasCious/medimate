import tkinter as tk

class AppointmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Page")
        self.root.geometry("1280x853")  # Set the window size

        # Center the window
        self.center_window()

        # Create a frame to hold the profiles
        self.profile_frame = tk.Frame(self.root)
        self.profile_frame.pack(expand=True)  # Use expand to center the frame vertically

        # Create profile buttons and labels
        self.create_profile_widgets()

    def center_window(self):
        # Get the dimensions of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (400 // 2)

        # Set the position of the window
        self.root.geometry(f"+{x}+{y}")

    def create_profile_widgets(self):
        profiles = ["Profile 1", "Profile 2", "Profile 3", "Profile 4"]
        self.labels = {}  # Dictionary to hold labels for each profile

        for i, profile in enumerate(profiles):
            # Create a frame for each profile button and label
            frame = tk.Frame(self.profile_frame)
            frame.grid(row=0, column=i, padx=20)  # Space out buttons with padx

            # Create a button for each profile
            button = tk.Button(frame, text=profile, command=lambda p=profile: self.select_profile(p))
            button.pack()

            # Create a label for each profile with default text
            label = tk.Label(frame, text="Doctor's Profile", width=20, height=3, relief="groove")
            label.pack(pady=5)  # Add some vertical padding between button and label
            self.labels[profile] = label  # Store the label in the dictionary

        # Center the profile frame in the window
        self.profile_frame.grid_rowconfigure(0, weight=1)  # Allow the row to expand
        self.profile_frame.grid_columnconfigure(tuple(range(len(profiles))), weight=1)  # Allow columns to expand


    def select_profile(self, profile):
        # Update the label with the selected profile details
        for p in self.labels:
            self.labels[p].config(text="Doctor's Profile")  # Reset all labels to default text

        self.labels[profile].config(text=f"You have selected {profile}.\nDetails about {profile} can be added here.")

    

if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentApp(root)
    root.mainloop()
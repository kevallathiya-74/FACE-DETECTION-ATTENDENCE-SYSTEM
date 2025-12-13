import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import threading
import glob

# project module
import show_attendance
import take_image
import train_image
import automated_attendance

# engine = pyttsx3.init()
# engine.say("Welcome!")
# engine.say("Please browse through your options..")
# engine.runAndWait()


def text_to_speech(text):
    """Run text-to-speech - simplified version to avoid threading issues"""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        pass


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "./models/Trainner.yml"
)
trainimage_path = "./training_images"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = (
    "./student_details/studentdetails.csv"
)
attendance_path = "attendance"

# to destroy screen
def del_sc1():
    sc1.destroy()

# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x600")
    ImageUI.configure(background="#1c1c1c")
    ImageUI.resizable(0, 0)
    
    # Title
    titl = tk.Label(
        ImageUI, 
        text="Register Your Face", 
        bg="#1c1c1c", 
        fg="#00ff00", 
        font=("Verdana", 30, "bold")
    )
    titl.pack(pady=20)

    # Details frame
    details_frame = tk.Frame(ImageUI, bg="#1c1c1c")
    details_frame.pack(fill=X, padx=20, pady=10)

    # Division
    tk.Label(
        details_frame,
        text="Division",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 12)
    ).grid(row=0, column=0, padx=5, pady=5)
    
    division_entry = tk.Entry(
        details_frame,
        width=17,
        bg="#333333",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat"
    )
    division_entry.grid(row=0, column=1, padx=5, pady=5)

    # Enrollment No
    tk.Label(
        details_frame,
        text="Enrollment No",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 12)
    ).grid(row=1, column=0, padx=5, pady=5)
    
    enrollment_entry = tk.Entry(
        details_frame,
        width=17,
        validate="key",
        bg="#333333",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat"
    )
    enrollment_entry.grid(row=1, column=1, padx=5, pady=5)
    enrollment_entry["validatecommand"] = (enrollment_entry.register(testVal), "%P", "%d")

    # Roll Number
    tk.Label(
        details_frame,
        text="Roll Number",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 12)
    ).grid(row=2, column=0, padx=5, pady=5)
    
    roll_entry = tk.Entry(
        details_frame,
        width=17,
        validate="key",
        bg="#333333",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat"
    )
    roll_entry.grid(row=2, column=1, padx=5, pady=5)
    roll_entry["validatecommand"] = (roll_entry.register(testVal), "%P", "%d")

    # Name
    tk.Label(
        details_frame,
        text="Name",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 12)
    ).grid(row=3, column=0, padx=5, pady=5)
    
    name_entry = tk.Entry(
        details_frame,
        width=17,
        bg="#333333",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat"
    )
    name_entry.grid(row=3, column=1, padx=5, pady=5)

    # Notification
    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bg="#333333",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat"
    )
    message.pack(pady=20)

    def take_image():
        division = division_entry.get()
        enrollment = enrollment_entry.get()
        roll = roll_entry.get()
        name = name_entry.get()
        
        if not all([division, enrollment, roll, name]):
            err_screen()
            return
            
        take_image.TakeImage(
            enrollment,
            name,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        
        # Save to student details CSV
        df = pd.read_csv(studentdetail_path)
        new_student = pd.DataFrame({
            'Division': [division],
            'Enrollment': [enrollment],
            'Roll Number': [roll],
            'Name': [name]
        })
        df = pd.concat([df, new_student], ignore_index=True)
        df.to_csv(studentdetail_path, index=False)
        
        # Clear entries
        division_entry.delete(0, END)
        enrollment_entry.delete(0, END)
        roll_entry.delete(0, END)
        name_entry.delete(0, END)

    def train_image():
        if not os.path.exists(trainimage_path) or not os.listdir(trainimage_path):
            message_window = Tk()
            message_window.title("No Images Found")
            message_window.geometry("400x150")
            message_window.configure(background="#1c1c1c")
            
            tk.Label(
                message_window,
                text="No student images found!\nPlease register students first.",
                fg="#00ff00",
                bg="#1c1c1c",
                font=("Verdana", 12),
                wraplength=350
            ).pack(pady=20)
            
            tk.Button(
                message_window,
                text="OK",
                command=message_window.destroy,
                fg="#00ff00",
                bg="#333333",
                width=10,
                height=1,
                activebackground="#3c3c3c",
                font=("Verdana", 12)
            ).pack(pady=10)
            return
        
        train_image.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # Buttons frame
    button_frame = tk.Frame(ImageUI, bg="#1c1c1c")
    button_frame.pack(pady=20)

    # Take Image button
    takeImg = tk.Button(
        button_frame,
        text="Take Image",
        command=take_image,
        bg="#2c2c2c",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat",
        padx=20,
        pady=10
    )
    takeImg.pack(side=LEFT, padx=10)

    # Train Image button
    trainImg = tk.Button(
        button_frame,
        text="Train Image",
        command=train_image,
        bg="#2c2c2c",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat",
        padx=20,
        pady=10
    )
    trainImg.pack(side=LEFT, padx=10)

    # Add hover effects
    for button in button_frame.winfo_children():
        button.bind("<Enter>", lambda e: e.widget.configure(bg="#3c3c3c"))
        button.bind("<Leave>", lambda e: e.widget.configure(bg="#2c2c2c"))

    ImageUI.mainloop()

def start_slot_attendance(slot_name, subject):
    result = automated_attendance.take_attendance_for_slot(slot_name, subject)
    message_window = Tk()
    message_window.title("Attendance Result")
    message_window.geometry("400x150")
    message_window.configure(background="#1c1c1c")
    
    tk.Label(
        message_window,
        text=result,
        fg="#00ff00",
        bg="#1c1c1c",
        font=("Verdana", 12),
        wraplength=350
    ).pack(pady=20)
    
    tk.Button(
        message_window,
        text="OK",
        command=message_window.destroy,
        fg="#00ff00",
        bg="#333333",
        width=10,
        height=1,
        activebackground="#3c3c3c",
        font=("Verdana", 12)
    ).pack(pady=10)

def automated_attendance_window():
    automated_window = Tk()
    automated_window.title("Automated Attendance")
    automated_window.geometry("800x600")
    automated_window.configure(background="#1c1c1c")
    
    # Title
    tk.Label(
        automated_window,
        text="Automated Attendance System",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 24, "bold")
    ).pack(pady=(20, 10))
    
    # Subject selection
    subject_frame = tk.Frame(automated_window, bg="#1c1c1c")
    subject_frame.pack(fill=X, pady=10)
    
    tk.Label(
        subject_frame,
        text="Enter Subject:",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 12)
    ).pack(side=LEFT, padx=10)
    
    subject_entry = tk.Entry(
        subject_frame,
        width=20,
        bg="#333333",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat"
    )
    subject_entry.pack(side=LEFT, padx=10)
    
    # Status label
    status_label = tk.Label(
        automated_window,
        text="Click Start to begin automated attendance",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 12)
    )
    status_label.pack(pady=20)
    
    # Timer label
    timer_label = tk.Label(
        automated_window,
        text="",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 16, "bold")
    )
    timer_label.pack(pady=10)
    
    def start_attendance():
        subject = subject_entry.get()
        if not subject:
            status_label.config(text="Please enter a subject name!")
            return
            
        status_label.config(text="Starting automated attendance...")
        automated_window.update()
        
        # Start attendance recording
        result = automated_attendance.start_automated_attendance(subject, 120)  # 120 seconds = 2 minutes
        
        # Update status
        status_label.config(text=result)
        automated_window.update()
        
        # Show completion message
        message_window = Tk()
        message_window.title("Attendance Complete")
        message_window.geometry("400x150")
        message_window.configure(background="#1c1c1c")
        
        tk.Label(
            message_window,
            text="Automated attendance completed!\nYou can view the results in the Automated Attendance View menu.",
            fg="#00ff00",
            bg="#1c1c1c",
            font=("Verdana", 12),
            wraplength=350
        ).pack(pady=20)
        
        tk.Button(
            message_window,
            text="OK",
            command=message_window.destroy,
            fg="#00ff00",
            bg="#333333",
            width=10,
            height=1,
            activebackground="#3c3c3c",
            font=("Verdana", 12)
        ).pack(pady=10)
    
    # Start button
    start_btn = tk.Button(
        automated_window,
        text="Start Automated Attendance",
        command=start_attendance,
        bg="#2c2c2c",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat",
        padx=20,
        pady=10
    )
    start_btn.pack(pady=20)
    
    # Add hover effect
    start_btn.bind("<Enter>", lambda e: start_btn.configure(bg="#3c3c3c"))
    start_btn.bind("<Leave>", lambda e: start_btn.configure(bg="#2c2c2c"))
    
    automated_window.mainloop()

def view_automated_attendance():
    view_window = Tk()
    view_window.title("Automated Attendance Records")
    view_window.geometry("1000x600")
    view_window.configure(background="#1c1c1c")
    
    # Title
    tk.Label(
        view_window,
        text="Automated Attendance Records",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 24, "bold")
    ).pack(pady=(20, 10))
    
    # Subject selection
    subject_frame = tk.Frame(view_window, bg="#1c1c1c")
    subject_frame.pack(fill=X, pady=10)
    
    tk.Label(
        subject_frame,
        text="Enter Subject:",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 12)
    ).pack(side=LEFT, padx=10)
    
    subject_entry = tk.Entry(
        subject_frame,
        width=20,
        bg="#333333",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat"
    )
    subject_entry.pack(side=LEFT, padx=10)
    
    # Create treeview for attendance data
    tree = ttk.Treeview(view_window, columns=("Time", "Division", "Enrollment", "Roll", "Name", "Status"), show="headings")
    tree.heading("Time", text="Time")
    tree.heading("Division", text="Division")
    tree.heading("Enrollment", text="Enrollment")
    tree.heading("Roll", text="Roll")
    tree.heading("Name", text="Name")
    tree.heading("Status", text="Status")
    
    # Configure column widths
    tree.column("Time", width=150)
    tree.column("Division", width=100)
    tree.column("Enrollment", width=100)
    tree.column("Roll", width=100)
    tree.column("Name", width=200)
    tree.column("Status", width=100)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack treeview and scrollbar
    tree.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    def load_attendance():
        subject = subject_entry.get()
        if not subject:
            messagebox.showerror("Error", "Please enter a subject name!")
            return
            
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        # Load attendance data - Check both possible file paths
        try:
            # First try loading from the main attendance file
            main_file = f"Attendance/{subject}/attendance.csv"
            if os.path.exists(main_file):
                df = pd.read_csv(main_file)
                for _, row in df.iterrows():
                    tree.insert("", "end", values=(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current time
                        row.get("Division", ""),
                        row["Enrollment"],
                        row.get("Roll", ""),
                        row["Name"],
                        "Present"
                    ))
            else:
                # Try loading the most recent session file
                session_files = glob.glob(f"Attendance/{subject}/session_*.csv")
                if session_files:
                    latest_file = max(session_files, key=os.path.getctime)  # Get most recent file
                    df = pd.read_csv(latest_file)
                    for _, row in df.iterrows():
                        tree.insert("", "end", values=(
                            row.get("Time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                            row.get("Division", ""),
                            row["Enrollment"],
                            row.get("Roll", ""),
                            row["Name"],
                            row.get("Status", "Present")
                        ))
                else:
                    messagebox.showinfo("Info", f"No attendance records found for {subject}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error loading attendance: {str(e)}")
    
    # Load button
    load_btn = tk.Button(
        view_window,
        text="Load Attendance",
        command=load_attendance,
        bg="#2c2c2c",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat",
        padx=20,
        pady=10
    )
    load_btn.pack(pady=10)
    
    # Add hover effect
    load_btn.bind("<Enter>", lambda e: load_btn.configure(bg="#3c3c3c"))
    load_btn.bind("<Leave>", lambda e: load_btn.configure(bg="#2c2c2c"))
    
    view_window.mainloop()

def check_model_trained():
    if not os.path.exists(trainimagelabel_path):
        message_window = Tk()
        message_window.title("Model Not Trained")
        message_window.geometry("400x150")
        message_window.configure(background="#1c1c1c")
        
        tk.Label(
            message_window,
            text="Model is not trained yet!\nPlease register students and train the model first.",
            fg="#00ff00",
            bg="#1c1c1c",
            font=("Verdana", 12),
            wraplength=350
        ).pack(pady=20)
        
        tk.Button(
            message_window,
            text="OK",
            command=message_window.destroy,
            fg="#00ff00",
            bg="#333333",
            width=10,
            height=1,
            activebackground="#3c3c3c",
            font=("Verdana", 12)
        ).pack(pady=10)
        return False
    return True

window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="#1c1c1c")  # Dark theme

# Add a modern frame for better organization
main_frame = tk.Frame(window, bg="#1c1c1c")
main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Header section with logo and title
header_frame = tk.Frame(main_frame, bg="#1c1c1c")
header_frame.pack(fill=X, pady=(0, 20))

logo = Image.open("UI_Image/0001.png")
logo = logo.resize((60, 57), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
l1 = tk.Label(header_frame, image=logo1, bg="#1c1c1c")
l1.pack(side=LEFT, padx=10)

title_frame = tk.Frame(header_frame, bg="#1c1c1c")
title_frame.pack(side=LEFT, fill=X, expand=True)

titl = tk.Label(
    title_frame, 
    text="CLASS VISION", 
    bg="#1c1c1c", 
    fg="#00ff00", 
    font=("Verdana", 32, "bold")
)
titl.pack()

welcome_text = tk.Label(
    title_frame,
    text="Welcome to CLASS VISION",
    bg="#1c1c1c",
    fg="#00ff00",
    font=("Verdana", 24, "bold")
)
welcome_text.pack(pady=(5, 0))

# Main content area with buttons
content_frame = tk.Frame(main_frame, bg="#1c1c1c")
content_frame.pack(fill=BOTH, expand=True)

# Button style configuration
button_style = {
    "font": ("Verdana", 14),
    "bg": "#2c2c2c",
    "fg": "#00ff00",
    "height": 2,
    "width": 20,
    "relief": "flat",
    "bd": 0,
    "activebackground": "#3c3c3c",
    "activeforeground": "#ffffff"
}

# Create a grid of buttons
buttons_frame = tk.Frame(content_frame, bg="#1c1c1c")
buttons_frame.pack(expand=True)

# Register button
register_btn = tk.Button(
    buttons_frame,
    text="Register New Student",
    command=TakeImageUI,
    **button_style
)
register_btn.grid(row=0, column=0, padx=20, pady=10)

# Take Attendance button
attendance_btn = tk.Button(
    buttons_frame,
    text="Take Attendance",
    command=lambda: check_model_trained() and automated_attendance.subjectChoose(text_to_speech),
    **button_style
)
attendance_btn.grid(row=0, column=1, padx=20, pady=10)

# Automated Attendance button
automated_btn = tk.Button(
    buttons_frame,
    text="Automated Attendance",
    command=lambda: check_model_trained() and automated_attendance_window(),
    **button_style
)
automated_btn.grid(row=0, column=2, padx=20, pady=10)

# View Attendance button
view_btn = tk.Button(
    buttons_frame,
    text="View Attendance",
    command=lambda: show_attendance.subjectchoose(text_to_speech),
    **button_style
)
view_btn.grid(row=1, column=0, padx=20, pady=10)

# Automated Attendance View button
automated_view_btn = tk.Button(
    buttons_frame,
    text="Automated Attendance View",
    command=view_automated_attendance,
    **button_style
)
automated_view_btn.grid(row=1, column=1, padx=20, pady=10)

# Exit button
exit_btn = tk.Button(
    buttons_frame,
    text="Exit",
    command=quit,
    **button_style
)
exit_btn.grid(row=1, column=2, padx=20, pady=10)

# Add hover effects to buttons
def on_enter(e):
    e.widget['background'] = '#3c3c3c'

def on_leave(e):
    e.widget['background'] = '#2c2c2c'

for button in buttons_frame.winfo_children():
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

window.mainloop()

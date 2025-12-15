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
import take_image as take_image_module
import train_image as train_image_module
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
    sc1.geometry("500x250")
    try:
        sc1.iconbitmap("AMS.ico")
    except:
        pass
    sc1.title("SmartAttend - Warning")
    sc1.configure(background="#0a0e27")
    sc1.resizable(0, 0)
    
    # Main frame
    frame = tk.Frame(sc1, bg="#1a1d35", highlightthickness=3, highlightbackground="#ef4444")
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Warning icon
    tk.Label(
        frame,
        text="⚠️",
        bg="#1a1d35",
        fg="#ef4444",
        font=("Segoe UI", 60)
    ).pack(pady=(25, 10))
    
    # Message
    tk.Label(
        frame,
        text="All Fields Required!",
        fg="#f0f4f8",
        bg="#1a1d35",
        font=("Segoe UI", 18, "bold"),
    ).pack(pady=8)
    
    tk.Label(
        frame,
        text="Please fill in all the details before proceeding",
        fg="#a5b4c9",
        bg="#1a1d35",
        font=("Segoe UI", 11),
    ).pack(pady=(0, 20))
    
    # OK button
    ok_btn = tk.Button(
        frame,
        text="OK",
        command=del_sc1,
        fg="#ffffff",
        bg="#ef4444",
        width=15,
        relief="flat",
        bd=0,
        cursor="hand2",
        pady=12,
        activebackground="#dc2626",
        font=("Segoe UI", 13, "bold"),
    )
    ok_btn.pack(pady=(0, 25))
    
    ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg="#dc2626"))
    ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg="#ef4444"))

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("SmartAttend - Student Registration")
    ImageUI.geometry("1000x800")
    
    # Modern colors
    BG_DARK = "#0a0e27"
    BG_MID = "#16213e"
    CARD_BG = "#1a1d35"
    ACCENT_BLUE = "#0096c7"
    TEXT_WHITE = "#f0f4f8"
    TEXT_GRAY = "#a5b4c9"
    INPUT_BG = "#252d4a"
    
    ImageUI.configure(background=BG_DARK)
    ImageUI.resizable(1, 1)
    
    # Main container
    main_frame = tk.Frame(ImageUI, bg=BG_DARK)
    main_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)
    
    # Header
    header_frame = tk.Frame(main_frame, bg=BG_DARK)
    header_frame.pack(fill=X, pady=(0, 15))
    
    # Icon
    icon_label = tk.Label(
        header_frame,
        text="🎓",
        bg=BG_DARK,
        fg=ACCENT_BLUE,
        font=("Segoe UI", 38)
    )
    icon_label.pack()
    
    title = tk.Label(
        header_frame, 
        text="Student Registration", 
        bg=BG_DARK, 
        fg=TEXT_WHITE, 
        font=("Segoe UI", 28, "bold")
    )
    title.pack(pady=(6, 2))
    
    subtitle = tk.Label(
        header_frame,
        text="Register a new student by capturing their face for attendance recognition",
        bg=BG_DARK,
        fg=TEXT_GRAY,
        font=("Segoe UI", 12)
    )
    subtitle.pack()

    # Card frame for form - don't let it expand
    card_frame = tk.Frame(main_frame, bg=CARD_BG, highlightthickness=3, highlightbackground=ACCENT_BLUE)
    card_frame.pack(fill=X, expand=False, pady=10)
    
    # Details frame
    details_frame = tk.Frame(card_frame, bg=CARD_BG)
    details_frame.pack(pady=25, padx=50)

    # Modern form field creator
    def create_field(parent, label_text, row_num, validate_digits=False):
        # Label
        label = tk.Label(
            parent,
            text=label_text,
            bg=CARD_BG,
            fg=TEXT_WHITE,
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        )
        label.grid(row=row_num, column=0, sticky="w", pady=15, padx=(0, 30))
        
        # Entry
        entry = tk.Entry(
            parent,
            width=40,
            bg=INPUT_BG,
            fg=TEXT_WHITE,
            font=("Segoe UI", 13),
            relief="flat",
            bd=0,
            insertbackground=TEXT_WHITE,
            highlightthickness=2,
            highlightbackground="#2a3f5f",
            highlightcolor=ACCENT_BLUE
        )
        entry.grid(row=row_num, column=1, pady=20, ipady=12, sticky="ew")
        
        if validate_digits:
            entry["validate"] = "key"
            entry["validatecommand"] = (entry.register(testVal), "%P", "%d")
        
        return entry
    
    # Configure grid
    details_frame.grid_columnconfigure(1, weight=1)
    
    # Create fields
    division_entry = create_field(details_frame, "Division:", 0)
    enrollment_entry = create_field(details_frame, "Enrollment No:", 1, validate_digits=True)
    roll_entry = create_field(details_frame, "Roll Number:", 2, validate_digits=True)
    name_entry = create_field(details_frame, "Full Name:", 3)

    # Status message frame
    status_frame = tk.Frame(main_frame, bg="#252d4a", highlightthickness=2, highlightbackground="#0096c7")
    status_frame.pack(fill=X, pady=10, expand=False)
    
    message = tk.Label(
        status_frame,
        text="Fill in all details and click 'Capture Images' to register the student",
        bg="#252d4a",
        fg=TEXT_GRAY,
        font=("Segoe UI", 11),
        wraplength=850,
        pady=12
    )
    message.pack()

    def take_image():
        division = division_entry.get()
        enrollment = enrollment_entry.get()
        roll = roll_entry.get()
        name = name_entry.get()
        
        if not all([division, enrollment, roll, name]):
            err_screen()
            return
            
        take_image_module.TakeImage(
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
        
        train_image_module.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # Buttons frame - ensure it's always visible
    button_frame = tk.Frame(main_frame, bg=BG_DARK)
    button_frame.pack(pady=15, fill=X, expand=False)
    
    # Container to center buttons
    button_container = tk.Frame(button_frame, bg=BG_DARK)
    button_container.pack()
    
    # Modern button creator
    def create_button(parent, text, command, bg_color, icon=""):
        btn = tk.Button(
            parent,
            text=f"{icon} {text}",
            command=command,
            bg=bg_color,
            fg="#ffffff",
            font=("Segoe UI", 14, "bold"),
            relief="flat",
            bd=0,
            padx=40,
            pady=15,
            cursor="hand2",
            highlightthickness=0
        )
        
        hover_colors = {
            "#0096c7": "#0077a3",
            "#7c3aed": "#6d28d9",
        }
        hover_color = hover_colors.get(bg_color, bg_color)
        
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        
        return btn

    # Buttons in container
    takeImg = create_button(button_container, "Capture Images", take_image, "#0096c7", "📸")
    takeImg.pack(side=LEFT, padx=15)

    trainImg = create_button(button_container, "Train Model", train_image, "#7c3aed", "🧠")
    trainImg.pack(side=LEFT, padx=15)

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
    # Modern colors
    BG_DARK = "#0a0e27"
    CARD_BG = "#1a1d35"
    ACCENT_BLUE = "#0096c7"
    TEXT_WHITE = "#f0f4f8"
    TEXT_GRAY = "#a5b4c9"
    INPUT_BG = "#252d4a"
    
    automated_window = Tk()
    automated_window.title("SmartAttend - Automated Attendance")
    automated_window.geometry("700x550")
    automated_window.configure(background=BG_DARK)
    
    # Main container
    main_frame = tk.Frame(automated_window, bg=BG_DARK)
    main_frame.pack(fill=BOTH, expand=True, padx=40, pady=40)
    
    # Icon
    tk.Label(
        main_frame,
        text="🤖",
        bg=BG_DARK,
        fg=ACCENT_BLUE,
        font=("Segoe UI", 56)
    ).pack(pady=(0, 10))
    
    # Title
    tk.Label(
        main_frame,
        text="Automated Attendance System",
        bg=BG_DARK,
        fg=TEXT_WHITE,
        font=("Segoe UI", 28, "bold")
    ).pack(pady=(0, 50))
    
    # Input card
    input_card = tk.Frame(main_frame, bg=CARD_BG, highlightthickness=2, highlightbackground=ACCENT_BLUE)
    input_card.pack(fill=X, pady=(0, 25))
    
    # Subject selection
    subject_frame = tk.Frame(input_card, bg=CARD_BG)
    subject_frame.pack(pady=25, padx=30)
    
    tk.Label(
        subject_frame,
        text="Enter Subject:",
        bg=CARD_BG,
        fg=TEXT_WHITE,
        font=("Segoe UI", 14, "bold")
    ).pack(side=LEFT, padx=(0, 20))
    
    subject_entry = tk.Entry(
        subject_frame,
        width=30,
        bg=INPUT_BG,
        fg=TEXT_WHITE,
        font=("Segoe UI", 13),
        relief="flat",
        bd=0,
        insertbackground=TEXT_WHITE,
        highlightthickness=2,
        highlightbackground="#2a3f5f",
        highlightcolor=ACCENT_BLUE
    )
    subject_entry.pack(side=LEFT, ipady=10, padx=10)
    
    # Status label
    status_label = tk.Label(
        main_frame,
        text="Click Start to begin automated attendance",
        bg=BG_DARK,
        fg=TEXT_GRAY,
        font=("Segoe UI", 12)
    )
    status_label.pack(pady=20)
    
    # Timer label
    timer_label = tk.Label(
        main_frame,
        text="",
        bg=BG_DARK,
        fg=ACCENT_BLUE,
        font=("Segoe UI", 18, "bold")
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
        message_window.geometry("500x200")
        message_window.configure(background=BG_DARK)
        
        msg_frame = tk.Frame(message_window, bg=BG_DARK)
        msg_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(
            msg_frame,
            text="✓",
            fg=ACCENT_BLUE,
            bg=BG_DARK,
            font=("Segoe UI", 36)
        ).pack(pady=(0, 15))
        
        tk.Label(
            msg_frame,
            text="Automated attendance completed!\nYou can view the results in the Automated Attendance View menu.",
            fg=TEXT_WHITE,
            bg=BG_DARK,
            font=("Segoe UI", 12),
            wraplength=400
        ).pack(pady=(0, 20))
        
        ok_btn = tk.Button(
            msg_frame,
            text="OK",
            command=message_window.destroy,
            fg=TEXT_WHITE,
            bg=ACCENT_BLUE,
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        ok_btn.pack()
        ok_btn.bind("<Enter>", lambda e: ok_btn.configure(bg="#0077a3"))
        ok_btn.bind("<Leave>", lambda e: ok_btn.configure(bg=ACCENT_BLUE))
    
    # Start button
    start_btn = tk.Button(
        main_frame,
        text="▶ Start Automated Attendance",
        command=start_attendance,
        bg=ACCENT_BLUE,
        fg=TEXT_WHITE,
        font=("Segoe UI", 14, "bold"),
        relief="flat",
        bd=0,
        padx=40,
        pady=15,
        cursor="hand2",
        highlightthickness=0
    )
    start_btn.pack(pady=20)
    
    # Add hover effect
    start_btn.bind("<Enter>", lambda e: start_btn.configure(bg="#0077a3"))
    start_btn.bind("<Leave>", lambda e: start_btn.configure(bg=ACCENT_BLUE))
    
    automated_window.mainloop()

def view_automated_attendance():
    view_window = Tk()
    view_window.title("SmartAttend - Attendance Analytics")
    view_window.geometry("1400x800")
    view_window.state('zoomed')
    
    # Modern colors matching main design
    BG_DARK = "#0a0e27"
    CARD_BG = "#1a1d35"
    ACCENT_BLUE = "#0096c7"
    TEXT_WHITE = "#f0f4f8"
    TEXT_GRAY = "#a5b4c9"
    INPUT_BG = "#252d4a"
    
    view_window.configure(background=BG_DARK)
    
    # Main container
    main_frame = tk.Frame(view_window, bg=BG_DARK)
    main_frame.pack(fill=BOTH, expand=True, padx=40, pady=30)
    
    # Header
    header_frame = tk.Frame(main_frame, bg=BG_DARK)
    header_frame.pack(fill=X, pady=(0, 30))
    
    # Icon
    icon_label = tk.Label(
        header_frame,
        text="📈",
        bg=BG_DARK,
        fg=ACCENT_BLUE,
        font=("Segoe UI", 56)
    )
    icon_label.pack()
    
    title_label = tk.Label(
        header_frame,
        text="Attendance Analytics",
        bg=BG_DARK,
        fg=TEXT_WHITE,
        font=("Segoe UI", 36, "bold")
    )
    title_label.pack(pady=(10, 5))
    
    subtitle_label = tk.Label(
        header_frame,
        text="View automated attendance records and statistics",
        bg=BG_DARK,
        fg=TEXT_GRAY,
        font=("Segoe UI", 12)
    )
    subtitle_label.pack()
    
    # Input card
    input_card = tk.Frame(main_frame, bg=CARD_BG, highlightthickness=3, highlightbackground=ACCENT_BLUE)
    input_card.pack(fill=X, pady=(0, 20))
    
    input_frame = tk.Frame(input_card, bg=CARD_BG)
    input_frame.pack(pady=25, padx=40)
    
    tk.Label(
        input_frame,
        text="Subject Name:",
        bg=CARD_BG,
        fg=TEXT_WHITE,
        font=("Segoe UI", 14, "bold")
    ).pack(side=LEFT, padx=(0, 20))
    
    subject_entry = tk.Entry(
        input_frame,
        width=30,
        bg=INPUT_BG,
        fg=TEXT_WHITE,
        font=("Segoe UI", 13),
        relief="flat",
        bd=0,
        insertbackground=TEXT_WHITE,
        highlightthickness=2,
        highlightbackground="#2a3f5f",
        highlightcolor=ACCENT_BLUE
    )
    subject_entry.pack(side=LEFT, ipady=10, padx=10)
    
    # Load button
    load_btn = tk.Button(
        input_frame,
        text="📊 Load Records",
        bg=ACCENT_BLUE,
        fg=TEXT_WHITE,
        font=("Segoe UI", 13, "bold"),
        relief="flat",
        bd=0,
        padx=30,
        pady=10,
        cursor="hand2",
        highlightthickness=0
    )
    load_btn.pack(side=LEFT, padx=10)
    
    load_btn.bind("<Enter>", lambda e: load_btn.configure(bg="#0077a3"))
    load_btn.bind("<Leave>", lambda e: load_btn.configure(bg=ACCENT_BLUE))
    
    # Table card
    table_card = tk.Frame(main_frame, bg=CARD_BG, highlightthickness=3, highlightbackground=ACCENT_BLUE)
    table_card.pack(fill=BOTH, expand=True)
    
    # Style for treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=INPUT_BG,
                    foreground=TEXT_WHITE,
                    fieldbackground=INPUT_BG,
                    borderwidth=0,
                    font=("Segoe UI", 11))
    style.configure("Custom.Treeview.Heading",
                    background=ACCENT_BLUE,
                    foreground=TEXT_WHITE,
                    borderwidth=0,
                    font=("Segoe UI", 12, "bold"))
    style.map("Custom.Treeview",
              background=[("selected", ACCENT_BLUE)])
    
    # Create treeview for attendance data
    tree_frame = tk.Frame(table_card, bg=CARD_BG)
    tree_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)
    
    tree = ttk.Treeview(
        tree_frame,
        columns=("Time", "Division", "Enrollment", "Roll", "Name", "Status"),
        show="headings",
        style="Custom.Treeview"
    )
    tree.heading("Time", text="Time")
    tree.heading("Division", text="Division")
    tree.heading("Enrollment", text="Enrollment")
    tree.heading("Roll", text="Roll Number")
    tree.heading("Name", text="Name")
    tree.heading("Status", text="Status")
    
    # Configure column widths
    tree.column("Time", width=180, anchor="center")
    tree.column("Division", width=100, anchor="center")
    tree.column("Enrollment", width=120, anchor="center")
    tree.column("Roll", width=120, anchor="center")
    tree.column("Name", width=200, anchor="w")
    tree.column("Status", width=120, anchor="center")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack treeview and scrollbar
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    def load_attendance():
        subject = subject_entry.get().strip()
        if not subject:
            messagebox.showerror("Error", "Please enter a subject name!")
            return
            
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        # Load attendance data - Check both possible file paths
        try:
            # Look for the subject folder (case-insensitive)
            attendance_dir = "Attendance"
            subject_lower = subject.lower()
            
            # Find matching subject folder
            subject_folder = None
            if os.path.exists(attendance_dir):
                for folder in os.listdir(attendance_dir):
                    if folder.lower() == subject_lower:
                        subject_folder = os.path.join(attendance_dir, folder)
                        break
            
            if not subject_folder:
                messagebox.showinfo("Info", f"No folder found for subject: {subject}")
                return
            
            # Get all CSV files except attendance.csv
            all_csv_files = glob.glob(f"{subject_folder}/*.csv")
            session_files = [f for f in all_csv_files if not f.endswith("attendance.csv")]
            
            if session_files:
                # Load the most recent session file
                latest_file = max(session_files, key=os.path.getctime)
                df = pd.read_csv(latest_file)
                
                # Load student details to get correct Division and Roll Number
                student_details = {}
                if os.path.exists("student_details/studentdetails.csv"):
                    student_df = pd.read_csv("student_details/studentdetails.csv")
                    for _, student in student_df.iterrows():
                        enrollment = str(student.get("Enrollment", ""))
                        division = str(student.get("Division", ""))
                        # Store all entries, prioritize non-numeric divisions
                        if enrollment not in student_details or (division and not division.isdigit()):
                            student_details[enrollment] = {
                                "Division": division,
                                "Roll Number": str(student.get("Roll Number", ""))
                            }
                
                for _, row in df.iterrows():
                    enrollment = str(row.get("Enrollment", ""))
                    
                    # Get details from student database
                    if enrollment in student_details:
                        division = student_details[enrollment]["Division"]
                        roll_no = student_details[enrollment]["Roll Number"]
                    else:
                        # Fallback to data from session file
                        division = row.get("Division", "N/A")
                        roll_no = row.get("Roll Number", row.get("Roll", ""))
                    
                    tree.insert("", "end", values=(
                        row.get("Time", datetime.datetime.now().strftime("%H:%M:%S")),
                        division,
                        enrollment,
                        roll_no,
                        row.get("Name", ""),
                        row.get("Status", "Present")
                    ))
            else:
                messagebox.showinfo("Info", f"No session files found for {subject}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error loading attendance: {str(e)}")
    
    # Connect load button command
    load_btn.configure(command=load_attendance)
    
    # Info footer
    footer_frame = tk.Frame(main_frame, bg=BG_DARK)
    footer_frame.pack(fill=X, pady=(20, 0))
    
    info_label = tk.Label(
        footer_frame,
        text="💡 Tip: Enter the subject name and click 'Load Records' to view attendance data",
        bg=BG_DARK,
        fg=TEXT_GRAY,
        font=("Segoe UI", 10, "italic")
    )
    info_label.pack()
    
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
window.title("SmartAttend - AI Face Recognition System")
window.geometry("1440x900")
window.state('zoomed')  # Start maximized
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"

# Modern gradient colors
BG_DARK = "#0a0e27"
BG_MID = "#16213e"
CARD_BG = "#1a1d35"
ACCENT_BLUE = "#0096c7"
ACCENT_CYAN = "#00d4ff"
TEXT_WHITE = "#f0f4f8"
TEXT_GRAY = "#a5b4c9"
SUCCESS_GREEN = "#06ffa5"
HOVER_BG = "#252d4a"

window.configure(background=BG_DARK)

# Main container with gradient effect
main_container = tk.Frame(window, bg=BG_DARK)
main_container.pack(fill=BOTH, expand=True)

# ================== TOP BAR ==================
top_bar = tk.Frame(main_container, bg=BG_MID, height=80)
top_bar.pack(fill=X, side=TOP)
top_bar.pack_propagate(False)

# Logo and title section
logo_section = tk.Frame(top_bar, bg=BG_MID)
logo_section.pack(side=LEFT, padx=30, pady=15)

try:
    logo = Image.open("UI_Image/0001.png")
    logo = logo.resize((50, 50), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(logo_section, image=logo1, bg=BG_MID)
    logo_label.image = logo1
    logo_label.pack(side=LEFT, padx=(0, 15))
except:
    pass

title_label = tk.Label(
    logo_section,
    text="SmartAttend",
    bg=BG_MID,
    fg=TEXT_WHITE,
    font=("Segoe UI", 28, "bold")
)
title_label.pack(side=LEFT)

# Time display
time_frame = tk.Frame(top_bar, bg=BG_MID)
time_frame.pack(side=RIGHT, padx=30)

time_label = tk.Label(
    time_frame,
    text=datetime.datetime.now().strftime("%I:%M %p"),
    bg=BG_MID,
    fg=ACCENT_CYAN,
    font=("Segoe UI", 24, "bold")
)
time_label.pack()

date_label = tk.Label(
    time_frame,
    text=datetime.datetime.now().strftime("%B %d, %Y"),
    bg=BG_MID,
    fg=TEXT_GRAY,
    font=("Segoe UI", 11)
)
date_label.pack()

def update_time():
    time_label.config(text=datetime.datetime.now().strftime("%I:%M %p"))
    date_label.config(text=datetime.datetime.now().strftime("%B %d, %Y"))
    window.after(1000, update_time)
update_time()

# ================== MAIN CONTENT ==================
content_container = tk.Frame(main_container, bg=BG_DARK)
content_container.pack(fill=BOTH, expand=True, padx=40, pady=30)

# Welcome section
welcome_frame = tk.Frame(content_container, bg=BG_DARK)
welcome_frame.pack(fill=X, pady=(0, 40))

welcome_title = tk.Label(
    welcome_frame,
    text="AI-Powered Face Recognition",
    bg=BG_DARK,
    fg=TEXT_WHITE,
    font=("Segoe UI", 32, "bold")
)
welcome_title.pack()

welcome_subtitle = tk.Label(
    welcome_frame,
    text="Automated Attendance Management System",
    bg=BG_DARK,
    fg=TEXT_GRAY,
    font=("Segoe UI", 14)
)
welcome_subtitle.pack(pady=(5, 0))

# Cards container
cards_container = tk.Frame(content_container, bg=BG_DARK)
cards_container.pack(fill=BOTH, expand=True)

# Configure grid
for i in range(2):
    cards_container.grid_rowconfigure(i, weight=1)
for i in range(3):
    cards_container.grid_columnconfigure(i, weight=1)

# Modern card button creator
def create_card(parent, icon, title, subtitle, command, row, col, accent_color=ACCENT_BLUE):
    # Card frame
    card = tk.Frame(parent, bg=CARD_BG, highlightthickness=2, highlightbackground=accent_color)
    card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
    
    # Inner padding frame
    inner = tk.Frame(card, bg=CARD_BG)
    inner.pack(fill=BOTH, expand=True, padx=25, pady=30)
    
    # Icon
    icon_label = tk.Label(
        inner,
        text=icon,
        bg=CARD_BG,
        fg=accent_color,
        font=("Segoe UI", 48)
    )
    icon_label.pack(pady=(0, 15))
    
    # Title
    title_label = tk.Label(
        inner,
        text=title,
        bg=CARD_BG,
        fg=TEXT_WHITE,
        font=("Segoe UI", 18, "bold")
    )
    title_label.pack(pady=(0, 8))
    
    # Subtitle
    subtitle_label = tk.Label(
        inner,
        text=subtitle,
        bg=CARD_BG,
        fg=TEXT_GRAY,
        font=("Segoe UI", 11),
        wraplength=250
    )
    subtitle_label.pack()
    
    # Make card clickable
    def on_click(e):
        command()
    
    def on_enter(e):
        card.config(bg=HOVER_BG, highlightbackground=SUCCESS_GREEN)
        inner.config(bg=HOVER_BG)
        icon_label.config(bg=HOVER_BG, fg=SUCCESS_GREEN)
        title_label.config(bg=HOVER_BG)
        subtitle_label.config(bg=HOVER_BG)
    
    def on_leave(e):
        card.config(bg=CARD_BG, highlightbackground=accent_color)
        inner.config(bg=CARD_BG)
        icon_label.config(bg=CARD_BG, fg=accent_color)
        title_label.config(bg=CARD_BG)
        subtitle_label.config(bg=CARD_BG)
    
    for widget in [card, inner, icon_label, title_label, subtitle_label]:
        widget.bind("<Button-1>", on_click)
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.config(cursor="hand2")
    
    return card

# Create cards
create_card(cards_container, "👤", "Register Student", "Add new students to the system", TakeImageUI, 0, 0, ACCENT_BLUE)
create_card(cards_container, "✓", "Take Attendance", "Mark attendance manually", lambda: check_model_trained() and automated_attendance.subjectChoose(text_to_speech), 0, 1, ACCENT_CYAN)
create_card(cards_container, "🤖", "Auto Attendance", "Automated attendance system", lambda: check_model_trained() and automated_attendance_window(), 0, 2, "#7c3aed")
create_card(cards_container, "📊", "View Records", "View attendance reports", lambda: show_attendance.subjectchoose(text_to_speech), 1, 0, "#06ffa5")
create_card(cards_container, "📈", "Analytics", "Automated attendance analytics", view_automated_attendance, 1, 1, "#f59e0b")
create_card(cards_container, "🚪", "Exit", "Close the application", quit, 1, 2, "#ef4444")

# Footer
footer = tk.Frame(main_container, bg=BG_DARK, height=50)
footer.pack(fill=X, side=BOTTOM)

footer_label = tk.Label(
    footer,
    text="© 2025 SmartAttend • Powered by AI & Computer Vision",
    bg=BG_DARK,
    fg=TEXT_GRAY,
    font=("Segoe UI", 10)
)
footer_label.pack(pady=15)

window.mainloop()

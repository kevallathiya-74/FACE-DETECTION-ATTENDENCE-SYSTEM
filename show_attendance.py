import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject=="":
            t='Please enter the subject name.'
            text_to_speech(t)
            return
    
        # Check if main attendance file exists
        main_file = f"attendance\\{Subject}\\attendance.csv"
        
        if not os.path.exists(main_file):
            # Try to find session files
            filenames = glob(f"attendance\\{Subject}\\{Subject}*.csv")
            
            if not filenames:
                t=f'No attendance records found for {Subject}.'
                text_to_speech(t)
                return
            
            # Merge all session files
            df = [pd.read_csv(f) for f in filenames]
            newdf = df[0].copy()
            for i in range(1, len(df)):
                newdf = newdf.merge(df[i], how="outer")
            newdf.fillna(0, inplace=True)
        else:
            # Read the main attendance file
            newdf = pd.read_csv(main_file)
        
        # Identify date columns (columns that are not standard fields)
        standard_fields = ['Division', 'Enrollment', 'Roll Number', 'Name', 'Time', 'Attendance', 'Status', 'Roll']
        date_columns = [col for col in newdf.columns if col not in standard_fields]
        
        # Remove old problematic columns
        columns_to_remove = ['Time', 'Status', 'Division', 'Roll', 'Roll Number']
        for col in columns_to_remove:
            if col in newdf.columns and col not in ['Enrollment', 'Name']:
                newdf = newdf.drop(columns=[col])
        
        # Re-identify date columns after cleanup
        date_columns = [col for col in newdf.columns if col not in ['Enrollment', 'Name', 'Attendance']]
        
        # Print debug info
        print(f"Date columns found: {date_columns}")
        print(f"DataFrame shape: {newdf.shape}")
        print(f"DataFrame columns: {newdf.columns.tolist()}")
        
        # Initialize or update Attendance column
        if 'Attendance' not in newdf.columns:
            newdf["Attendance"] = ""
        
        # Calculate attendance percentage for each student
        for i in range(len(newdf)):
            if date_columns:
                # Get only date columns
                attendance_values = newdf.loc[i, date_columns]
                # Convert to numeric, replacing any non-numeric values with 0
                numeric_values = pd.to_numeric(attendance_values, errors='coerce').fillna(0)
                # Calculate percentage (values should be 0 or 1)
                if len(numeric_values) > 0:
                    total_days = len(numeric_values)
                    present_days = numeric_values.sum()
                    attendance_pct = round((present_days / total_days) * 100, 2)
                    newdf.loc[i, "Attendance"] = f"{attendance_pct:.2f}%"
                    print(f"Student {i}: Present {present_days}/{total_days} days = {attendance_pct}%")
                else:
                    newdf.loc[i, "Attendance"] = "0.00%"
            else:
                newdf.loc[i, "Attendance"] = "0.00%"
        
        # Reorder columns: Enrollment, Name, date columns, Attendance
        final_columns = ['Enrollment', 'Name'] + date_columns + ['Attendance']
        newdf = newdf[final_columns]
        
        newdf.to_csv(f"attendance\\{Subject}\\attendance.csv", index=False)

        root = tkinter.Tk()
        root.title(f"SmartAttend - {Subject} Attendance Report")
        root.state('zoomed')  # Maximize window
        
        # Modern colors
        BG_DARK = "#0a0e27"
        BG_MID = "#16213e"
        CARD_BG = "#1a1d35"
        ACCENT_BLUE = "#0096c7"
        TEXT_WHITE = "#f0f4f8"
        TEXT_GRAY = "#a5b4c9"
        ROW_EVEN = "#1f2540"
        ROW_ODD = "#252d4a"
        
        root.configure(background=BG_DARK)
        
        # Main container
        container = tk.Frame(root, bg=BG_DARK)
        container.pack(fill=BOTH, expand=True, padx=40, pady=30)
        
        # Header
        header = tk.Frame(container, bg=BG_DARK)
        header.pack(fill=X, pady=(0, 25))
        
        # Title
        title_frame = tk.Frame(header, bg=BG_DARK)
        title_frame.pack(side=LEFT)
        
        tk.Label(
            title_frame,
            text=f"📊 {Subject}",
            bg=BG_DARK,
            fg=TEXT_WHITE,
            font=("Segoe UI", 32, "bold")
        ).pack(anchor="w")
        
        tk.Label(
            title_frame,
            text=f"Total Students: {len(newdf)} • Attendance Report",
            bg=BG_DARK,
            fg=TEXT_GRAY,
            font=("Segoe UI", 13)
        ).pack(anchor="w", pady=(5, 0))
        
        # Table card
        table_card = tk.Frame(container, bg=CARD_BG, highlightthickness=3, highlightbackground=ACCENT_BLUE)
        table_card.pack(fill=BOTH, expand=True)
        
        # Scrollable frame
        scroll_frame = tk.Frame(table_card, bg=CARD_BG)
        scroll_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)
        
        # Scrollbars
        h_scroll = tk.Scrollbar(scroll_frame, orient=HORIZONTAL, bg=CARD_BG)
        h_scroll.pack(side=BOTTOM, fill=X)
        
        v_scroll = tk.Scrollbar(scroll_frame, orient=VERTICAL, bg=CARD_BG)
        v_scroll.pack(side=RIGHT, fill=Y)
        
        # Canvas
        canvas = tk.Canvas(
            scroll_frame,
            bg=CARD_BG,
            highlightthickness=0,
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set
        )
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        h_scroll.config(command=canvas.xview)
        v_scroll.config(command=canvas.yview)
        
        # Table frame
        table_frame = tk.Frame(canvas, bg=CARD_BG)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")
        
        cs = f"attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:
                    # Header row
                    if r == 0:
                        label = tkinter.Label(
                            table_frame,
                            width=15,
                            height=2,
                            fg=TEXT_WHITE,
                            font=("Segoe UI", 12, "bold"),
                            bg=ACCENT_BLUE,
                            text=row,
                            relief=tkinter.FLAT,
                            padx=10,
                            pady=8
                        )
                    else:
                        # Data rows with alternating colors
                        bg_color = ROW_EVEN if r % 2 == 0 else ROW_ODD
                        label = tkinter.Label(
                            table_frame,
                            width=15,
                            height=1,
                            fg=TEXT_WHITE,
                            font=("Segoe UI", 11),
                            bg=bg_color,
                            text=row,
                            relief=tkinter.FLAT,
                            padx=10,
                            pady=10
                        )
                    label.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                    c += 1
                r += 1
        
        # Update canvas scroll region
        table_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        root.mainloop()
        print(newdf)

    subject = Tk()
    subject.title("SmartAttend - View Attendance")
    subject.geometry("900x650")
    
    # Modern colors
    BG_DARK = "#0a0e27"
    CARD_BG = "#1a1d35"
    ACCENT_BLUE = "#0096c7"
    TEXT_WHITE = "#f0f4f8"
    TEXT_GRAY = "#a5b4c9"
    INPUT_BG = "#252d4a"
    
    subject.configure(background=BG_DARK)
    subject.resizable(1, 1)
    
    # Main container
    main_frame = tk.Frame(subject, bg=BG_DARK)
    main_frame.pack(fill=BOTH, expand=True, padx=50, pady=40)
    
    # Header
    header_frame = tk.Frame(main_frame, bg=BG_DARK)
    header_frame.pack(fill=X, pady=(0, 30))
    
    # Icon
    icon_label = tk.Label(
        header_frame,
        text="📊",
        bg=BG_DARK,
        fg=ACCENT_BLUE,
        font=("Segoe UI", 56)
    )
    icon_label.pack()
    
    title_label = tk.Label(
        header_frame,
        text="View Attendance",
        bg=BG_DARK,
        fg=TEXT_WHITE,
        font=("Segoe UI", 36, "bold")
    )
    title_label.pack(pady=(10, 5))
    
    subtitle_label = tk.Label(
        header_frame,
        text="Select a subject to view attendance records and statistics",
        bg=BG_DARK,
        fg=TEXT_GRAY,
        font=("Segoe UI", 12)
    )
    subtitle_label.pack()
    
    # Card frame
    card_frame = tk.Frame(main_frame, bg=CARD_BG, highlightthickness=3, highlightbackground=ACCENT_BLUE)
    card_frame.pack(fill=BOTH, expand=True, pady=20)
    
    # Input frame
    input_frame = tk.Frame(card_frame, bg=CARD_BG)
    input_frame.pack(pady=60, padx=50)
    
    # Subject label
    sub_label = tk.Label(
        input_frame,
        text="Subject Name:",
        bg=CARD_BG,
        fg=TEXT_WHITE,
        font=("Segoe UI", 16, "bold")
    )
    sub_label.pack(pady=(0, 20))
    
    # Subject entry
    tx = tk.Entry(
        input_frame,
        width=35,
        bg=INPUT_BG,
        fg=TEXT_WHITE,
        font=("Segoe UI", 16),
        relief="flat",
        bd=0,
        insertbackground=TEXT_WHITE,
        highlightthickness=2,
        highlightbackground="#2a3f5f",
        highlightcolor=ACCENT_BLUE,
        justify=CENTER
    )
    tx.pack(ipady=15, pady=(0, 40))

    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
            f"attendance\\{sub}"
            )

    # Buttons frame
    btn_frame = tk.Frame(input_frame, bg=CARD_BG)
    btn_frame.pack()
    
    # Modern button creator
    def create_button(parent, text, command, bg_color, icon=""):
        btn = tk.Button(
            parent,
            text=f"{icon} {text}",
            command=command,
            bg=bg_color,
            fg="#ffffff",
            font=("Segoe UI", 13, "bold"),
            relief="flat",
            bd=0,
            padx=35,
            pady=14,
            cursor="hand2",
            highlightthickness=0
        )
        
        hover_colors = {
            "#0096c7": "#0077a3",
            "#06ffa5": "#05e094",
        }
        hover_color = hover_colors.get(bg_color, bg_color)
        
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        
        return btn
    
    # Buttons
    view_btn = create_button(btn_frame, "View Attendance", calculate_attendance, "#0096c7", "📊")
    view_btn.pack(side=LEFT, padx=15)
    
    folder_btn = create_button(btn_frame, "Open Folder", Attf, "#06ffa5", "📁")
    folder_btn.pack(side=LEFT, padx=15)
    
    subject.mainloop()

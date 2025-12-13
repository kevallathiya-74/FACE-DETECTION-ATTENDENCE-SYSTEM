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
    
        filenames = glob(
            f"attendance\\{Subject}\\{Subject}*.csv"
        )
        
        # Check if any attendance files exist
        if not filenames:
            t=f'No attendance records found for {Subject}.'
            text_to_speech(t)
            return
            
        df = [pd.read_csv(f) for f in filenames]
        
        # Check if dataframes were loaded
        if not df:
            t=f'No attendance records found for {Subject}.'
            text_to_speech(t)
            return
            
        newdf = df[0].copy()
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        
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
                    attendance_pct = round(numeric_values.mean() * 100, 2)
                    newdf.loc[i, "Attendance"] = f"{attendance_pct:.2f}%"
                else:
                    newdf.loc[i, "Attendance"] = "0.00%"
            else:
                newdf.loc[i, "Attendance"] = "0.00%"
        
        # Reorder columns: Enrollment, Name, date columns, Attendance
        final_columns = ['Enrollment', 'Name'] + date_columns + ['Attendance']
        newdf = newdf[final_columns]
        
        newdf.to_csv(f"attendance\\{Subject}\\attendance.csv", index=False)

        root = tkinter.Tk()
        root.title("Attendance of "+Subject)
        root.configure(background="black")
        cs = f"attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:

                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
            f"attendance\\{sub}"
            )


    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()

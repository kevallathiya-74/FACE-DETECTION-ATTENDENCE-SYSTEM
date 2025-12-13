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
import tkinter.ttk as tkk
import tkinter.font as font
import pyttsx3

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "models\\Trainner.yml"
trainimage_path = "training_images"
studentdetail_path = "student_details\\studentdetails.csv"
attendance_path = "attendance"

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

def get_current_slot():
    current_time = datetime.datetime.now().time()
    slots = {
        "Slot 1": (datetime.time(7, 0), datetime.time(8, 0)),
        "Slot 2": (datetime.time(8, 20), datetime.time(9, 0)),
        "Slot 3": (datetime.time(9, 20), datetime.time(10, 0)),
        "Slot 4": (datetime.time(10, 20), datetime.time(11, 0)),
        "Slot 5": (datetime.time(11, 20), datetime.time(12, 0)),
        "Slot 6": (datetime.time(12, 20), datetime.time(13, 0)),
        "Slot 7": (datetime.time(13, 20), datetime.time(14, 0))
    }
    
    for slot_name, (start_time, end_time) in slots.items():
        if start_time <= current_time <= end_time:
            return slot_name
    return None

def take_attendance_for_slot(slot_name, subject):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(trainimagelabel_path)
        except:
            e = "Model not found, please train model"
            return e
            
        facecasCade = cv2.CascadeClassifier(haarcasecade_path)
        df = pd.read_csv(studentdetail_path)
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Updated columns for attendance
        col_names = ["Division", "Enrollment", "Roll Number", "Name", "Time"]
        attendance = pd.DataFrame(columns=col_names)
        
        start_time = time.time()
        duration = 10  # Changed from 60 to 10 seconds duration for attendance
        
        while time.time() - start_time < duration:
            ___, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = facecasCade.detectMultiScale(gray, 1.2, 5)
            
            for (x, y, w, h) in faces:
                Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                if conf < 70:
                    ts = time.time()
                    time_stamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                    
                    # Get student details from CSV
                    student_info = df.loc[df["Enrollment"] == Id]
                    if not student_info.empty:
                        division = student_info["Division"].values[0]
                        roll_number = student_info["Roll Number"].values[0]
                        name = student_info["Name"].values[0]
                        
                        # Check if student already marked present
                        if not attendance["Enrollment"].isin([Id]).any():
                            attendance.loc[len(attendance)] = [
                                division,
                                Id,
                                roll_number,
                                name,
                                time_stamp
                            ]
                            text_to_speech(f"Attendance marked for {name}")
                            
                        cv2.rectangle(im, (x, y), (x+w, y+h), (0, 260, 0), 4)
                        cv2.putText(im, str(name), (x+h, y), font, 1, (255, 255, 0), 4)
                    else:
                        cv2.rectangle(im, (x, y), (x+w, y+h), (0, 25, 255), 7)
                        cv2.putText(im, "Unknown", (x+h, y), font, 1, (0, 25, 255), 4)
                else:
                    cv2.rectangle(im, (x, y), (x+w, y+h), (0, 25, 255), 7)
                    cv2.putText(im, "Unknown", (x+h, y), font, 1, (0, 25, 255), 4)
            
            cv2.imshow(f"Taking Attendance for {slot_name}", im)
            key = cv2.waitKey(30) & 0xFF
            if key == 27:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        
        # Save attendance to CSV
        if not attendance.empty:
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            time_stamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            Hour, Minute, Second = time_stamp.split(":")
            
            path = os.path.join(attendance_path, subject)
            if not os.path.exists(path):
                os.makedirs(path)
            
            # Save detailed session file
            fileName = f"{path}/{subject}_{slot_name}_{date}_{Hour}-{Minute}-{Second}.csv"
            attendance.to_csv(fileName, index=False)
            
            # Update main attendance file with date column
            main_attendance_file = os.path.join(path, "attendance.csv")
            
            # Create attendance update with date column
            attendance_update = pd.DataFrame({
                'Enrollment': attendance['Enrollment'],
                'Name': attendance['Name'],
                date: [1] * len(attendance)  # Mark present with 1
            })
            
            if os.path.exists(main_attendance_file):
                # Read existing attendance
                existing_df = pd.read_csv(main_attendance_file)
                
                # Remove old Attendance column if it exists
                if 'Attendance' in existing_df.columns:
                    existing_df = existing_df.drop(columns=['Attendance'])
                
                # Remove Time column if it exists  
                if 'Time' in existing_df.columns:
                    existing_df = existing_df.drop(columns=['Time'])
                
                # Merge with new attendance
                merged_df = existing_df.merge(
                    attendance_update,
                    on=['Enrollment', 'Name'],
                    how='outer'
                )
                
                # Fill NaN with 0 (absent)
                merged_df = merged_df.fillna(0)
                
                # Save updated attendance
                merged_df.to_csv(main_attendance_file, index=False)
            else:
                # Create new attendance file
                attendance_update.to_csv(main_attendance_file, index=False)
            
            return f"Attendance saved successfully for {slot_name}"
        else:
            return "No attendance was recorded"
            
    except Exception as e:
        return f"Error: {str(e)}"

def start_automated_attendance(subject, duration=10):
    try:
        # Create directory for subject if it doesn't exist
        subject_dir = f"attendance/{subject}"
        if not os.path.exists(subject_dir):
            os.makedirs(subject_dir)
        
        # Initialize face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(trainimagelabel_path)
        except:
            return "Error: Model not trained. Please train the model first."
        
        # Load student details
        try:
            df = pd.read_csv(studentdetail_path)
        except:
            return "Error: No student details found"
        
        # Initialize camera
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return "Error: Could not open camera"
        
        # Initialize variables
        font = cv2.FONT_HERSHEY_SIMPLEX
        attendance_data = []
        marked_students = set()
        faceCascade = cv2.CascadeClassifier(haarcasecade_path)
        
        # Get current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Start time
        start_time = time.time()
        
        while time.time() - start_time < 10:
            ret, frame = cam.read()
            if not ret:
                continue
                
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            
            for (x, y, w, h) in faces:
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Recognize face
                face = gray[y:y+h, x:x+w]
                try:
                    Id, conf = recognizer.predict(face)
                    
                    if conf < 70:  # If confidence is less than 70, we have a match
                        # Get student details
                        student_info = df.loc[df["Enrollment"] == Id]
                        if not student_info.empty and Id not in marked_students:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            name = student_info["Name"].values[0]
                            
                            attendance_data.append({
                                'Time': current_time,
                                'Division': student_info["Division"].values[0],
                                'Enrollment': Id,
                                'Roll': student_info["Roll Number"].values[0],
                                'Name': name,
                                'Status': 'Present'
                            })
                            marked_students.add(Id)
                            
                            # Display name and add voice feedback
                            cv2.putText(frame, f"Name: {name}", (x, y-10), font, 0.75, (0, 255, 0), 2)
                            text_to_speech(f"Attendance marked for {name}")
                        else:
                            cv2.putText(frame, "Already Marked", (x, y-10), font, 0.75, (0, 255, 255), 2)
                    else:
                        cv2.putText(frame, "Unknown", (x, y-10), font, 0.75, (0, 0, 255), 2)
                except:
                    cv2.putText(frame, "Processing...", (x, y-10), font, 0.75, (255, 0, 0), 2)
            
            # Show remaining time
            remaining_time = int(10 - (time.time() - start_time))
            cv2.putText(frame, f"Time left: {remaining_time}s", (10, 30), font, 1, (0, 255, 255), 2)
            
            # Display frame
            cv2.imshow('Automated Attendance', frame)
            
            # Break if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release camera and close windows
        cam.release()
        cv2.destroyAllWindows()
        
        # Save attendance data
        if attendance_data:
            # Create main attendance file path
            main_attendance_file = os.path.join(attendance_path, subject, "attendance.csv")
            
            # Convert attendance data to DataFrame
            new_attendance_df = pd.DataFrame(attendance_data)
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Create a simplified DataFrame with just the essential columns
            attendance_update = pd.DataFrame({
                'Enrollment': new_attendance_df['Enrollment'],
                'Name': new_attendance_df['Name'],
                current_date: [1] * len(new_attendance_df)  # Mark present with 1
            })
            
            if os.path.exists(main_attendance_file):
                # Read existing attendance data
                existing_df = pd.read_csv(main_attendance_file)
                
                # If the date column already exists, drop it from existing data
                if current_date in existing_df.columns:
                    existing_df = existing_df.drop(columns=[current_date])
                
                # Merge without duplicate columns
                merged_df = existing_df.merge(
                    attendance_update,
                    on=['Enrollment', 'Name'],
                    how='outer'
                )
                
                # Fill NaN values with 0 (absent)
                merged_df = merged_df.fillna(0)
                
                # Save updated attendance
                merged_df.to_csv(main_attendance_file, index=False)
            else:
                # For new attendance file
                attendance_update.to_csv(main_attendance_file, index=False)
            
            # Save detailed session data separately
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            session_file = f"{attendance_path}/{subject}/session_{timestamp}.csv"
            new_attendance_df.to_csv(session_file, index=False)
            
            return f"Attendance recorded successfully for {len(attendance_data)} students"
        else:
            return "No attendance recorded"
            
    except Exception as e:
        return f"Error: {str(e)}"

def subjectChoose(text_to_speech_func):
    """UI for choosing subject and taking attendance"""
    import tkinter as tk
    from tkinter import END
    
    subject_window = tk.Tk()
    subject_window.title("Take Attendance")
    subject_window.geometry("400x250")
    subject_window.configure(background="#1c1c1c")
    subject_window.resizable(0, 0)
    
    # Title
    tk.Label(
        subject_window,
        text="Take Attendance",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 20, "bold")
    ).pack(pady=20)
    
    # Subject entry frame
    entry_frame = tk.Frame(subject_window, bg="#1c1c1c")
    entry_frame.pack(pady=20)
    
    tk.Label(
        entry_frame,
        text="Subject:",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 12)
    ).pack(side="left", padx=10)
    
    subject_entry = tk.Entry(
        entry_frame,
        width=20,
        bg="#333333",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat"
    )
    subject_entry.pack(side="left", padx=10)
    
    # Notification label
    notification = tk.Label(
        subject_window,
        text="",
        bg="#1c1c1c",
        fg="#00ff00",
        font=("Verdana", 10),
        wraplength=350
    )
    notification.pack(pady=10)
    
    def start_attendance():
        subject = subject_entry.get().strip()
        if not subject:
            notification.configure(text="Please enter a subject name!", fg="yellow")
            text_to_speech_func("Please enter subject name")
            return
        
        notification.configure(text=f"Starting attendance for {subject}...", fg="#00ff00")
        subject_window.update()
        
        # Take attendance using current slot
        current_slot = get_current_slot()
        if current_slot:
            result = take_attendance_for_slot(current_slot, subject)
        else:
            # Fallback to simple attendance without slot
            result = take_attendance_for_slot("General", subject)
        
        notification.configure(text=result)
        text_to_speech_func(result)
    
    # Take Attendance button
    tk.Button(
        subject_window,
        text="Take Attendance",
        command=start_attendance,
        bg="#2c2c2c",
        fg="#00ff00",
        font=("Verdana", 12),
        relief="flat",
        padx=20,
        pady=10
    ).pack(pady=20)
    
    subject_window.mainloop() 
import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from train_image import TrainImage

# Initialize the student details CSV file if it doesn't exist
def initialize_csv():
    if not os.path.exists("student_details"):
        os.makedirs("student_details")
    
    csv_file = "student_details/studentdetails.csv"
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Division", "Enrollment", "Roll Number", "Name"])

def detect_eyes_and_blink(gray, face_x, face_y, face_w, face_h):
    """Simplified eye detection and blink check"""
    # Load both cascade classifiers
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eye_tree_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
    
    # Define the eye region (upper half of face)
    roi_gray = gray[face_y:face_y + int(face_h/2), face_x:face_x + face_w]
    roi_gray = cv2.equalizeHist(roi_gray)
    
    # Try both classifiers
    eyes1 = eye_cascade.detectMultiScale(
        roi_gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(25, 25)
    )
    
    eyes2 = eye_tree_cascade.detectMultiScale(
        roi_gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(25, 25)
    )
    
    # Combine detected eyes
    eyes = np.vstack([eyes1, eyes2]) if len(eyes1) > 0 and len(eyes2) > 0 else eyes1 if len(eyes1) > 0 else eyes2
    
    # If we detect eyes, check their average intensity
    if len(eyes) >= 2:
        eye_intensities = []
        for (ex, ey, ew, eh) in eyes[:2]:  # Only check first two eyes
            eye_roi = roi_gray[ey:ey + eh, ex:ex + ew]
            intensity = np.mean(eye_roi)
            eye_intensities.append(intensity)
        
        # If average intensity is low, eyes might be closed
        avg_intensity = np.mean(eye_intensities)
        return len(eyes), avg_intensity
    
    return len(eyes), 0

# take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    # Initialize CSV file first
    initialize_csv()
    
    if (l1 == "") and (l2==""):
        t='Please Enter the your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1=='':
        t='Please Enter the your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t='Please Enter the your Name.'
        text_to_speech(t)
    else:
        try:
            # Check if student already exists
            df = pd.read_csv("student_details/studentdetails.csv")
            if l1 in df['Enrollment'].values:
                F = "Student Data already exists"
                text_to_speech(F)
                return
            
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            os.makedirs(path, exist_ok=True)
            
            # Initialize variables for blink detection
            blink_count = 0
            last_blink_time = time.time()
            eyes_closed = False
            start_time = time.time()
            
            # Store intensity history
            intensity_history = []
            
            while True:
                ret, img = cam.read()
                if not ret:
                    continue
                
                # Resize and enhance image
                img = cv2.resize(img, None, fx=1.2, fy=1.2)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                
                # Detect faces
                faces = detector.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(100, 100)
                )
                
                current_time = time.time()
                elapsed_time = current_time - start_time
                
                # Draw helper rectangle
                h, w = img.shape[:2]
                cv2.rectangle(img, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 0), 2)
                
                if len(faces) > 0:
                    # Use the largest face
                    face = max(faces, key=lambda x: x[2] * x[3])
                    x, y, w, h = face
                    
                    # Check if face is centered
                    face_center = (x + w//2, y + h//2)
                    frame_center = (img.shape[1]//2, img.shape[0]//2)
                    is_centered = abs(face_center[0] - frame_center[0]) < 100 and abs(face_center[1] - frame_center[1]) < 100
                    
                    if is_centered:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        
                        # Detect eyes and check blink
                        num_eyes, intensity = detect_eyes_and_blink(gray, x, y, w, h)
                        
                        # Store intensity
                        if num_eyes >= 2:
                            intensity_history.append(intensity)
                            if len(intensity_history) > 10:
                                intensity_history.pop(0)
                        
                        # Detect blink using intensity changes
                        if len(intensity_history) >= 3:
                            if not eyes_closed and intensity < min(intensity_history[:-1]) * 0.8:
                                eyes_closed = True
                            elif eyes_closed and intensity > max(intensity_history[:-1]) * 0.8:
                                eyes_closed = False
                                if current_time - last_blink_time > 0.5:  # Minimum time between blinks
                                    blink_count += 1
                                    last_blink_time = current_time
                        
                        # Display status
                        if blink_count >= 2:
                            status = "Blink detected! Capturing images..."
                            color = (0, 255, 0)
                            
                            # Capture image
                            if sampleNum < 50:
                                sampleNum += 1
                                image_path = os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg")
                                cv2.imwrite(image_path, gray[y:y + h, x:x + w])
                        else:
                            status = f"Blinks detected: {blink_count}/2 - Please blink naturally"
                            color = (0, 255, 255)
                    else:
                        status = "Please center your face in the green box"
                        color = (0, 165, 255)
                else:
                    status = "No face detected - Please look at the camera"
                    color = (0, 0, 255)
                
                # Display status and remaining time
                cv2.putText(img, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                if blink_count < 2:
                    time_left = max(0, 30 - int(elapsed_time))
                    cv2.putText(img, f"Time left: {time_left}s", (10, 60), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Display progress
                cv2.putText(img, f"Images: {sampleNum}/50", (10, 90),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                cv2.imshow("Registration - Please look at camera and blink naturally", img)
                
                # Exit conditions
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif sampleNum >= 50:
                    break
                elif elapsed_time > 30 and blink_count < 2:
                    break
            
            cam.release()
            cv2.destroyAllWindows()
            
            # Only save data if we captured enough images
            if sampleNum >= 50:
                # Add new student data with default division and roll number
                new_student = pd.DataFrame({
                    'Division': ['A'],  # Default division
                    'Enrollment': [Enrollment],
                    'Roll Number': [Enrollment],  # Using enrollment as roll number
                    'Name': [Name]
                })
                df = pd.concat([df, new_student], ignore_index=True)
                df.to_csv("student_details/studentdetails.csv", index=False)
                
                res = "Images Saved for ER No:" + Enrollment + " Name:" + Name
                message.configure(text=res)
                text_to_speech(res)
                
                # Train the model after successful registration
                trainimagelabel_path = "models/Trainner.yml"
                TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech)
            else:
                res = "Registration failed. Please try again."
                message.configure(text=res)
                text_to_speech(res)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            F = "Error saving student data"
            text_to_speech(F)

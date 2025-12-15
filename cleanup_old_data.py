import os
import shutil

def cleanup_old_data():
    """Remove all old training data, models, and CSV files"""
    
    print("Starting cleanup process...\n")
    
    # 1. Remove training images
    training_images_path = "training_images"
    if os.path.exists(training_images_path):
        try:
            shutil.rmtree(training_images_path)
            os.makedirs(training_images_path)
            print("✓ Cleared training images folder")
        except Exception as e:
            print(f"✗ Error clearing training images: {e}")
    
    # 2. Remove trained model
    model_path = "models/Trainner.yml"
    if os.path.exists(model_path):
        try:
            os.remove(model_path)
            print("✓ Removed trained model (Trainner.yml)")
        except Exception as e:
            print(f"✗ Error removing model: {e}")
    
    # 3. Clear student details CSV
    student_csv = "student_details/studentdetails.csv"
    if os.path.exists(student_csv):
        try:
            with open(student_csv, 'w', newline='') as f:
                f.write("Division,Enrollment,Roll Number,Name\n")
            print("✓ Cleared student details CSV")
        except Exception as e:
            print(f"✗ Error clearing student CSV: {e}")
    
    # 4. Remove all attendance CSV files
    attendance_path = "attendance"
    if os.path.exists(attendance_path):
        try:
            for subject_folder in os.listdir(attendance_path):
                subject_path = os.path.join(attendance_path, subject_folder)
                if os.path.isdir(subject_path):
                    # Remove all CSV files in subject folder
                    for file in os.listdir(subject_path):
                        if file.endswith('.csv'):
                            os.remove(os.path.join(subject_path, file))
            print("✓ Cleared all attendance CSV files")
        except Exception as e:
            print(f"✗ Error clearing attendance files: {e}")
    
    print("\n✅ Cleanup completed successfully!")
    print("You can now start fresh with new student registrations.")

if __name__ == "__main__":
    confirm = input("⚠️  WARNING: This will delete ALL training data, models, and CSV files.\nAre you sure you want to continue? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        cleanup_old_data()
    else:
        print("Cleanup cancelled.")

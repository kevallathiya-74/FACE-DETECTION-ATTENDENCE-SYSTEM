# 🎓 Attendance Management System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

A comprehensive **Face Recognition-based Attendance Management System** built with Python, OpenCV, and Tkinter. This system automates attendance tracking using facial recognition technology, eliminating manual attendance processes and providing real-time data management.

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Functionality
- ✅ **Face Registration** - Register students with enrollment details and facial data
- ✅ **Automated Face Detection** - Real-time face detection using Haar Cascade Classifier
- ✅ **Face Recognition** - LBPH (Local Binary Patterns Histograms) algorithm for accurate recognition
- ✅ **Attendance Tracking** - Automated attendance marking with timestamp
- ✅ **Slot-based System** - Time-slot based attendance management
- ✅ **Multi-subject Support** - Separate attendance records for different subjects
- ✅ **Attendance Reports** - View and export attendance data in CSV format
- ✅ **Text-to-Speech** - Voice feedback for system actions
- ✅ **Modern UI** - Clean, dark-themed graphical user interface

### Security & Data Management
- 🔒 Secure student data storage
- 📊 CSV-based data persistence
- 📈 Attendance percentage calculation
- 🔄 Real-time data updates

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core programming language |
| **OpenCV** | Computer vision and face recognition |
| **Tkinter** | GUI framework |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computing |
| **Pillow (PIL)** | Image processing |
| **pyttsx3** | Text-to-speech conversion |

## 💻 System Requirements

### Hardware Requirements
- **Camera**: Webcam or external camera (minimum 720p recommended)
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Processor**: Intel Core i3 or equivalent

### Software Requirements
- **Operating System**: Windows 10/11, Linux, or macOS
- **Python**: Version 3.9 or higher
- **Webcam Drivers**: Latest camera drivers installed

## 📦 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/Attendance-Management-System.git
cd Attendance-Management-System
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import cv2; print('OpenCV Version:', cv2.__version__)"
```

## 🚀 Usage Guide

### Running the Application
```bash
python attendance.py
```

### Complete Workflow

#### 1️⃣ **Register New Student**
1. Click **"Register New Student"** button
2. Fill in the required details:
   - Division (e.g., CS5, IT3)
   - Enrollment Number (unique ID)
   - Roll Number
   - Student Name
3. Click **"Take Image"** button
4. Position your face in the camera frame
5. System captures 50+ images automatically
6. Wait for confirmation message

#### 2️⃣ **Train the Model**
1. After registering students, click **"Train Image"** button
2. Wait for the training process to complete
3. Model will be saved in `TrainingImageLabel/` directory
4. You'll hear a voice confirmation

#### 3️⃣ **Take Attendance**
1. Click **"Take Attendance"** button
2. Enter the subject name (e.g., Python, Mathematics)
3. Camera will open for 10 seconds
4. System automatically recognizes faces and marks attendance
5. Attendance saved in `Attendance/{subject}/` directory

#### 4️⃣ **View Attendance**
1. Click **"View Attendance"** button
2. Enter subject name
3. View consolidated attendance report with percentages

### Time Slots
The system supports 7 predefined time slots:
- **Slot 1**: 07:00 - 08:00
- **Slot 2**: 08:20 - 09:00
- **Slot 3**: 09:20 - 10:00
- **Slot 4**: 10:20 - 11:00
- **Slot 5**: 11:20 - 12:00
- **Slot 6**: 12:20 - 13:00
- **Slot 7**: 13:20 - 14:00

## 📁 Project Structure

```
Attendance-Management-System/
│
├── attendance.py                 # Main application entry point
├── automated_attendance.py       # Attendance taking logic with slots
├── takeImage.py                  # Image capture module
├── trainImage.py                 # Model training module
├── show_attendance.py            # Attendance viewing module
│
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
│
├── haarcascade_frontalface_default.xml  # Face detection model
│
├── TrainingImage/                # Captured student images (gitignored)
│   └── {EnrollmentNo}_*.jpg
│
├── TrainingImageLabel/           # Trained models (gitignored)
│   └── Trainner.yml
│
├── StudentDetails/               # Student information (gitignored)
│   └── studentdetails.csv
│
├── Attendance/                   # Attendance records (gitignored)
│   ├── {subject}/
│   │   ├── attendance.csv       # Main attendance file
│   │   └── session_*.csv        # Individual session records
│
├── Project Snap/                 # Screenshots and demos
└── UI_Image/                     # UI assets
```

## 🔧 How It Works

### 1. Face Detection
The system uses **Haar Cascade Classifier** to detect faces in real-time from the webcam feed.

### 2. Face Recognition
**LBPH (Local Binary Patterns Histograms)** algorithm is used for face recognition:
- Creates a histogram of local binary patterns
- Compares with trained model
- Returns confidence score (lower is better)

### 3. Training Process
```
Captured Images → Grayscale Conversion → Feature Extraction → Model Training → Save Model
```

### 4. Recognition Process
```
Camera Input → Face Detection → Feature Extraction → Compare with Model → Identify Student → Mark Attendance
```

### 5. Data Flow
```
Student Registration → Image Capture → Model Training → Attendance Taking → Data Storage → Report Generation
```

## 📸 Screenshots

### Main Dashboard
![Main Dashboard](Project%20Snap/1.PNG)

### Student Registration
![Registration](Project%20Snap/registration.png)

### Taking Attendance
![Attendance](Project%20Snap/attendance.png)

### Attendance Report
![Report](Project%20Snap/7.PNG)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Include error handling
- Update README for new features

## 📝 To-Do / Future Enhancements

- [ ] Add database support (MySQL/PostgreSQL)
- [ ] Implement user authentication system
- [ ] Add email notifications for absent students
- [ ] Create web-based dashboard
- [ ] Add mobile app support
- [ ] Implement attendance analytics and graphs
- [ ] Add export to PDF functionality
- [ ] Multi-camera support
- [ ] Cloud storage integration

## ⚠️ Troubleshooting

### Camera Not Working
```bash
# Check camera access
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Model Training Fails
- Ensure at least one student is registered
- Check TrainingImage folder has images
- Verify image format is correct

### Recognition Accuracy Issues
- Improve lighting conditions
- Take more training images (50+ recommended)
- Ensure face is clearly visible
- Re-train the model

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- OpenCV community for excellent documentation
- Python community for amazing libraries
- Contributors and testers

## 📞 Support

For support, email your.email@example.com or open an issue on GitHub.

---

<div align="center">
Made with ❤️ by [Your Name]

⭐ Star this repository if you find it helpful!
</div>#   F A C E - D E T E C T I O N - A T T E N D E N C E - S Y S T E M  
 
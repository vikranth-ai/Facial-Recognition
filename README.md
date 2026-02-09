# Face Recognition Attendance System

A real-time attendance management system using facial recognition technology, built with Python, Flask, OpenCV, and MySQL.

## 📋 Overview

This project implements an automated attendance system that uses face recognition to mark attendance. The system captures faces through a webcam, compares them against a database of registered users, and automatically records attendance with timestamps in a MySQL database.

## ✨ Features

- **Real-time Face Recognition**: Detects and recognizes faces using computer vision
- **Automated Attendance Marking**: Automatically records attendance when a registered face is detected
- **User Management**: Easy registration of new users with webcam capture
- **Daily Attendance Tables**: Creates separate tables for each day's attendance records
- **Web Interface**: Clean, responsive UI built with Flask and Bootstrap
- **Live Clock Display**: Shows current date and time on the dashboard
- **Duplicate Prevention**: Ensures each person is marked present only once per day
- **Visual Feedback**: Displays attendance records in real-time

## 🛠️ Technologies Used

- **Python 3.12**: Core programming language
- **Flask**: Web framework for the application
- **OpenCV (cv2)**: Computer vision and image processing
- **face_recognition**: Face detection and recognition library
- **MySQL**: Database for storing user and attendance data
- **Bootstrap 5**: Frontend UI framework
- **NumPy**: Numerical operations for face encoding

## 📁 Project Structure

```
├── app.py                    # Main Flask application
├── attendanceSystem.py       # Standalone attendance script (CSV-based)
├── connection.py             # MySQL database connection handler
├── test.py                   # Testing script with visual feedback
├── templates/
│   ├── home.html            # Main dashboard template
│   └── add_user.html        # User registration template
├── faces/                   # Directory storing user face images
└── attendance.csv           # CSV-based attendance log (legacy)
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- Webcam

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/vikranth-ai/Face-Recognition.git
   cd face-recognition-attendance
   ```

2. **Install required packages**
   ```bash
   pip install flask opencv-python face-recognition mysql-connector-python numpy
   ```

3. **Set up MySQL database**
   ```sql
   CREATE DATABASE attendance;
   USE attendance;
   
   CREATE TABLE users (
       name VARCHAR(30),
       id VARCHAR(30)
   );
   ```

4. **Update database credentials**
   
   Edit the database connection settings in `app.py`:
   ```python
   mydb = mysql.connector.connect(
       host="localhost",
       user="your_username",
       password="your_password",
       database="attendance"
   )
   ```

5. **Create faces directory**
   ```bash
   mkdir faces
   ```

## 💻 Usage

### Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   
   Open your browser and navigate to: `http://localhost:5000`

### Adding New Users

1. Navigate to the "Add New User" section on the home page
2. Enter the user's name and ID
3. Click "Add New User" button
4. Position your face in front of the webcam
5. Press 's' to capture and save the image
6. The system will save the face image and register the user

### Taking Attendance

1. Click the "Take Attendance" button on the home page
2. The webcam will activate and start detecting faces
3. Registered faces will be automatically recognized and marked present
4. Press 'q' to stop the attendance session
5. View the attendance records in the table on the dashboard

## 📊 Database Schema

### users table
| Column | Type | Description |
|--------|------|-------------|
| name | VARCHAR(30) | User's name |
| id | VARCHAR(30) | User's ID number |

### att_DD_MM_YYYY tables (Created daily)
| Column | Type | Description |
|--------|------|-------------|
| name | VARCHAR(30) | User's name |
| id | VARCHAR(30) | User's ID number |
| time | VARCHAR(10) | Time of attendance |

## 🔧 Configuration

### Face Recognition Parameters

- **Distance Threshold**: 0.6 (adjustable in code for stricter/looser matching)
- **Face Encoding Model**: Default HOG-based detector
- **Image Format**: JPG/PNG supported

### File Naming Convention

Face images are stored as: `{name}_{id}.jpg`

## 🎯 Use Cases

- Educational institutions (schools, colleges, universities)
- Corporate offices
- Training centers
- Events and conferences
- Examination halls
- Any organization requiring automated attendance tracking

## ⚠️ Known Limitations

- Requires good lighting conditions for optimal face detection
- Single face capture per user registration
- Database credentials stored in plain text (should use environment variables in production)
- No authentication/authorization system implemented

## 🔜 Future Enhancements

- [ ] Multi-face registration per user
- [ ] Export attendance to Excel/PDF
- [ ] Email notifications for attendance reports
- [ ] Admin dashboard with analytics
- [ ] User authentication system
- [ ] REST API for mobile app integration
- [ ] Cloud deployment support
- [ ] Attendance reports and statistics

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 👨‍💻 Author

Your Name - [GitHub Profile](https://github.com/vikranth-ai)

## 🙏 Acknowledgments

- face_recognition library by Adam Geitgey
- OpenCV community
- Flask documentation

---

import cv2
import face_recognition
import numpy as np
import os
import datetime
import mysql.connector
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="neeraj@123",
    database="attendance"
)
cursor = mydb.cursor()

# Helper: Load known faces from 'faces' folder
def load_known_faces():
    known_faces = []
    known_names = []
    known_ids = []
    for filename in os.listdir('faces'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            path = os.path.join('faces', filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_faces.append(encodings[0])
                name, id_part = os.path.splitext(filename)[0].rsplit('_', 1)
                known_names.append(name)
                known_ids.append(id_part)
    return known_faces, known_names, known_ids

@app.route('/')
def index():
    today_table = 'att_' + datetime.date.today().strftime("%d_%m_%Y")
    try:
        cursor.execute(f"SELECT name, id, time FROM {today_table}")
        rows = cursor.fetchall()
        names, rolls, times = zip(*rows) if rows else ([], [], [])
    except:
        names, rolls, times = [], [], []
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    return render_template("home.html", names=names, rolls=rolls, times=times, l=len(names),
                           totalreg=total_users, today=datetime.date.today().strftime('%d-%m-%Y'))

@app.route('/start')
def take_attendance():
    known_faces, known_names, known_ids = load_known_faces()
    attendance_marked = set()

    cap = cv2.VideoCapture(0)

    today_table = 'att_' + datetime.date.today().strftime("%d_%m_%Y")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {today_table} (
            name VARCHAR(30),
            id VARCHAR(30),
            time VARCHAR(10)
        )
    """)
    mydb.commit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[!] Camera error")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, locations)

        for face_encoding in encodings:
            distances = face_recognition.face_distance(known_faces, face_encoding)
            if len(distances) == 0:
                continue

            best_match_index = np.argmin(distances)
            if distances[best_match_index] < 0.6:
                name = known_names[best_match_index]
                user_id = known_ids[best_match_index]

                if name not in attendance_marked:
                    current_time = datetime.datetime.now().strftime('%H:%M:%S')
                    cursor.execute(f"SELECT * FROM {today_table} WHERE name = %s", (name,))
                    if cursor.fetchone() is None:
                        cursor.execute(f"INSERT INTO {today_table} (name, id, time) VALUES (%s, %s, %s)",
                                       (name, user_id, current_time))
                        mydb.commit()
                        attendance_marked.add(name)

        cv2.imshow("Taking Attendance - Press 'q' to exit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Fetch all attendance entries from today's table
    cursor.execute(f"SELECT name, id, time FROM {today_table}")
    rows = cursor.fetchall()
    names, rolls, times = zip(*rows) if rows else ([], [], [])

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    return render_template("home.html", names=names, rolls=rolls, times=times, l=len(names),
                           totalreg=total_users, today=datetime.date.today().strftime('%d-%m-%Y'))

@app.route('/add', methods=['POST'])
def add_user():
    username = request.form['newusername']
    userid = request.form['newuserid']
    filename = f"{username}_{userid}.jpg"

    # Capture from webcam
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[!] Failed to capture")
            break

        cv2.imshow("Capture Face - Press 's' to Save", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(os.path.join("faces", filename), frame)
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save to users table
    cursor.execute("INSERT INTO users (name, id) VALUES (%s, %s)", (username, userid))
    mydb.commit()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

import cv2
import mysql.connector
import os
import face_recognition
import datetime

# Load known faces
known_faces = []
known_names = []

for filename in os.listdir('faces'):
    image_path = os.path.join('faces', filename)
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) > 0:
        known_faces.append(encodings[0])
        known_names.append(os.path.splitext(filename)[0])
    else:
        print(f"[!] No face found in {filename}. Skipping...")

# Initialize video
video_capture = cv2.VideoCapture(0)
attendance_marked = set()

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="neeraj@123",
    database="attendance"
)

# Get today's date for table name
today = 'att_' + datetime.date.today().strftime("%d_%m_%Y")

# Create table if it doesn't exist
cursor = mydb.cursor()
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {today} (
        name VARCHAR(30),
        time VARCHAR(10)
    )
""")
mydb.commit()
cursor.close()

# Start capturing frames
while True:
    ret, frame = video_capture.read()
    if not ret:
        print("[!] Failed to read from camera")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = face_distances.argmin() if len(face_distances) > 0 else None

        name = "Unknown"
        if best_match_index is not None and face_distances[best_match_index] < 0.6:
            name = known_names[best_match_index]

            if name not in attendance_marked:
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                cursor = mydb.cursor()
                cursor.execute(f"SELECT * FROM {today} WHERE name = %s", (name,))
                result = cursor.fetchone()

                if result is None:
                    cursor.execute(f"INSERT INTO {today} (name, time) VALUES (%s, %s)", (name, current_time))
                    mydb.commit()
                    attendance_marked.add(name)

                cursor.close()

        # Draw face rectangle and name
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Attendance System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

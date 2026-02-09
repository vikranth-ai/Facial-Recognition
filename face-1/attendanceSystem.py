import cv2
import csv
import os
import face_recognition
import datetime

from face_recognition import face_encodings

#load known faces and their names from the 'faces' folder
known_faces=[]
known_names=[]

for filename in os.listdir('faces'):
    image = face_recognition.load_image_file(os.path.join('faces', filename))
    encoding=face_recognition.face_encodings(image)[0]

    if len(encoding) > 0:
        known_faces.append(encoding[0])
        known_names.append(os.path.splitext(filename)[0])
    else:
        print(f"⚠️ Warning: No face found in {filename}. Skipping...")

video_capture = cv2.VideoCapture(0)

attendance_marked = False

while True:
    ret, frame = video_capture.read()

    rgb_frame = frame[:, :, ::-1]

    face_locations =  face_recognition.face_locations(rgb_frame)
    face_encodings = []
    for face_location in face_locations:
        try:
            encodings = face_recognition.face_encodings(rgb_frame, [face_location])
            if encodings:
                face_encodings.append(encodings[0])
        except Exception as e:
            print(f"⚠️ Skipping a face due to error: {e}")

    recognized_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces,face_encoding)
        face_distances = face_recognition.face_distance(known_faces, face_encoding,tolerance=0.6)
        print("Distances:", face_distances)
        name = 'Unknown'

        if True in matches:
            matched_indices = [i for i, match in enumerate(matches) if match]
            for index in matched_indices:
                name = known_names[index]
                recognized_names.append(name)


    if len(recognized_names)>0:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        with open('attendance.csv','r') as file:
            reader = csv.reader(file)
            existing_names = set(row[0] for row in reader)
        with open('attendance.csv','a',newline='') as file:
            writer = csv.writer(file)
            for name in recognized_names:
                if name not in existing_names:
                    writer.writerow([name, current_time])
                    existing_names.add(name)

        attendance_marked = True


    cv2.imshow('camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or attendance_marked:
        break

video_capture.release()
cv2.destroyAllWindows()

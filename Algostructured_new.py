import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import csv
import pandas as pd
import random
from utils.attendace_write import read_student_data, write_to_csv
from utils.email_automation import sendmail
from utils.draw_border import draw_border
from utils.calcuclate_final import calculate
import time

# video_capture = cv2.VideoCapture('http://192.168.176.196:8080/video')
video_capture = cv2.VideoCapture(2)


def Find_attend(known_face_encodings,known_face_names,current_minute):
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    c=0
    l2={}
    l1=[]
    timestamp_dict = {}
    _,frame=video_capture.read()
    lt = [1400,1550,1550,1700]
    a,b = lt[0],lt[1]
    if current_minute == 2:
        a,b = lt[2],lt[3]
    
    while _:
        ret, frame = video_capture.read()
        c+=1
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,model="large")

            face_names = []
            for face_encoding in face_encodings:

                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                l1.append(name)
                face_names.append(name)
                if name not in timestamp_dict:
                    timestamp_dict[name] = [time.time()]
                else:
                    timestamp_dict[name].append(time.time())
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            draw_border(frame, (left, top), (right, bottom), (255, 0, 0), 2, 10, 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    
    attendee = calculate(l1,l2,timestamp_dict)
    print(attendee)
    student_data_file = 'attendance/input.csv'
    output_file = 'attendance/output.csv'
    student_data = read_student_data(student_data_file)

    write_to_csv(attendee, student_data, output_file)
    sendmail()
    return attendee
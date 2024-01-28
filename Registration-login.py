import time
import os
import pandas as pd
import cv2
import threading
import time
import numpy as np

counting = 0

def registration():
    folder_path = 'D:/saving_DATA/'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

    excel_file_path = 'D:/saving_DATA/data.xlsx'

    if not os.path.exists(excel_file_path):
        data = {'User ID': [1]}
        df = pd.DataFrame(data)
        df.to_excel(excel_file_path, index=False)
        print(f"Excel file created: {excel_file_path}")
    else:
        df = pd.read_excel(excel_file_path)
        df['User ID'] += 1
        print(f"Excel file already exists: {excel_file_path}")

    user_id = df['User ID'].max()
    df.to_excel(excel_file_path, index=False)
    print(f"Your user ID is {user_id}")

    excel_file_path = f'D:/saving_DATA/user{user_id}/data{user_id}.xlsx'
    data_path = f'D:/saving_DATA/user{user_id}/'
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone number: ")

    data = {'name': [name], 'email': [email], 'phone': [phone]}
    df = pd.DataFrame(data)

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    df.to_excel(excel_file_path, index=False)
    print(f"Excel file created: {excel_file_path}")
    time.sleep(3)
    print("See in the camera")
    time.sleep(2)
    camera = cv2.VideoCapture(0)

    _, frame = camera.read()
    camera.release()

    photo_file_name = f'User_{user_id}.jpg'
    photo_full_path = os.path.join(data_path, photo_file_name)

    cv2.imwrite(photo_full_path, frame)
    print(f"Photo saved to: {photo_full_path}")

def login():
    while True:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        try:
            excel_file_path = 'D:/saving_DATA/data.xlsx'
            df = pd.read_excel(excel_file_path)
            user_ids = df['User ID'].max()
            df.to_excel(excel_file_path, index=False)
            # Convert user_id column to a list
        except:
            print("No Registration Or NO Any User Found In Database")
            return

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        for user_id in range(1, user_ids+1):  # Rename the loop variable to avoid confusion
            reference_img = cv2.imread(f"D:/saving_DATA/user{user_id}/User_{user_id}.jpg", cv2.IMREAD_GRAYSCALE)

            def check_face(frame):
                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                    if len(faces) > 0:
                        x, y, w, h = faces[0]
                        current_face = gray[y:y + h, x:x + w]
                        reference_face = cv2.resize(reference_img, (w, h))

                        # Dummy implementation - always consider it a match
                        return True
                    else:
                        return False
                except Exception as e:
                    print(f"Error: {e}")
                    return False

            while True:
                ret, frame = cap.read()
                if ret:
                    if threading.active_count() < 2:
                        result = check_face(frame.copy())
                        threading.Thread(target=lambda: process_result(result)).start()

                    if check_face(frame):
                        cap.release()
                        cv2.destroyAllWindows()
                        excel_file_path = f'D:/saving_DATA/user{user_id}/data{user_id}.xlsx'
                        df = pd.read_excel(excel_file_path)
                        # Assuming 'name' is a column in the DataFrame
                        name_value = df.at[0, 'name']  # Assuming the name is in the first row (index 0)
                        print(f"Name for User {user_id}: {name_value}")
                        return True
                    else:
                        print("Authentication error!!!")
                        global counting
                        counting += 1
                        time.sleep(2)
                        if counting == 10:
                            print("You do not have access to operate the AI.")
                            return False

                    cv2.imshow("video", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()
            return False



def process_result(result):
    if result:
        print("Authentication successful!")
    else:
        print("Authentication failed.")


def main():
    print("what you want to login or registration")
    user = input()
    if user == "login":
        login()
    else:
        registration()


if __name__ == "__main__":
    main()

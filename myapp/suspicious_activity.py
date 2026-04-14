# import cv2
# import requests
# import time
#
# URL = "http://127.0.0.1:8000/myapp/check_stranger_api/"
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#
# cap = cv2.VideoCapture(0)
# last_check_time = 0
#
# while True:
#     ret, frame = cap.read()
#     if not ret: break
#
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#
#     # If a face is found, check every 3 seconds
#     if len(faces) > 0 and (time.time() - last_check_time > 3):
#         last_check_time = time.time()
#
#         # Encode and send to Django
#         _, img_encoded = cv2.imencode('.jpg', frame)
#         files = {'image': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
#
#         try:
#             response = requests.post(URL, files=files)
#             print("Server Response:", response.json())
#         except Exception as e:
#             print("Connection Error:", e)
#
#     # Draw box for visual feedback
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#
#     cv2.imshow("Stranger Detection Mode", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'): break
#
# cap.release()
# cv2.destroyAllWindows()
import cv2
import requests
import time
import threading

URL = "http://127.0.0.1:8000/myapp/check_stranger_api/"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
last_check_time = 0
is_processing = False  # Flag to prevent overlapping requests


def send_to_django(frame_to_send):
    global is_processing
    try:
        _, img_encoded = cv2.imencode('.jpg', frame_to_send)
        files = {'image': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}

        # Increased timeout to 20s because AI is slow
        response = requests.post(URL, files=files, timeout=20)
        print("Server Response:", response.json())
    except requests.exceptions.ReadTimeout:
        print("Error: Server took too long (AI Processing).")
    except Exception as e:
        print("Network Error:", e)
    finally:
        is_processing = False  # Allow the next request to go through


while True:
    ret, frame = cap.read()
    if not ret: break

    # Only do detection logic if we aren't currently waiting for the server
    if not is_processing:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Check every 3 seconds IF a face is present
        if len(faces) > 0 and (time.time() - last_check_time > 3):
            last_check_time = time.time()
            is_processing = True  # Lock the process

            # Start background thread
            thread = threading.Thread(target=send_to_django, args=(frame.copy(),))
            thread.daemon = True
            thread.start()
    else:
        # Optionally, detect faces anyway just for the visual boxes
        # but don't send to server
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw visual feedback
    for (x, y, w, h) in faces:
        color = (0, 255, 0) if is_processing else (255, 0, 0)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        if is_processing:
            cv2.putText(frame, "Checking AI...", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Stranger Detection Mode", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
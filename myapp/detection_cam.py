# import cv2
# import torch
# import numpy as np
# from transformers import VideoMAEImageProcessor, VideoMAEForVideoClassification
# from collections import deque
#
# # -----------------------------
# # Load Pretrained VideoMAE Model
# # -----------------------------
# model_name = "MCG-NJU/videomae-base-finetuned-kinetics"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#
# processor = VideoMAEImageProcessor.from_pretrained(model_name)
# model = VideoMAEForVideoClassification.from_pretrained(model_name)
# model.to(device)
# model.eval()
#
# # -----------------------------
# # Video Capture
# # -----------------------------
# cap = cv2.VideoCapture(0)  # 0 for webcam
#
# # Store 16 frames (required by model)
# frame_buffer = deque(maxlen=16)
#
# print("Starting Violence Detection... Press Q to exit.")
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     # Resize frame to 224x224
#     frame_resized = cv2.resize(frame, (224, 224))
#     frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
#
#     frame_buffer.append(frame_rgb)
#
#     label_text = "Collecting frames..."
#
#     # When buffer is full (16 frames)
#     if len(frame_buffer) == 16:
#
#         # Convert to numpy
#         clip = list(frame_buffer)
#
#         inputs = processor(clip, return_tensors="pt")
#         inputs = {k: v.to(device) for k, v in inputs.items()}
#
#         with torch.no_grad():
#             outputs = model(**inputs)
#             logits = outputs.logits
#             predicted_class = torch.argmax(logits, dim=-1).item()
#
#         label = model.config.id2label[predicted_class]
#         label_text = f"Action: {label}"
#
#     # Display on screen
#     cv2.putText(frame,
#                 label_text,
#                 (20, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.8,
#                 (0, 0, 255),
#                 2)
#
#     cv2.imshow("Violence Detection (Transformer)", frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()


def send_loc(img,camid):
    import requests
    import os

    # Django API URL
    SERVER_URL = "http://127.0.0.1:8000/myapp/detect_noti/"

    # Camera ID
    CAM_ID = "CAM_01"

    # Path of saved image



    with open(img, "rb") as img_file:
        files = {
            "image": ("fight_frame.jpg", img_file, "image/jpeg")
        }

        data = {
            "cam_id": "1"
        }

        response = requests.post(SERVER_URL, files=files, data=data)

        try:
            print("Server Response:", response.json())
        except:
            print("Raw Response:", response.text)
import cv2
import torch
import numpy as np
from transformers import VideoMAEImageProcessor, VideoMAEForVideoClassification
from collections import deque

# -----------------------------
# Load Model
# -----------------------------
model_name = "MCG-NJU/videomae-base-finetuned-kinetics"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

processor = VideoMAEImageProcessor.from_pretrained(model_name)
model = VideoMAEForVideoClassification.from_pretrained(model_name)
model.to(device)
model.eval()

# -----------------------------
# Video Capture
# -----------------------------
cap = cv2.VideoCapture(0)  # Webcam
frame_buffer = deque(maxlen=16)

print("Fighting Detection Started... Press Q to Exit")

# Fight-related keywords
FIGHT_KEYWORDS = ["fight", "fighting", "punch", "kicking", "slap", "hit"]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_resized = cv2.resize(frame, (224, 224))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    frame_buffer.append(frame_rgb)

    label_text = "Collecting frames..."

    if len(frame_buffer) == 16:
        clip = list(frame_buffer)

        inputs = processor(clip, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=-1)
            predicted_class = torch.argmax(probs, dim=-1).item()

        predicted_label = model.config.id2label[predicted_class].lower()

        # Check if prediction contains fight keywords
        if any(word in predicted_label for word in FIGHT_KEYWORDS):
            label_text = "⚠️ FIGHTING DETECTED"
            cv2.imwrite("sample.png",frame)
            send_loc("sample.png","1")
            color = (0, 0, 255)
        else:
            label_text = "NORMAL"
            color = (0, 255, 0)

        cv2.putText(frame, label_text, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, color, 3)


    cv2.imshow("Fighting Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


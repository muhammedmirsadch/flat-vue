import os
import cv2
import django
import numpy as np
import datetime
from pygame import mixer
from tensorflow.keras.models import load_model
from django.core.mail import send_mail
from django.conf import settings

# -------------------- DJANGO SETUP --------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flatvue.settings")
django.setup()

from myapp.models import suspicious_activities, surveillance_camera

# -------------------- INITIALIZE --------------------
print("Starting Abnormal Activity Detection System...")

# Load CNN model ONLY ONCE
model = load_model("model1.h5")

# Initialize alarm
mixer.init()
ALARM_SOUND = "alarm.mp3"

# Camera ID from your surveillance_camera table
CAMERA_ID = 1

# Detection settings
FRAME_THRESHOLD = 10   # abnormal detected after 10 continuous frames
pred_count = 0

# Start webcam
cap = cv2.VideoCapture(0)

# -------------------- PREDICTION FUNCTION --------------------
def predict_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (48, 48))
    normalized = resized / 255.0
    reshaped = normalized.reshape(1, 48, 48, 1)
    prediction = model.predict(reshaped, verbose=0)
    return np.argmax(prediction)

# -------------------- MAIN LOOP --------------------
try:
    camera = surveillance_camera.objects.get(id=CAMERA_ID)
except surveillance_camera.DoesNotExist:
    print("Camera not found in database!")
    exit()

print("Camera started successfully...")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    prediction = predict_frame(frame)

    # If abnormal class = 1
    if prediction == 1:
        pred_count += 1
    else:
        pred_count = 0

    # If abnormal detected continuously
    if pred_count >= FRAME_THRESHOLD:
        print("🚨 ABNORMAL ACTIVITY DETECTED!")

        # Play alarm
        if os.path.exists(ALARM_SOUND):
            mixer.music.load(ALARM_SOUND)
            mixer.music.play()

        # Create filename
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d_%H%M%S") + ".jpg"

        # Ensure media folder exists
        save_dir = os.path.join(settings.MEDIA_ROOT, "suspicious")
        os.makedirs(save_dir, exist_ok=True)

        full_path = os.path.join(save_dir, filename)

        # Save image
        cv2.imwrite(full_path, frame)

        # Save to database
        suspicious_activities.objects.create(
            CAMERA=camera,
            image="suspicious/" + filename,
            date=datetime.date.today()
        )

        print("Image saved & database updated.")

        # Send Email Alert
        try:
            send_mail(
                subject="🚨 Abnormal Activity Detected",
                message="Suspicious activity detected in surveillance camera.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[camera.FLAT_OWNER.email],
                fail_silently=False,
            )
            print("Email alert sent successfully.")
        except Exception as e:
            print("Email sending failed:", e)

        pred_count = 0  # Reset counter

    # Show live feed
    cv2.imshow("Live Surveillance", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()
print("System Stopped.")
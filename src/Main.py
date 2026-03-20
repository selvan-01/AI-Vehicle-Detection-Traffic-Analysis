import cv2
import imutils

# ==============================
# CONFIGURATION
# ==============================
CASCADE_PATH = "models/cars.xml"
CAMERA_ID = 0
FRAME_WIDTH = 1000
TRAFFIC_THRESHOLD = 8

# ==============================
# LOAD MODEL
# ==============================
car_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# ==============================
# INITIALIZE CAMERA
# ==============================
cam = cv2.VideoCapture(CAMERA_ID)

if not cam.isOpened():
    print("❌ Error: Cannot access camera")
    exit()

# ==============================
# MAIN LOOP
# ==============================
while True:
    ret, frame = cam.read()

    if not ret:
        print("❌ Failed to grab frame")
        break

    # Resize frame
    frame = imutils.resize(frame, width=FRAME_WIDTH)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect vehicles
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    # Count vehicles
    vehicle_count = len(cars)

    # Draw bounding boxes
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # ==============================
    # TRAFFIC ANALYSIS
    # ==============================
    print("------------------------------------------------")
    print(f"Vehicle Count (North): {vehicle_count}")

    if vehicle_count >= TRAFFIC_THRESHOLD:
        traffic_status = "HIGH TRAFFIC - TURN RED SIGNAL"
        print("🚦 North More Traffic, Please turn ON RED Signal")
    else:
        traffic_status = "LOW TRAFFIC"
        print("✅ No Traffic")

    # ==============================
    # DISPLAY INFO ON SCREEN
    # ==============================
    cv2.putText(frame, f'Vehicles: {vehicle_count}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, traffic_status, (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # Show frame
    cv2.imshow("Vehicle Detection & Traffic Analysis", frame)

    # Exit on ESC key
    if cv2.waitKey(33) == 27:
        break

# ==============================
# RELEASE RESOURCES
# ==============================
cam.release()
cv2.destroyAllWindows()
import cv2
from cvzone.FaceDetectionModule import FaceDetector
import mediapipe as mp
import simpleaudio as sa
from flask import Flask, render_template, Response
import pyrebase

config = {
  "apiKey": "AIzaSyBLJURU5ZIcqswOnRIbWOVgxNztmP6qdro",
  "authDomain": "toggle-button-4087f.firebaseapp.com",
  "databaseURL": "https://toggle-button-4087f-default-rtdb.firebaseio.com",
  "projectId": "toggle-button-4087f",
  "storageBucket": "toggle-button-4087f.appspot.com",
  "messagingSenderId": "441033032973",
  "appId": "1:441033032973:web:98bae899e594302dc55c44",
  "measurementId": "G-CBSWK5B3Y5"
};

firebase = pyrebase.initialize_app(config)
database = firebase.database()

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

app = Flask(__name__)
camera = cv2.VideoCapture(0)

detector = FaceDetector()

Sound_1 = sa.WaveObject.from_wave_file('C:/Users/jagra/Desktop/SanProgram/Sound_2.wav')

def generate_frames():
    face_detected = False
    while True:
        try:
            success, frame = camera.read()
            if not success:
                print("Failed to read frame from camera.")
                break

            img, bBoxes = detector.findFaces(frame)
            image = cv2.flip(frame, 1)

            # Convert the BGR image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image and find hands
            results = hands.process(image_rgb)

            if bBoxes and not face_detected:
                print("Hello")
                # play_object = Sound_1.play()
                # play_object.wait_done()
                face_detected = True
            elif not bBoxes and face_detected:
                print("Nothing")
                face_detected = False

            # Convert back to BGR for OpenCV
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            # Draw hand landmarks and connections
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmarks = hand_landmarks.landmark

                    # Define a function to check if a finger is up
                    def is_finger_up(tip_id, pip_id):
                        return landmarks[tip_id].y < landmarks[pip_id].y

                    # List of finger tips and PIP (proximal interphalangeal) joints
                    finger_tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                   mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                                   mp_hands.HandLandmark.RING_FINGER_TIP,
                                   mp_hands.HandLandmark.PINKY_TIP]
                    finger_pips = [mp_hands.HandLandmark.INDEX_FINGER_PIP,
                                   mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                                   mp_hands.HandLandmark.RING_FINGER_PIP,
                                   mp_hands.HandLandmark.PINKY_PIP]

                    # Count fingers that are up
                    fingers_up = [is_finger_up(finger_tips[i], finger_pips[i]) for i in range(4)]
                    thumb_up = landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x

                    # Add thumb status
                    fingers_up.insert(0, thumb_up)

                    # Count the number of fingers up
                    num_fingers_up = fingers_up.count(True)

                    # Print the number of fingers up
                    print(num_fingers_up)
                    if num_fingers_up == 0:
                        data = {
                            "L1" : "0",
                            "L2" : "0",
                            "L3" : "0",
                            "L4" : "0",
                            "L5" : "0"
                        }
                        database.update(data)
                        print(num_fingers_up)

                    if num_fingers_up == 1:
                        data = {
                            "L1" : "1",
                            "L2" : "0",
                            "L3" : "0",
                            "L4" : "0",
                            "L5" : "0"
                        }
                        database.update(data)
                        print(num_fingers_up)

                    if num_fingers_up == 2:
                        data = {
                            "L1" : "0",
                            "L2" : "1",
                            "L3" : "0",
                            "L4" : "0",
                            "L5" : "0"
                        }
                        database.update(data)
                        print(num_fingers_up)
                    
                    if num_fingers_up == 3:
                        data = {
                            "L1" : "0",
                            "L2" : "0",
                            "L3" : "1",
                            "L4" : "0",
                            "L5" : "0"
                        }
                        database.update(data)
                        print(num_fingers_up)
                    
                    if num_fingers_up == 4:
                        data = {
                            "L1" : "0",
                            "L2" : "0",
                            "L3" : "0",
                            "L4" : "1",
                            "L5" : "0"
                        }
                        database.update(data)
                        print(num_fingers_up)
                    
                    if num_fingers_up == 5:
                        data = {
                            "L1" : "0",
                            "L2" : "0",
                            "L3" : "0",
                            "L4" : "0",
                            "L5" : "1"
                        }
                        database.update(data)
                        print(num_fingers_up)
                    

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    camera.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)

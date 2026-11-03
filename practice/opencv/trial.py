import cv2                                                                                          #for camera and drawing tool kit
import math                                                                                         #to calculate the position of thumb's landmark
import mediapipe as mp                                                                              #made the mediapipe library available in the code
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode        #tells the mediapipeline how to work
from mediapipe.tasks.python.core.base_options import BaseOptions                                    #the model itself

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def fist(hand):
    thumb_curled  = distance(hand[3],  hand[7])<0.10
    index_curled  = distance(hand[8],  hand[5])<0.10
    middle_curled = distance(hand[12], hand[9])<0.10
    ring_curled   = distance(hand[16], hand[13])<0.10
    pinky_curled  = distance(hand[20], hand[17])<0.10

    return thumb_curled and index_curled and middle_curled and ring_curled and pinky_curled

def point(hand):
    thumb_curled  = distance(hand[3],  hand[11])<0.10
    index_curled  = not (distance(hand[8],  hand[5])<0.10)
    middle_curled = distance(hand[12], hand[9])<0.10
    ring_curled   = distance(hand[16], hand[13])<0.10
    pinky_curled  = distance(hand[20], hand[17])<0.10

    return middle_curled and ring_curled and pinky_curled and thumb_curled and index_curled

def claw(hand):
    thumb_curled  = distance(hand[3],  hand[7])<0.10 
    index_curled  = distance(hand[8],  hand[6])<0.10 
    middle_curled = distance(hand[12], hand[10])<0.10 
    ring_curled   = distance(hand[16], hand[14])<0.10 
    pinky_curled  = distance(hand[20], hand[18])<0.10 

    return index_curled and middle_curled and ring_curled and pinky_curled 

def peace(hand):
    thumb_curled  = distance(hand[4],  hand[15])<0.10
    index_curled  = not (distance(hand[8],  hand[5])<0.10)
    middle_curled = not (distance(hand[12], hand[9])<0.10)
    ring_curled   = distance(hand[16], hand[13])<0.10
    pinky_curled  = distance(hand[20], hand[17])<0.10


    return thumb_curled  and ring_curled and pinky_curled and index_curled and middle_curled


# 1. SETUP
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),    #says where the model is located
    running_mode=RunningMode.VIDEO,                                       #doen't assume it as a single photo(uses motion tarcking for better accuracy)
    num_hands=1                                                           #to tell the code how many hands to look for
)
detector = HandLandmarker.create_from_options(options)                    #loads the model into RAM(reads the .task file, unpacks the model and prepare it to analysis images)

# 2. WEBCAM
cap = cv2.VideoCapture(0)         #opens the camera
frame_count = 0                   #to tell the model how many photos have been at what millisecond

# 3. LOOP
while True:
    ret, frame = cap.read()       #camera takes the photo and returns it as a frame
    if not ret:                   # to state that camera is working or not
        break
    
    frame = cv2.flip(frame, 1)                           #to flip the frame horizontally 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   #opencv knows BGR, mediapipe knows RGB. so, we convert it
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)   #frame needs to be stored in special format, won't accept raw numpy
    results = detector.detect_for_video(mp_image, frame_count * 33)         #looks at the frame and returns the results. 33 is the time between frames in milliseconds, so we multiply it by the frame count to get the time of the current frame
    frame_count += 1                                                        #increase the counter for the next loop
    
    if results.hand_landmarks:                                     #checks if hand is visible or not if yes it will execut the inside code if not then skip
        for hand in results.hand_landmarks:

            # --- Gesture classification ---
            if fist(hand):
                gesture = "RESET"
                color = (125, 125, 125)
            elif point(hand):
                gesture = "AIR"
                color = (0, 255, 0)
            elif peace(hand):
                gesture = "WATER"
                color = (255, 0, 0)
            elif claw(hand):
                gesture = "FIRE"
                color = (0, 0, 255)
            else:
                gesture = "UNKNOWN"
                color = (0, 0, 0)
    
            cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
    
    # --- JOB 2: Draw landmarks (21 times per hand) ---
            for i, landmark in enumerate(hand):
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, color, -1)  # All dots match the gesture color

    cv2.imshow("Hand Tracking", frame)       #to show the frame with the landmarks drawn on it
    if cv2.waitKey(1) & 0xFF == ord('q'):    #to check if the user pressed 'q' if yes loop will stop if not it will go on
        break

# 4. CLEANUP
cap.release()                #tells the code to sleep and let other apps use the camera
cv2.destroyAllWindows()      #closes all open cv window
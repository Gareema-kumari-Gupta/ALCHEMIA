import cv2
import math
import random
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
from mediapipe.tasks.python.core.base_options import BaseOptions


# ============ PARTICLE CLASS ============
class Particle:
    def __init__(self, x, y, element):
        self.x = x
        self.y = y
        self.life = 40
        self.element = element
        
        if element == "FIRE":
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-5, -2)
            self.color = (0, random.randint(50, 150), 255)
            self.size = random.randint(5, 10)
        elif element == "WATER":
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(2, 5)
            self.color = (255, random.randint(100, 200), 0)
            self.size = random.randint(3, 6)
        elif element == "AIR":
            self.vx = random.uniform(-6, 6)
            self.vy = random.uniform(-3, 3)
            self.color = (220, 220, 220)
            self.size = random.randint(2, 4)
        else:
            self.vx = 0
            self.vy = 0
            self.color = (128, 128, 128)
            self.size = 3
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vx += random.uniform(-0.2, 0.2)
        
        if self.element == "FIRE":
            self.vy += 0.05
        elif self.element == "WATER":
            self.vx += random.uniform(-0.3, 0.3)
    
    def draw(self, frame):
        if self.life > 0:
            radius = max(1, self.life // 5)
            cv2.circle(frame, (int(self.x), int(self.y)), radius, self.color, -1)


# ============ GESTURE FUNCTIONS ============
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def fist(hand):
    thumb_curled  = distance(hand[3],  hand[7]) < 0.10
    index_curled  = distance(hand[8],  hand[5]) < 0.10
    middle_curled = distance(hand[12], hand[9]) < 0.10
    ring_curled   = distance(hand[16], hand[13]) < 0.10
    pinky_curled  = distance(hand[20], hand[17]) < 0.10
    return thumb_curled and index_curled and middle_curled and ring_curled and pinky_curled

def point(hand):
    thumb_curled  = distance(hand[3],  hand[11]) < 0.10
    index_curled  = not (distance(hand[8],  hand[5]) < 0.10)
    middle_curled = distance(hand[12], hand[9]) < 0.10
    ring_curled   = distance(hand[16], hand[13]) < 0.10
    pinky_curled  = distance(hand[20], hand[17]) < 0.10
    return middle_curled and ring_curled and pinky_curled and thumb_curled and index_curled

def claw(hand):
    thumb_curled  = distance(hand[3],  hand[7]) < 0.10 
    index_curled  = distance(hand[8],  hand[6]) < 0.10 
    middle_curled = distance(hand[12], hand[10]) < 0.10 
    ring_curled   = distance(hand[16], hand[14]) < 0.10 
    pinky_curled  = distance(hand[20], hand[18]) < 0.10 
    return index_curled and middle_curled and ring_curled and pinky_curled 

def peace(hand):
    thumb_curled  = distance(hand[4],  hand[15]) < 0.10
    index_curled  = not (distance(hand[8],  hand[5]) < 0.10)
    middle_curled = not (distance(hand[12], hand[9]) < 0.10)
    ring_curled   = distance(hand[16], hand[13]) < 0.10
    pinky_curled  = distance(hand[20], hand[17]) < 0.10
    return thumb_curled and ring_curled and pinky_curled and index_curled and middle_curled


# ============ SETUP ============
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=RunningMode.VIDEO,
    num_hands=1
)
detector = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
particles = []
frame_count = 0  # <-- ADD THIS

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = detector.detect_for_video(mp_image, frame_count * 33)  # <-- FIX THIS
    frame_count += 1  # <-- ADD THIS
    
    # ... rest of your loop stays the same ...
    
    gesture = "UNKNOWN"
    color = (128, 128, 128)
    element = None
    
    if results.hand_landmarks:
        for hand_landmarks in results.hand_landmarks:
            
            if fist(hand_landmarks):
                gesture = "RESET"
                color = (128, 128, 128)
                particles = []
            elif point(hand_landmarks):
                gesture = "AIR"
                color = (0, 255, 0)
                element = "AIR"
            elif peace(hand_landmarks):
                gesture = "WATER"
                color = (255, 0, 0)
                element = "WATER"
            elif claw(hand_landmarks):
                gesture = "FIRE"
                color = (0, 0, 255)
                element = "FIRE"
            
            for landmark in hand_landmarks:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, color, -1)
            
            if element:
                spawn_x = int(hand_landmarks[9].x * frame.shape[1])
                spawn_y = int(hand_landmarks[9].y * frame.shape[0])
                for _ in range(3):
                    particles.append(Particle(spawn_x, spawn_y, element))
    
    for p in particles[:]:
        p.update()
        p.draw(frame)
        if p.life <= 0:
            particles.remove(p)
    
    cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
    cv2.putText(frame, f"Particles: {len(particles)}", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow("Element Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2

cap = cv2.VideoCapture(0)           # Open camera

while True:
    ret, frame = cap.read()             # Read ONE frame
    frame = cv2.flip(frame, 1)          # Mirror the frame horizontally

    height, width, _ = frame.shape
    cv2.rectangle(frame, (0, 0), (100, 100), (255, 0, 0), 3)                   #Draw a rectangle on the frame
    cv2.circle(frame, (width // 2, height // 2), 30, (0, 0, 255), -1)          # Draw a circle on the frame on the center of the frame
    text = f"{width} x {height}"
    cv2.putText(frame, text, (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)     #to add text on the frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                       #to convert coloured frame in grey scale

    cv2.imshow("Webcam", frame)            # Show that ONE frame
    cv2.imshow("Grayscale", gray_frame)    # Show that ONE frame in grayscale

    #print("Grey Frame",gray_frame.shape)
    #print("Normal Frame",frame.shape)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()                       # CLOSE the camera
cv2.destroyAllWindows()             # DESTROY the window
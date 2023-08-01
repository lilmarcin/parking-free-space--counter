
import numpy as np
import cv2
import pickle


cap = cv2.VideoCapture('car_parking.mp4')


# Open file with parking positions
with open('parking_positions', 'rb') as f:
    parking_positions = pickle.load(f)

# Parking position parameters
width, height = 18, 30
area = width * height
empty = 0.25

def space_counter(img):
    global counter

    counter = 0

    for position in parking_positions:
        x1, y1, x2, y2 = position

        # Crop parking position and count occupied pixels
        img_crop = img[y1:y2, x1:x2]
        count = cv2.countNonZero(img_crop)

        occupied_area = count / area

        # Empty space
        if occupied_area < empty:
            color = [0, 255, 0]
            counter += 1

        # Half-empty space (shadows/shifted frame)
        elif occupied_area >= empty and occupied_area <= 0.4:
            color = [0, 127, 255]

        # Busy space
        else:
            color = [0, 0, 255]

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.resize(frame, (1600, 900))
    # Frame processing
    # Gray scaling
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Gaussian bluring
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    # Thresholding
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 35, 20)
    # Median bluring
    img_blur=cv2.medianBlur(img_thresh, 5)
    # Dilating
    dilated_img = cv2.dilate(img_blur, np.ones((3,3),np.uint8))
    space_counter(dilated_img)

    alpha = 0.7
    frame_new = cv2.addWeighted(frame, alpha, frame, 1 - alpha, 0)

    w, h = 220, 30
    cv2.rectangle(frame_new, (0, 0), (w, h), (0, 255, 127), -1)
    cv2.putText(frame_new, f"Free: {counter}/{len(parking_positions)}", (0, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0, 0, 0), 2)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WINDOW_NORMAL, cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 1600, 900)

    cv2.imshow('frame', frame_new)
    # cv2.imshow('image_blur', img_blur)
    # cv2.imshow('image_thresh', img_thresh)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
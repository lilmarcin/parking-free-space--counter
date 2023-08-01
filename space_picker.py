import cv2
import pickle
from math import sqrt

# single dimensions of the parking space (in pixels)
width, height = 18, 30
pt1_x, pt1_y, pt2_x, pt2_y = None, None, None, None

window_width, window_height = 1600, 900

try:
    with open('/src/parking_positions', 'rb') as f:
        parking_pos = pickle.load(f)
except FileNotFoundError:
    parking_pos = []

def add_single_position(x, y):
    return [(x, y, x + width, y + height)]

def add_multiple_positions(x, y, n=10):
    positions = []
    for i in range(n):
        positions.append((x + i * width, y, x + (i + 1) * width, y + height))
    return positions


def mouse_events(event, x, y, flag, param):
    global pt1_x, pt1_y, pt2_x, pt2_y

    if event == cv2.EVENT_LBUTTONDOWN:
            parking_pos.extend(add_single_position(x, y))
    if event == cv2.EVENT_MBUTTONDOWN:
            parking_pos.extend(add_multiple_positions(x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(parking_pos):
            x1, y1, x2, y2 = position
            if x1 < x < x2 and y1 < y < y2:
                parking_pos.pop(i)

    with open('parking_positions', 'wb') as f:
        pickle.dump(parking_pos, f)


while True:
    img = cv2.imread('car_parking_random_frame.png')
    img = cv2.resize(img, (window_width, window_height))
    for position in parking_pos:
        x1, y1, x2, y2 = position
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 1)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', window_width, window_height)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', mouse_events)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
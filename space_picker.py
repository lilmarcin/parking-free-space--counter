import cv2
import pickle
from math import sqrt

width, height = 13, 26
pt1_x, pt1_y, pt2_x, pt2_y = None, None, None, None
line_count = 0

try:
    with open('parking_positions', 'rb') as f:
        parking_pos = pickle.load(f)
except:
    parking_pos = []


def mouse_events(event, x, y, flag, param):
    global pt1_x, pt1_y, pt2_x, pt2_y

    if event == cv2.EVENT_LBUTTONDOWN:
        pt1_x, pt1_y = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        pt2_x, pt2_y = x, y
        parking_pos.append((x, y))

    if event == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(parking_pos):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                parking_pos.pop(i)

    with open('parking_positions', 'wb') as f:
        pickle.dump(parking_pos, f)


while True:
    img = cv2.imread('car_parking_random_frame.png')

    for position in parking_pos:
        cv2.rectangle(img, position, (position[0] + width, position[1] + height), (255, 0, 255), 1)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)

    cv2.imshow('image', img)
    cv2.setMouseCallback('image', mouse_events)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
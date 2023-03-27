import cv2
import numpy as np

while True:
    img = cv2.imread('/images/car_parking_random_frame.png', -1)

    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        img_blur = cv2.GaussianBlur(plane, (5, 5), 1)
        img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 35, 20)
        img_blur=cv2.medianBlur(img_thresh, 5)
        dilated_img = cv2.dilate(img_blur, np.ones((3,3), np.uint8))
        result_planes.append(dilated_img)
        
    result = cv2.merge(result_planes)
    #result_norm = cv2.merge(result_norm_planes)

    #cv2.imshow('dilated_img', bg_img)
    cv2.imshow('blur.png', result)
    #cv2.imshow('shadows_out_norm.png', result_norm)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
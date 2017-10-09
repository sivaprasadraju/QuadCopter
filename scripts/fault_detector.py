import cv2
from matplotlib import pyplot as plt
import numpy as np

class FaultDetector:
    def isFaulty(self, img):
        cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
        params = cv2.SimpleBlobDetector_Params()
        params.maxCircularity = 0.92
        params.filterByInertia = True
        params.maxInertiaRatio = 0.6
        params.filterByColor = True
        params.filterByCircularity = True
        params.blobColor = 0
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(thresh)
        img = cv2.drawKeypoints(img, keypoints, np.array([]), (255, 0, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return (len(keypoints) > 0, img)
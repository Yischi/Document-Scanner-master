import cv2 as cv
import numpy as np
import os

class BackgroundSub:
    def __init__(self, frame):
        self._setupBackground(frame)

    def _setupBackground(self, frame):
        self.backSub = cv.createBackgroundSubtractorMOG2(0, 40,False)
        cv.imshow("init", frame)
        self.backSub.apply(frame)

    def apply(self, frame):
        frame2 = self.backSub.apply(frame)
        self._setupBackground(frame)
        return frame2


class BackgroundSub2:
    def __init__(self, frame):
        self._setupBackground(frame)

    def _setupBackground(self, frame):
        self.Background = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("init", frame)

    def apply(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #self.Background = self.Background + 20
        #frame2 = abs(int(self.Background) - int(frame))
        frame2 = cv.subtract(self.Background, frame)
        self.Background = frame
        return frame2

BASE = os.path.dirname(__file__)
ImagesPath = ["Sub1.jpg", "Sub2.jpg", "Sub3.jpg", "Sub4.jpg"]
Images = []
SubImage = []

for path in ImagesPath:
    Images.append(cv.imread(BASE + "/" + path))

BS = BackgroundSub2(Images[1])
BSImage = BS.apply(Images[3])

cv.imshow("BS", BSImage)

cv.waitKey(500000)
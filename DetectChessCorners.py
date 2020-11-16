import numpy as np
import cv2 as cv
import glob
import os

heightImg = 800
widthImg  = 1000

FieldSize = 100

BASE = os.path.dirname(__file__)
pathImage = "SchachBrett2.jpg"
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)

objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
img = cv.imread(BASE+ "/"+ pathImage) #glob.glob('*.jpg')
img = cv.resize(img, (widthImg, heightImg))

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# Find the chess board corners
ret, corners = cv.findChessboardCorners(gray, (7,7), None)
 # If found, add object points, image points (after refining them)
if ret == True:
    #get Corner Position of the 1. Rank
    #print(corners)
    leftupper = corners[6][0]
    leftlower = corners[48][0]
    rightupper = corners[42][0]
    rightlower = corners[0][0]

    #Transform Image with the founded Corner Position
    pts1 = np.float32([rightupper, rightlower, leftupper, leftlower])  # PREPARE POINTS FOR WARP
    print(pts1)
    pts2 = np.float32([[FieldSize, FieldSize*7], [FieldSize*7, FieldSize*7], [FieldSize*7, FieldSize], [FieldSize, FieldSize]])  # PREPARE POINTS FOR WARP
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv.warpPerspective(img, matrix, (FieldSize*8, FieldSize*8))

    #Draw founded Chess Corners
    imgContours = img.copy()
    objpoints.append(objp)
    corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
    imgpoints.append(corners)
    # Draw and display the corners
    cv.drawChessboardCorners(img, (7,7), corners2, ret)

else:
    ret, corners = cv.findChessboardCorners(gray, (5, 5), None)

#cv.imshow('img', img)
cv.imshow('img', imgWarpColored)

cv.waitKey(500000)

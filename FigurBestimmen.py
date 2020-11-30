import numpy as np
import cv2 as cv
import os

FieldSize = 100

def getImage():

    BASE = os.path.dirname(__file__)
    pathImage = "SchachBrett3.jpg"

    img = cv.imread(BASE + "/" + pathImage)  # glob.glob('*.jpg')

    return img

def TransformeImage(img):
    leftupper = [343, 298]
    leftlower = [297, 1272]
    rightupper = [1304, 347]
    rightlower = [1269, 1299]

    # Transform Image with the founded Corner Position
    pts1 = np.float32([rightlower, rightupper, leftupper, leftlower])  # PREPARE POINTS FOR WARP
    print(pts1)
    pts2 = np.float32([[FieldSize, FieldSize * 7], [FieldSize * 7, FieldSize * 7], [FieldSize * 7, FieldSize],
                       [FieldSize, FieldSize]])  # PREPARE POINTS FOR WARP
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv.warpPerspective(img, matrix, (FieldSize * 8, FieldSize * 8))

    return imgWarpColored

def getCornerPersentage(img, X,Y):
    foundedCorners = 0
    for x in range(FieldSize):
        for y in range(FieldSize):
            #print(img[X*FieldSize + x, Y*FieldSize +y])
            if img[X*FieldSize + x, Y*FieldSize +y] != 0:
                foundedCorners += 1

    print("X " + str(X) + " Y " + str(Y) + ": " + str(foundedCorners))
    return foundedCorners/ (FieldSize * FieldSize)

def main():
    img = getImage()
    imgCanny = cv.Canny(img, 100, 150)
    imgResult = TransformeImage(imgCanny)
    persentages = []
    for Y in range(8):
        rank = []
        for X in range(8):
            rank.append(getCornerPersentage(imgCanny, X,Y))
        persentages.append(rank)
    print(persentages)
    cv.imshow('img', imgResult)
    cv.waitKey(500000)


main()


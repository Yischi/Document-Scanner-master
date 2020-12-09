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

    toleranze = int(FieldSize * 0.1)
    foundedCorners = 0
    for x in range(FieldSize - 2 * toleranze):
        for y in range(FieldSize - 2 * toleranze):
            if img[X*FieldSize + x +toleranze, Y*FieldSize +y+ toleranze] != 0:
                foundedCorners += 1

    persentage = foundedCorners/ (FieldSize * FieldSize)
    print(persentage)
    return persentage > 0.02

def main():
    img = getImage()
    chessimg = TransformeImage(img)
    imgCanny = cv.Canny(chessimg, 100, 150)
    foundedPeases = []
    for Y in range(8):
        for X in range(8):
            if getCornerPersentage(imgCanny, Y,X):
                foundedPeases.append([X,Y])
    print(foundedPeases)
    for pos in foundedPeases:
        X = pos[0]
        Y = pos[1]
        imgResult = cv.rectangle(chessimg, (X * FieldSize, Y*FieldSize), ((X+1) * FieldSize, (Y+1) * FieldSize), (0, 255, 0), 6)

    cv.imshow('img', imgResult)
    cv.waitKey(500000)


main()


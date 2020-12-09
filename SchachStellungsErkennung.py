import cv2 as cv
import numpy as np

class SchachBild:
    def __init__(self, fieldSize):
        self.FieldSize = fieldSize
        self.Tolerance = int(fieldSize * 0.1)
        self.InnerField = fieldSize - 2 * self.Tolerance
        print("init fin")

    def _setupBackground(self, frame):
        self.backSub = cv.createBackgroundSubtractorKNN(1, 16, True)
        frame = self.filterChessboard(frame)
        self.backSub.apply(frame)

    def initialFrame(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        print(1)
        ret, corners = cv.findChessboardCorners(gray, (7, 7), None)
        print(2)
        if ret == True:
            # get Corner Position of the 1. Rank
            self.leftupper = corners[6][0]
            self.leftlower = corners[48][0]
            self.rightupper = corners[42][0]
            self.rightlower = corners[0][0]
            # PREPARE POINTS FOR Transformation
            pts1 = np.float32([self.rightupper, self.rightlower, self.leftupper, self.leftlower])
            pts2 = np.float32([[self.FieldSize, self.FieldSize * 7], [self.FieldSize * 7, self.FieldSize * 7],
                               [self.FieldSize * 7, self.FieldSize],
                               [self.FieldSize, self.FieldSize]])
            print(3)
            self.matrix = cv.getPerspectiveTransform(pts1, pts2)
            print("Calculated matrix")

            self._setupBackground(frame)
        else:
            print("NO CHECK BOARD")
        return ret

    def _useBackGroundSubtraction(self, frame):
        frame = self.backSub.apply(frame)
        return frame

    def filterChessboard(self, frame):
        return cv.warpPerspective(frame, self.matrix, (self.FieldSize * 8, self.FieldSize * 8))

    def _getCornerPersentage(self, img, X, Y):
        foundedCorners = 0
        for x in range(self.InnerField):
            for y in range(self.InnerField):
                # print(img[X*FieldSize + x, Y*FieldSize +y])
                if img[X*self.FieldSize + x + self.Tolerance, Y*self.FieldSize +y+ self.Tolerance] != 0:
                    foundedCorners += 1

        persentage = foundedCorners / (self.FieldSize * self.FieldSize)
        print(persentage)
        return persentage > 0.02

    def findChessPeases(self, frame):
        frame = self.filterChessboard(frame)
        frame = self._useBackGroundSubtraction(frame)

        #imgCanny = cv.Canny(frame, 100, 150)
        foundedFigures = []
        for Y in range(8):
            for X in range(8):
                if self._getCornerPersentage(frame, X, Y):
                    foundedFigures.append([X,Y])
        return foundedFigures, frame

    def draw(self,img,  X, Y):
        img = cv.rectangle(img, (X * self.FieldSize, Y *self.FieldSize), ((X+1)*self.FieldSize, (Y+1)*self.FieldSize), (0, 255, 0), 3)
        return img





def main():
    # Open the device at the ID 0

    cap = cv.VideoCapture(1)

    # Check whether user selected camera is opened successfully.

    if not (cap.isOpened()):
        print("ERROR")

    # To set the resolution

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 2000)

    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2000)

    #take init frame
    while(True):
        ret, frame = cap.read()
        cv.imshow("preview", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            schachBild = SchachBild(100)
            print("test")
            ret = schachBild.initialFrame(frame)
            if ret:
                print("init schachBild")
                break

    #show chess board
    ChessBoard = schachBild.filterChessboard(frame)
    cv.imshow("preview", ChessBoard)
    print("showed schachBild")



    while (True):

        # Capture frame-by-frame

        ret, frame = cap.read()
        if ret:

            if cv.waitKey(1) & 0xFF == ord("w"):
                # find peases in frame
                foundPeases, frame = schachBild.findChessPeases(frame)
                print(foundPeases)
                #mark founded peases
                for pos in foundPeases :
                    frame = schachBild.draw(frame, pos[0], pos[1])

                # Display the resulting frame
                cv.imshow("preview", frame)
                print("new Frame")
                while True:
                    if cv.waitKey(1) & 0xFF == ord("q"):
                        break

            else:
                frame = schachBild.filterChessboard(frame)
                #frame = schachBild._useBackGroundSubtraction(frame)
        cv.imshow("preview", frame)
        print("new Frame")
        # Waits for a user input to quit the application

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    # When everything done, release the capture

    cap.release()

    cv.destroyAllWindows()

main()
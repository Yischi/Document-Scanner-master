import cv2 as cv
import numpy as np

class SchachBild:
    def __init__(self, fieldSize):
        self.FieldSize = fieldSize
        print("init fin")


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
        else:
            print("NO CHECK BOARD")

    def filterChessboard(self, frame):
        return cv.warpPerspective(frame, self.matrix, (self.FieldSize * 8, self.FieldSize * 8))



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
            break
    schachBild = SchachBild(100)
    print("test")
    schachBild.initialFrame(frame)
    print("init schachBild")

    #show chess board
    chessborad = schachBild.filterChessboard(frame)
    cv.imshow("preview", chessborad)
    print("showed schachBild")



    while (True):

        # Capture frame-by-frame

        ret, frame = cap.read()
        frame = schachBild.filterChessboard(frame)

        # Display the resulting frame
        if ret:
            cv.imshow("preview", frame)
            print("new Frame")
        # Waits for a user input to quit the application

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    # When everything done, release the capture

    cap.release()

    cv.destroyAllWindows()

main()
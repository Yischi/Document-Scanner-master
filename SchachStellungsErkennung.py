import cv2 as cv
import numpy as np

class Move:
    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos

    def __str__(self):
        if self.startPos[0] == -1 or self.startPos[1] == -1 or self.endPos[0] == -1 or self.endPos[1] == -1:
            return "ungültiger Zug"
        alphabet = "abcdefgh"
        numbers = "87654321"
        return alphabet[self.startPos[0]] + numbers[self.startPos[1]] + ":" + alphabet[self.endPos[0]] + numbers[self.endPos[1]]


class BackgroundSub:
    def __init__(self, frame):
        self.setupBackground(frame)

    def setupBackground(self, frame):
        self.Background = frame.copy()

    def apply(self, frame):
        frame2 = cv.subtract(self.Background, frame)
        frame3 = cv.subtract(frame, self.Background)
        self.Background = frame.copy()
        return frame2 + frame3
    def BsubF(self, frame):
        frame2 = cv.subtract(self.Background, frame)
        return frame2
    def FsubB(self, frame):
        frame2 = cv.subtract(frame, self.Background)
        return frame2

class SchachBild:
    def __init__(self, fieldSize):
        self.FieldSize = fieldSize
        self.Tolerance = int(fieldSize * 0.15)
        self.InnerField = fieldSize - 2 * self.Tolerance
        self.direktion = 0
        self.oldPeases = []
        for X in range(8):
            self.oldPeases.append([])
            for Y in range(8):
                self.oldPeases[X].append(False)
        self.moveNumber = 0
        print("init fin")


    def _setupBackground(self, frame):
        self.BackgroundSub = BackgroundSub(frame)

    def turnChessboard(self, frame):
        self.direktion = (self.direktion +1) % 4
        self.Corners = [self.Corners[3], self.Corners[0] ,self.Corners[1],self.Corners[2]]
        print("rotate " +str(self.direktion))
        pts1 = np.float32([self.Corners])
        pts2 = np.float32([[self.FieldSize, self.FieldSize * 7],
                           [self.FieldSize * 7, self.FieldSize * 7],
                           [self.FieldSize * 7, self.FieldSize],
                           [self.FieldSize, self.FieldSize]])
        self.matrix = cv.getPerspectiveTransform(pts1, pts2)
        frame = self.filterChessboard(frame)
        self._setupBackground(frame)

    def initialFrame(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (7, 7), None)
        if ret == True:
            # get Corner Position of the 1. Rank
            self.leftupper = corners[6][0]
            self.leftlower = corners[48][0]
            self.rightlower = corners[42][0]
            self.rightupper = corners[0][0]

            self.Corners = [self.leftupper.copy(), self.rightupper.copy(), self.rightlower.copy(), self.leftlower.copy()]

            # PREPARE POINTS FOR Transformation
            pts1 = np.float32([self.Corners])
            pts2 = np.float32([[self.FieldSize, self.FieldSize * 7],
                               [self.FieldSize * 7, self.FieldSize * 7],
                               [self.FieldSize * 7, self.FieldSize],
                               [self.FieldSize, self.FieldSize]])
            self.matrix = cv.getPerspectiveTransform(pts1, pts2)


            print("Calculated matrix")

            #init Background
            initFrame = self.filterChessboard(frame)
            self._setupBackground(initFrame)
        else:
            print("NO CHECK BOARD")
        return ret

    def _useBackGroundSubtraction(self, frame):
        return self.BackgroundSub.apply(frame)

    def filterChessboard(self, frame):
        return cv.warpPerspective(frame, self.matrix, (self.FieldSize * 8, self.FieldSize * 8))


    def _getCornerPersentage(self, img, X, Y, threshold = 10, neededPersentage = 2):
        foundedCorners = 0
        for x in range(self.InnerField):
            for y in range(self.InnerField):
                if img[Y*self.FieldSize + y + self.Tolerance, X*self.FieldSize +x+ self.Tolerance] > threshold:
                    foundedCorners += 1

        persentage = float(foundedCorners) / float(self.InnerField * (self.InnerField))
        print(persentage * 100)
        print(foundedCorners)
        print("of X: " +str(X) + " Y: " +str(Y))
        return persentage > (neededPersentage / 100.0)

    def findMovedPease(self, frame):
        frame = self.filterChessboard(frame)
        imgCanny = cv.Canny(frame, 100, 1)
        frame = self._useBackGroundSubtraction(frame)
        imgBS = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("BS-Image", imgBS)
        cv.imshow("imgCanny", imgCanny)

        FieldsChanged = []
        MovedTo = [-1,-1]
        for Y in range(8):
            for X in range(8):
                if self._getCornerPersentage(imgBS, X, Y, 20, 10):
                    FieldsChanged.append([X,Y])

        print(FieldsChanged)
        for pos in FieldsChanged:
            if self._getCornerPersentage(imgCanny, pos[0], pos[1], 0, 1):
                MovedTo = pos.copy()
        print(MovedTo)
        return FieldsChanged, frame, MovedTo

    def findallChessPeases(self, frame):
        frame = self.filterChessboard(frame)
        imgCanny = cv.Canny(frame, 100, 150)
        imgBS = cv.cvtColor(self._useBackGroundSubtraction(frame), cv.COLOR_BGR2GRAY)
        cv.imshow("imgCanny", imgCanny)

        Peases = []
        currentPeases = []
        move = Move([-1,-1], [-1,-1])
        self.moveNumber = self.moveNumber + 1

        for X in range(8):
            currentPeases.append([])
            for Y in range(8):
                if self._getCornerPersentage(imgCanny, X, Y,0, 1):
                    currentPeases[X].append(True)
                    Peases.append([X,Y])
                    if self.oldPeases[X][Y] != currentPeases[X][Y]:
                        move.endPos = [X,Y]
                        print("EndPos: " + str(move.endPos))
                else:
                    currentPeases[X].append(False)
                    if self.oldPeases[X][Y] != currentPeases[X][Y]:
                        move.startPos = [X,Y]
                        print("StartPos: " + str(move.startPos))

        print(Peases)

        #if endPos not founded -> pease has taken an other one
        if move.endPos[0] == -1 and move.endPos[1] == -1:
            cv.imshow("BS-Image", imgBS)
            print("test taken")
            for X in range(8):
                for Y in range(8):
                    if currentPeases[X][Y] == True:
                        if self._getCornerPersentage(imgBS, X, Y, 100, 10):

                            move.endPos = [X,Y]
                            print("taken")

        print(move)
        self.oldPeases = currentPeases.copy()
        return Peases, frame, move

    def draw(self,img,  X, Y, Color = (0, 255, 0)):
        print("draw X: " +str(X) + " Y: " +str(Y))
        img = cv.rectangle(img, (X * self.FieldSize, Y *self.FieldSize), ((X+1)*self.FieldSize, (Y+1)*self.FieldSize), Color, 3)
        return img
    def setBackgound(self, frame):
        frame = self.filterChessboard(frame)
        bsubf = self.BackgroundSub.apply2(frame)
        fsubb = self.BackgroundSub.apply1(frame)
        both = bsubf + fsubb
        #return(bsubf.equal(fsubb))
        cv.imshow("bsubf", bsubf)
        cv.imshow("fsubb", fsubb)
        cv.imshow("both", both)
        self.BackgroundSub.setupBackground(frame)






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
            #find move (Background sub -Bad way)
            if cv.waitKey(1) & 0xFF == ord("w"):
                # find peases in frame
                foundPeases, frame, MovedTo = schachBild.findMovedPease(frame)
                print(foundPeases)
                #mark founded peases
                for pos in foundPeases :
                    frame = schachBild.draw(frame, pos[0], pos[1])
                frame = schachBild.draw(frame, MovedTo[0], MovedTo[1], (0, 0, 255))

                # Display the resulting frame
                cv.imshow("preview", frame)
                print("w")
                while True:
                    if cv.waitKey(1) & 0xFF == ord("q"):
                        break
            #find and init all figures
            elif cv.waitKey(1) & 0xFF == ord("f"):
                # find peases in frame
                foundPeases, frame, move = schachBild.findallChessPeases(frame)
                print(foundPeases)
                #mark founded peases
                for pos in foundPeases :
                    frame = schachBild.draw(frame, pos[0], pos[1])

                # Display the resulting frame
                cv.imshow("preview", frame)
                print("f")
                while True:
                    if cv.waitKey(1) & 0xFF == ord("q"):
                        break

            #find Move (best way)
            elif cv.waitKey(1) & 0xFF == ord("m"):
                # find peases in frame
                foundPeases, frame, move = schachBild.findallChessPeases(frame)
                print(foundPeases)
                #mark move peases

                frame = schachBild.draw(frame, move.startPos[0], move.startPos[1], (0, 0, 255))
                frame = schachBild.draw(frame, move.endPos[0], move.endPos[1])


                # Display the resulting frame
                cv.imshow("preview", frame)
                print("m")
                while True:
                    if cv.waitKey(1) & 0xFF == ord("q"):
                        break
            #rotate
            elif cv.waitKey(1) & 0xFF == ord("r"):
                schachBild.turnChessboard(frame)
            #set Background
            elif cv.waitKey(1) & 0xFF == ord("b"):
                schachBild.setBackgound(frame)
            else:
                frame = schachBild.filterChessboard(frame)
                #frame = schachBild._useBackGroundSubtraction(frame)
        cv.imshow("preview", frame)
        #print("new Frame")
        # Waits for a user input to quit the application

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

    cv.destroyAllWindows()

main()
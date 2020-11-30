import cv2



def startCamera():
    # Open the device at the ID 0

    cap = cv2.VideoCapture(1)

    # Check whether user selected camera is opened successfully.

    if not (cap.isOpened()):

        print("ERROR")

    # To set the resolution

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)

    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)


    while (True):

        # Capture frame-by-frame

        ret, frame = cap.read()


        # Display the resulting frame
        if ret:
            cv2.imshow("preview", frame)
            print("new Frame")
        # Waits for a user input to quit the application

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break

    # When everything done, release the capture

    cap.release()

    cv2.destroyAllWindows()

startCamera()
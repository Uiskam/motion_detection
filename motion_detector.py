import cv2
link = 'https://imageserver.webcamera.pl/blog/webcamera_premium_filmmp_gotowemp4--1624624964.mp4'
link2 = './Demos/Demo1.mp4'
warszawa = 'https://imageserver.webcamera.pl/rec/warszawa-plac-zamkowy/latest.mp4'
agh = 'http://live.uci.agh.edu.pl/video/stream1.cgi?start=1543408695 '

gauss_kernel_value = 3
thresh_value = 40
dilated_itrs = 10
debug = False


def main():
    cap = cv2.VideoCapture(link)
    # cap = cv2.VideoCapture('Demos/Demo1.mp4')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

    out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    INPUT_WIDTH = len(frame1[0])
    INPUT_HEIGHT = len(frame1)

    START_WIDTH = 0
    START_HEIGHT = 0
    END_WIDTH = INPUT_WIDTH
    END_HEIGHT = INPUT_HEIGHT
    SMALLEST_AREA = 600

    SENSITIVE_OF_CONTOURS = [(START_WIDTH, START_HEIGHT, END_WIDTH, END_HEIGHT // 2, SMALLEST_AREA),
                             (START_WIDTH, END_HEIGHT // 2, END_WIDTH, END_HEIGHT, 250)]

    SENSITIVE_OF_CONTOURS = [(START_WIDTH, START_HEIGHT, END_WIDTH, END_HEIGHT, SMALLEST_AREA)]

    # print(frame1.shape)
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (gauss_kernel_value, gauss_kernel_value), 0)
        _, thresh = cv2.threshold(blur, thresh_value, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=dilated_itrs)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            for start_width, start_height, end_width, end_height, smallest_area in SENSITIVE_OF_CONTOURS:
                if start_width <= x and x + w <= end_width and start_height <= y and y + h <= end_height:
                    if cv2.contourArea(contour) < smallest_area:
                        continue
                    else:
                        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 255), 3)

        image = cv2.resize(frame1, (1280, 720))
        out.write(image)

        if debug:
            WIDHT = 400
            HEGIHT = 300
            resized_frame1 = cv2.resize(frame1, (WIDHT, HEGIHT))
            resized_frame2 = cv2.resize(frame2, (WIDHT, HEGIHT))
            resized_diff = cv2.resize(diff, (WIDHT, HEGIHT))
            resized_gray = cv2.resize(gray, (WIDHT, HEGIHT))
            resized_blur = cv2.resize(blur, (WIDHT, HEGIHT))
            resized_thresh = cv2.resize(thresh, (WIDHT, HEGIHT))
            resized_dilated = cv2.resize(dilated, (WIDHT, HEGIHT))
            result = cv2.resize(frame1, (WIDHT, HEGIHT))
            cv2.imshow("Frame1", resized_frame1)
            cv2.imshow("Frame2", resized_frame2)
            cv2.imshow("Difference between frame1 and frame2", resized_diff)
            cv2.imshow("Gray on diff image", resized_gray)
            cv2.imshow("Blurred gray image", resized_blur)
            cv2.imshow("Thresh image", resized_thresh)
            cv2.imshow("Dilated image with thresh", resized_dilated)
            cv2.imshow("result", result)
            cv2.waitKey(0)
        else:
            WIDHT = 1024
            HEGIHT = 728
            frame1 = cv2.resize(frame1, (WIDHT, HEGIHT))
            cv2.imshow("result", frame1)

        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(40) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    out.release()


if __name__ == "__main__":
    main()

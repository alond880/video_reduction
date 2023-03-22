import os
import sys
import time

import cv2
import cv2 as cv

#fflag : 0 - folder
#        1 - file

# sys.argv:
# [0] = script
# [1] = path
# [2] = file/folder flag
# [3] = tank id
# [4] = location
# [5] = battalion
# [6] = sensetivity
# [7] = max length

if len(sys.argv) > 6:
    treshhold = sys.argv[6]
else:
    treshhold = 900


#minimum time between movments
if len(sys.argv) > 7:
    min_diff = sys.argv[7]
else:
    min_diff = 3


#frame_rate = 30.0
frames = []
time_stamps = []


def get_arguments(fflag):
    global file_name
    file_name = ""

    global file_details
    file_details = ""

    global folder_name
    folder_name = "_"

    if( len(sys.argv) > 3):
        tank_id = sys.argv[3]
        location = sys.argv[4]
        battalion = sys.argv[5]

    else:
        tank_id = "test"
        location = "test"
        battalion = "test"

    file_details = "_" + str(tank_id) + "_" + str(location) + "_" + str(battalion) + "_"
    folder_name = "/FOLDER OF - " + file_details + "/"



# write out video bits
def extraction(file, fflag, video, out_cuts_old, count):

    (out_cuts_old).release()  # relese previous video segment

    if not fflag:  # folder
        video_path_change = "C:/Users/Rapat/Desktop/saved_video_test/" + folder_name + video.removesuffix(".mp4") + "_number" + str(count) + ".mp4"
    else:  # file
        video_path_change = "C:/Users/Rapat/Desktop/saved_video_test/" + folder_name + file_details + "_number" + str(count) + ".mp4"

    print(video_path_change)
    out_cuts_new = cv.VideoWriter(video_path_change, cv2.VideoWriter_fourcc(*'MP4V'), frame_rate, (video_width, video_hight))

    return out_cuts_new


def motionDetection(file, video, fflag):
    count = 0
    flag_cut = False
    t = 0
    # cap = cv.VideoCapture(sys.argv[1])
    # cap = cv.VideoCapture("C:/Users/Rapat/Desktop/videos/arad.mp4")
    try:
        cap = cv.VideoCapture(file)
    except NameError:
        print(NameError + ": " + file)

    start_time = time.time()

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    global video_width
    global video_hight
    global frame_rate

    video_width = frame1.shape[1]
    video_hight = frame1.shape[0]
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    print("fps: " + str(frame_rate))

    # create folder for all videos
    if not os.path.exists("C:/Users/Rapat/Desktop/saved_video_test/"):
        os.makedirs("C:/Users/Rapat/Desktop/saved_video_test/")

    # create folder for specific video
    if not os.path.exists("C:/Users/Rapat/Desktop/saved_video_test/" + folder_name):
        os.makedirs("C:/Users/Rapat/Desktop/saved_video_test/" + folder_name)

    if not fflag: #folder
        str_file_save = "C:/Users/Rapat/Desktop/saved_video_test/" + folder_name + video.removesuffix(".mp4") + "_all" + ".mp4"
        str_file_save_cut = "C:/Users/Rapat/Desktop/saved_video_test/" + folder_name + video.removesuffix(".mp4") + "_number0" + ".mp4"
    else: #file
        str_file_save = "C:/Users/Rapat/Desktop/saved_video_test/" + folder_name + file_details + "_all" + ".mp4"
        str_file_save_cut = "C:/Users/Rapat/Desktop/saved_video_test/" + folder_name + file_details + "_number0" + ".mp4"

    print(str_file_save)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out_all = cv.VideoWriter(str_file_save, fourcc, frame_rate, (video_width, video_hight))
    out_cut = cv.VideoWriter(str_file_save_cut, fourcc, frame_rate, (video_width, video_hight))


    while cap.isOpened():
        if ret == True:

            diff = cv.absdiff(frame1, frame2)
            diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
            _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
            dilated = cv.dilate(thresh, None, iterations=3)
            contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, w, h) = cv.boundingRect(contour)
                if cv.contourArea(contour) < treshhold:
                    if flag_cut:
                        if (time.time() - t >= min_diff):
                            out_cut = extraction(file, fflag, video, out_cut, count)
                            count += 1
                            #t = 0
                            flag_cut = False
                    else:
                        t = time.time()
                        flag_cut = True
                    continue
                t = time.time()
                flag_cut = False

                time_stamps.append((time.time() - start_time)) #save movment frame time
                frames.append(frame1) #save movment frame
                cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                out_cut.write(frame2)
                out_all.write(frame2)



            #cv.drawContours(frame1, contours, -1, (0, 255, 0), 2)

            cv.imshow("Video", frame1)
            frame1 = frame2
            ret, frame2 = cap.read()



            if cv.waitKey(50) == 'a':

                break
        else:
            break

    cap.release()
    out_all.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    get_arguments(int(sys.argv[2]))

    print(sys.argv)

    if( len(sys.argv) > 2):
        if int(sys.argv[2]) == 1: #file
            motionDetection(sys.argv[1], None, 1)

        elif int(sys.argv[2]) == 0: #folder
            dirs = os.listdir(sys.argv[1])
            for video in dirs:
                file = sys.argv[1] + "/" + video
                motionDetection(file, video, 0)


    #extraction()
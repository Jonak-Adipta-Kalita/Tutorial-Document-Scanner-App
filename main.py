import cv2, sys
import utlis

webcam = False
webcam_num = 0

webcam_input = str(input("Want to use Webcam? (yes or no): "))

if webcam_input == "yes" or webcam_input == "YES":
    webcam = True
    webcam_name = int(input("The number of your Webcam you want to use? "))
elif webcam_input == "no" or webcam_input == "NO":
    webcam = False
else:
    print("Please type yes or no")
    sys.exit()

path = '1.jpg'
cap = cv2.VideoCapture(webcam_num)
cap.set(10,160)
cap.set(3, 1280)
cap.set(4, 720)
scale = 3
wP = 210 *scale
hP = 297 *scale

while True:
    if webcam:success,img = cap.read()
    else: img = cv2.imread(path)

    imgContours , conts = utlis.getContours(img,minArea=50000,filter=4)
    if len(conts) != 0:
        biggest = conts[0][2]
        #print(biggest)
        imgWarp = utlis.warpImg(img, biggest, wP,hP)
        imgContours2, conts2 = utlis.getContours(imgWarp,
                                                 minArea=2000, filter=4,
                                                 cThr=[50,50],draw = False)
        if len(conts) != 0:
            for obj in conts2:
                cv2.polylines(imgContours2,[obj[2]],True,(0,255,0),2)
                nPoints = utlis.reorder(obj[2])
                nW = round((utlis.findDis(nPoints[0][0]//scale,nPoints[1][0]//scale)/10),1)
                nH = round((utlis.findDis(nPoints[0][0]//scale,nPoints[2][0]//scale)/10),1)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
        cv2.imshow('JAK Document Scanner App - A4', imgContours2)

    img = cv2.resize(img,(0,0),None,0.5,0.5)
    cv2.imshow('JAK Document Scanner App',img)
    cv2.waitKey(1)

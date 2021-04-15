import time
import cv2
import numpy as np
from gpiozero import Buzzer
bzr = Buzzer(17)

video = cv2.VideoCapture("atak2.mp4")
enaz = np.array([70,60,50])
encok = np.array([120,255,100])

ret,ilkres = video.read()
konum = cv2.rectangle(ilkres,(180,85),(100,120),color=[0,0,255],thickness=3)
y=80
x=50
h=25
w=70
crop = ilkres[y:y+h, x:x+w]
#cv2.imshow("cırp",ilkres)
hsv_crop=cv2.cvtColor(crop,cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([hsv_crop],[0],None,[180],[0,174])
roi_hist =cv2.normalize(roi_hist,roi_hist,50,255,cv2.NORM_MINMAX)
sicak = (cv2.TermCriteria_EPS|cv2.TERM_CRITERIA_COUNT, 10, 1)

perv = 0
new = 0

while (video.isOpened()):

    ret,kare = video.read()
    #resize = cv2.resize(680,420)


    new = time.time()
    fps = 1/(new-perv)
    perv = new
    fps = int(fps)
    cv2.putText(kare, "FPS:" + str(round(fps)), (5, 15), cv2.FONT_HERSHEY_COMPLEX, 1/2,color=(0,0,255) )


    rows, cols, _ = kare.shape

    #x çizgisi ile y çizgisinin set.(kesişimi alınır ) ve hedef merkezine eşitlenir.

    #print(target_center)
    #target_center=(x + int(w / 2), 0), (x + int(w / 2), rows) + (0, y + int(h / 2)), (cols, y + int(h / 2))

    #burada ana rectanle nin çevresi bulunur.
    #big_rectangle = (100, 350), (550, 70)


    # bu kısımda hedef merkezi ile big rectanglenin kesişiyor ise süre başlatılır ve kitlenme durumu evet yapılır.
    # kesişimler yapılır iken değişkeler int e çevir

    yil = time.localtime()[0]
    ay = time.localtime()[1]
    gun = time.localtime()[2]
    #cv2.putText(kare, "Time:", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 1/2, (0,0,255))

    #rectangle ana

    cv2.rectangle(kare, (100, 300), (550, 70), (255, 0, 0), thickness=2)


    #rectangle helicoptr
    hsv = cv2.cvtColor(kare,cv2.COLOR_BGR2HSV)
    maske2 = cv2.inRange(hsv,enaz,encok)
    maske = cv2.calcBackProject([hsv],[2],roi_hist,[0,180],2)
    _,kitleme =cv2.meanShift(maske2,(x, y, w, h), sicak)

    x,y,w,h = kitleme

    cv2.line(kare, (x + int(w/2), 0), (x + int(w/2), rows), color=(0,255,0), thickness=1)
    cv2.line(kare, (0, y+ int(h/2)), (cols, y + int(h/2)), color= (0, 255, 0), thickness= 1 )

    line_y = (y+ int(h/2))
    line_x = (x + int(w/2))
    merkez_line = (line_y, line_x)
    print(merkez_line)

    LockState = "0"


    if (100<line_x<550 and 70<line_y<300) == True:
        LockState = " Kitlendi"
        cv2.rectangle(kare, (x, y), (x + w, y + h), (0, 0, 250), 2)

        bzr.on()

    elif ( line_y == 347 and line_x == 218) == True:
        bzr.off()


    else:
        LockState = " Kitlenmedi"
        bzr.on()
        time.sleep(1/50)
        bzr.off()
        time.sleep(1/50)




    cv2.putText(kare, "Hedef Durumu:" + str(LockState), (105, 290), fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=1 / 2, color=(0, 0, 255), thickness=1)

    #line_x = (x + int(w/2)
    #print(str(line_x))



    cv2.imshow("HedefeKitlen",kare)
    cv2.imshow("maske2",maske2)
    #cv2.imshow("hsv",hsv)
    #cv2.imshow("maske",maske)
    if cv2.waitKey(25) == ord("q"):
        break

cv2.destroyAllWindows()
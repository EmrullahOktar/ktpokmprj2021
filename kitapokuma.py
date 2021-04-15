import cv2
import numpy as np
#import pytesseract
import os
from gtts import gTTS
import time
import gpiozero
import requests
import json
import io

from googletrans import Translator
trans = Translator()

#komponentlerin bağlantı noktası
buton_ing = gpiozero.Button(2)
#buton_kapat = gpiozero.Button(3)
buton_ss_al = gpiozero.Button(4)

led_ing = gpiozero.LED(27) # buton ing aktif olması durumunda devamlı yanacak
led_ss = gpiozero.LED(22)
buzzer = gpiozero.Buzzer(17)

#maskeleme için istenilen aralık
enaz = np.array([50, 30, 30])
encok = np.array([120, 255, 110])


vid = cv2.VideoCapture(0)
cv2.namedWindow("FotoAlmaislemi")
img_counter = 0 #Foto sayisi

while True:
    ret,frame = vid.read()
    #frame2 = cv2.resize(frame,(1920,1080))

    # görüntünün daha iyi anlaşılması için "Maskeleme"işlemi;
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maske2 = cv2.inRange(hsv, enaz, encok)

    #foto alma
    k = cv2.waitKey(1)
    if k%256 == 27:
        print("kapatılıyor")
        break
        #esc Derlemeyi Sonlandırır.
    elif (buton_ss_al.is_pressed) :
        buzzer.on()
        led_ss.on()
        img_name = "opencv_frame_"+ str(img_counter)+".png"
        cv2.imwrite(img_name, frame)
        print("{} yazıldı!".format(img_name))
        img_counter +=    1


        # resmi döndürme ve çevirme;
        img = cv2.imread(img_name)
        ters = cv2.flip(img, 0)
        ters2 = cv2.flip(ters, 1)


        #  pytesseract ile görseli yazizya çevirme işlemi
        #text = pytesseract.image_to_string(img)
        #print(text)
        #---------#--------#---------#request ile yazı çevirme

        url_api = "https://api.ocr.space/parse/image"
        _, compressedimage = cv2.imencode(".jpg", img, [1, 90])

        file_bytes = io.BytesIO(compressedimage)
        sonuc = requests.post(url_api,
                              files={"img": file_bytes},
                              data={"apikey": "helloworld", "language": "tur"})

        sonuc = sonuc.content.decode()
        sonuc = json.loads(sonuc)

        result = sonuc.get("ParsedResults")[0]
        belirlenen_yazi = result.get("ParsedText")
        #print(belirlenen_yazi)
        print(sonuc)

        cevirilmesi_gereken = belirlenen_yazi # ocrden gelen yazi bu kısma eşitlenir

        t = trans.translate(
            cevirilmesi_gereken, src="en", dest="tr"
        )
        print(t.text) # ingilizceden türkçeye cevrilmiş text


        #yaziyi ses formatina donusturme
        dil = "tr"
        ses_ciktisi = gTTS(text=t.text, lang=dil, slow=False)
        ses_ciktisi.save("ses.mp3")
        led_ss.off()
        buzzer.off()

        #ses ciktisini otomatik acma
        os.system("xdg-open ses.mp3")

    elif (buton_ing.is_pressed):
        img_name = "opencv_frame_" + str(img_counter) + ".png"
        cv2.imwrite(img_name, frame)
        print("{} yazıldı!".format(img_name))
        img_counter += 1

        # resmi döndürme ve çevirme;
        img = cv2.imread(img_name)
        # ters = cv2.flip(img, 0)
        # ters2 = cv2.flip(ters, 1)

        #  pytesseract ile görseli yazizya çevirme işlemi
        # text = pytesseract.image_to_string(img)
        # print(text)
        # ---------#--------#---------#request ile yazı çevirme

        url_api = "https://api.ocr.space/parse/image"
        _, compressedimage = cv2.imencode(".jpg", img, [1, 90])

        file_bytes = io.BytesIO(compressedimage)
        sonuc = requests.post(url_api,
                              files={"img": file_bytes},
                              data={"apikey": "helloworld", "language": "tur"})

        sonuc = sonuc.content.decode()
        sonuc = json.loads(sonuc)

        belirlenen_yazi = sonuc.get("ParsedResults")[0].get("ParsedText")
        print(belirlenen_yazi)

        text1 = belirlenen_yazi + "lütfen sonraki sayfaya çeviriniz"
        text2 = "boş yazi"  # ses dosyasinin açılmasındakı parazitlenme için ek.
        text3 = text2 + text1

        # ----------------------------
        # Bu kısımda ıng cewvirme ıslemı yapılır
        # -----------------------

        # yaziyi ses formatina donusturme
        dil = "tr"
        ses_ciktisi = gTTS(text=text3, lang=dil, slow=False)
        ses_ciktisi.save("ses.mp3")

        #ses ciktisini otomatik acma
        os.system("xdg-open ses.mp3")




    cv2.imshow("FotoAlmaislemi",frame)
    cv2.imshow("Maskeleme", maske2)



    cv2.waitKey(1)


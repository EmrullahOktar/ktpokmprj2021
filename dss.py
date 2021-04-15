import cv2
import os
from gtts import gTTS
import requests
import json
import io


resim = cv2.imread("kitaptansozler.jpeg")

#resim_resized= cv2.resize(resim, (1280,720))


# resmi yaziya cevirme
url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", resim, [1, 60])

file_bytes = io.BytesIO(compressedimage)
sonuc = requests.post(url_api,
              files = {"sabahattin2.jpeg": file_bytes},
              data = {"apikey": "helloworld","language": "tur"})


sonuc = sonuc.content.decode()
sonuc = json.loads(sonuc)

belirlenen_yazi = sonuc.get("ParsedResults")[0].get("ParsedText")
print(belirlenen_yazi)

text2 = 'boş yazi' + belirlenen_yazi + "lütfen sonraki sayfaya çeviriniz"

# yaziyi ses formatina donusturme
dil = "tr"
ses_ciktisi = gTTS(text= text2, lang= dil, slow = False)
ses_ciktisi.save("ciktix2.mp3")

#ses ciktisini otomatik acma
os.system("xdg-open ciktix2.mp3")


#işlediğimiz resim
cv2.imshow("resiim",resim)
cv2.waitKey(0)

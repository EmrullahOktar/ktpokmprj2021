from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
driver.get("https://www.google.com.tr/maps")
sleep(3)

#hedef konum bilgisi
konumyaz = driver.find_element_by_name("q")
konumyaz.send_keys("silopi mevlana döner")
sleep(2)

#hedef konuma 'yol Tarif butonuna'basma
# //*[@id="searchbox-directions"]
yol_tarif_buton = driver.find_element_by_xpath("//*[@id='searchbox-directions']")
yol_tarif_buton.click()
sleep(2)


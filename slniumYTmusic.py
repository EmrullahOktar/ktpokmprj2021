from selenium import webdriver
from time import sleep

# selenium ile youtubeden müzik açma

driver = webdriver.Chrome()
driver.get("https://www.youtube.com")
sleep(2)
username = driver.find_element_by_name("search_query")

sleep(1)
username.send_keys("ahmet kaya kum gibi")
sleep(2)
# //*[@id="search-icon-legacy"]/yt-icon
login = driver.find_element_by_xpath("//*[@id='search-icon-legacy']/yt-icon")
login.click()
sleep(3)
# //*[@id="contents"]/ytd-video-renderer[1]
videoac = driver.find_element_by_xpath("//*[@id='contents']/ytd-video-renderer[1]")
videoac.click()

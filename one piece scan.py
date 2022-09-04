from selenium.webdriver.chrome.options import Options as ChromeOptions
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import shutil
import requests


f = open('cache.json', 'r')
reader = f.read()
print(reader)

link = reader[1:]
link = link[:-1]
print(link)

chrome_options = ChromeOptions()
chrome_options.add_extension('adblock.crx')
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
driver.get(link)

time.sleep(3)

while True:

    try:
        driver.find_element(By.CLASS_NAME, "alert-info")
        print()
        print("Il n'y a plus de chapitre publiés")
        break
    except:
        image_urls = set()
        image = driver.find_element(By.CLASS_NAME, "scan-page")

        if image.get_attribute('src') and 'http' in image.get_attribute('src'):
            image_url = image.get_attribute('src')
            print(image_url)

            if len(image_url.split("/")[7].split("-")) > 1:
                chap = "chapitre{}".format(image_url.split("/")[7].split("-")[1])
            else:
                chap = "chapitre{}".format(image_url.split("/")[7])
            page = "page{}".format(image_url.split("/")[8].split(".")[0])

            image_name = "imgs/"+chap+page+".png"
            print(image_name)
            response = requests.get(image_url, stream=True)
            with open(image_name, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            del response

        next_page = driver.find_element(By.ID, "ppp")
        next_page.click()

        cache = driver.current_url

        file = open('cache.json', 'w')
        file.write(json.dumps(cache))
        file.close()


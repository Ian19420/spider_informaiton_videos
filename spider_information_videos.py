from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas

driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://www.youtube.com/results?search_query=letting+go")

for x in range(2):
    tags = driver.find_elements(By.XPATH, "//*[@id='video-title']")
    links = []
    for tag in tags:
        href = tag.get_attribute("href")
        if href:
            links.append(href)
    wait = WebDriverWait(driver, 10)
    html = driver.find_element(By.TAG_NAME, "html")
    html.send_keys(Keys.END) ##向下捲動

driver.implicitly_wait(10)
df = pandas.DataFrame(columns=["id", "title", "description"])
for link in links:
    driver.get(link)
    num = link.strip('https://www.youtube.com/watch?v=')
    title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#container >h1"))).text
    description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#description"))).text
    df.loc[len(df)] = [num, title, description]
df.to_csv("YouTube.csv", index=False, encoding="utf-8", mode = "w")
driver.quit()
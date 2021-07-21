import time
import os

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

USR = os.getenv("IG_USER")
PWD = os.getenv("IG_PWD")

def crawl_ig(account):
    url = f"https://www.instagram.com/{account}/"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    current_url = driver.current_url
    time.sleep(1)
    if "login" in current_url:

        username = driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(USR)
        time.sleep(0.5)
        pwd = driver.find_element_by_xpath('//input[@name="password"]')
        pwd.send_keys(PWD)
        time.sleep(0.5)
        btn = driver.find_element_by_xpath('//button[@type="submit"]')
        btn.click()
        time.sleep(3)
        driver.get(url)
        time.sleep(5)

    else:
        suggested_btn = driver.find_elements_by_class_name('coreSpritePagingChevron')[-1]
        while suggested_btn:
            try:
                suggested_btn.click()
                driver.find_elements_by_class_name('coreSpritePagingChevron')[-1]
            except:
                break

    story_btn = driver.find_elements_by_class_name('coreSpritePagingChevron')[0]
    while story_btn:
        try:
            story_btn.click()
            driver.find_elements_by_class_name('coreSpritePagingChevron')[0]
        except:
            break

    time.sleep(1)
    pageSource = driver.page_source
    driver.close()

    soup = bs(pageSource, "html.parser")
    title = soup.find("title").text.split(account)[0][:-2]
    posts = soup.select("main div header section ul li span")[0].text

    temp = soup.select("main div header section ul li a span")
    follower = temp[0].text
    following = temp[1].text

    description = bs(str(soup.select("main div header section div")[-1]), "lxml").text.replace(" ", "\n")
    blue_check = soup.find("span", title="已驗證")

    res = {"title": title,
        "posts": posts,
        "follower": follower,
        "following": following,
        "story_highlights": [],
        "suggesteds": []}

    temp = soup.select("main div div div div div ul")
    story_highlights = temp[0].findAll("li")
    for story in story_highlights:
        if story.find("img"):
            res["story_highlights"].append({"title": story.find("img")["alt"].split(" ")[0], 
                                   "img": story.find("img")["src"]})
    if len(temp) >= 3:
        suggesteds = temp[2].findAll("li")
        for suggest in suggesteds:
            if suggest.find("img"):
                res["suggesteds"].append({"title": suggest.find("img")["alt"].split(" ")[0],
                                    "img": suggest.find("img")["src"]})
    
    CLASS = soup.select("article div div div div")[0]["class"] 
    new_posts = soup.findAll("div", class_=CLASS)

    return res

print(crawl_ig("yga0721"))


from django.db.models.base import Model
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from news.models import HeadLine
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import time
import re
load_dotenv()
# from news.models import HeadLine
import os
# Create your views here.

# main_news = Model.objects.latest
# context = {
#         'main_news': main_news,
#     }



def scrape(requests):
    options = Options()
    # Add single argument (method 1)
    
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    
    # options.AddArguments("--headless", "--window-size=1920,1080", "--disable-gpu", "--disable-extensions", "--no-sandbox", "--incognito")

    # ------------------PATH do driver-----------------------
    PATH = os.environ['FACE_SELENIUM_DRIVER']

    driver = webdriver.Chrome(PATH, chrome_options=options)

    driver.get("https://maisesports.com.br/tag/pain-gaming/")
    time.sleep(5)
    content = driver.page_source
    
    # content = {}
    noticias = driver.find_elements_by_class_name("HistoryNewsstyled__LinkBox-mx9f66-0")
    # noticias = WebDriverWait(driver, 2).until(EC.elems((By.CSS_SELECTOR, "div[class='HistoryNewsstyled__NewsContainer-mx9f66-1']")))
    # for noticia in noticias:
    #     title = noticia.find_elements_by_css_selector("h4[class='HistoryNewsstyled__Title-mx9f66-3 WWwlw']")
    # print(noticias)
    src = re.findall(r'"featuredImage":{"sourceUrl":"([^"]*)"', content)
    
    count = 0
    for news,a in zip(noticias, src):
        link = news.get_attribute('href')
        # link = news.find_element_by_class_name("HistoryNewsstyled__LinkBox")
        next = news.find_elements_by_class_name("HistoryNewsstyled__NewsContainer-mx9f66-1")
        for i in next:
            title = news.find_element_by_class_name("HistoryNewsstyled__Title-mx9f66-3").text
            # img_src = news.find_element_by_class_name("HistoryNewsstyled__ImageBox-mx9f66-2")
            

        # content.update({link: [title, img_src]})
        # 
        # print(a)
        new_headline = HeadLine()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = a
           
        new_headline.save()
        count += 1
  
    return redirect("../")

def news_list(request):
    headlines = HeadLine.objects.all()[:5]
    context = {
        'object_list': headlines,
    }
    return render(request, "news/home.html", context)

def news_list_Five(request):
    headlines = HeadLine.objects.all()[:5]
    context = {
        'news_list': headlines,
    }
    return render(request, "news/home.html", context)

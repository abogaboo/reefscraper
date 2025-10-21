import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime

service = Service(executable_path=r"D:\chromedriver")
driver = webdriver.Chrome(service=service)


url = "https://www.statbotics.io/teams#breakdown"
driver.get(url)

def scrape(rank): #scrapes data for a single team based on rank
    print("Scraping the rank {rank} team. Their EPA is: ")
    currPath = "/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/table/tbody/tr[{rank}]/td[3]/div/div"
    link = driver.find_element_by_xpath(currPath)
    print(link.text)

# def scrapeAll():

scrape(1)
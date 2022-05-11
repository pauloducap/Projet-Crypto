from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


options = Options()
options.add_argument('--headless')

wallet = input("Entrez l'addresse de votre wallet XRP : ")
url = 'https://bithomp.com/explorer/' + wallet
print("Veuillez patienter pendant la récupération des données...")

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)
driver.get(url)


driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
amount_on_wallet = driver.find_element(By.XPATH, value="//span[@class='balance hint--left']").text
print("\nIl vous reste " + amount_on_wallet + "XRP sur votre wallet.")
driver.close()
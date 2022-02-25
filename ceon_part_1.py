import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from requests import get
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from time import sleep, strptime

service = Service('chromedriver_win32/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(service=service, options=options)
browser.get('http://scindeks.ceon.rs/journalDetails.aspx?issn=0042-8469')

issn_elem = browser.find_element(By.XPATH, "//td[contains(text(), 'ISSN')]/following-sibling::td")
print(issn_elem.text)

# link do stranice broj
'<a class="ctl00_cph1_JournalsDetailsControl_ic1_TreeViewIssues_0" href="issue.aspx?issue=15976" id="ctl00_cph1_JournalsDetailsControl_ic1_TreeViewIssuest1">vol. 70, br. 1</a>'

# pronalazimo elemente sa linkovima ka brojevim

brojevi_elems = browser.find_elements(By.CLASS_NAME, 'ctl00_cph1_JournalsDetailsControl_ic1_TreeViewIssues_0')

print(type(brojevi_elems), len(brojevi_elems))

# for elem in godine_elem:
#     print(elem.get_attribute('href'))

linkovi = [elem.get_attribute('href') for elem in brojevi_elems if elem.get_attribute('href').startswith('http://')]
for link in linkovi:
    print(link)

with open('out/ceon/linkovi_ka_clancima.txt', 'w', encoding='utf-8') as f:
    for link in linkovi:
        browser.get(link)
        clanci = browser.find_elements(By.XPATH, "//div[@class='naslov']/a")
        # for clanak in clanci:
        #     print(clanak.text, clanak.get_attribute('href')) // Vidimio da je u listu upalo i nesto sto nisu clanci pa filtriramo listu

        clanci_linkovi = [clanak.get_attribute('href') for clanak in clanci if clanak.get_attribute('href').startswith('http://scindeks.ceon.rs/article.aspx')]
        for clanak_link in clanci_linkovi:
            print('Sačuvano: ', clanak_link)
            f.write(clanak_link + '\n')

# Sada kada smo pogrebali linkove ka clancima preostaje nam da otvorimo svaki link i pogrebemo podatke sa stranica

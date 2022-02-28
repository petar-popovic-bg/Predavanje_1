# Predavanje_1 ceon_part_1.py
# Autor: Petar Popović
# Opis: Skript je namenjen pokaznoj vežbi na temu grebanja weba u sklopu VOA projekta.
#       Skript sakuplja linkove ka člancima izdanja "Vojnotehnički glasnik"
#       počevši od stranice časopisa, prolazeći kroz godine i brojeve
# Datum: 28.02.2022

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Kreiramo Selenium browser objekat
service = Service('chromedriver_win32/chromedriver.exe')
options = webdriver.ChromeOptions()
# Opcioni argument koji će sakriti grafički prikaz pretraživača
options.add_argument('headless')
browser = webdriver.Chrome(service=service, options=options)

# Otvaramo zadatu stranicu u Selenium browser objektu
browser.get('http://scindeks.ceon.rs/journalDetails.aspx?issn=0042-8469')

# link do stranice broj
'<a class="ctl00_cph1_JournalsDetailsControl_ic1_TreeViewIssues_0" href="issue.aspx?issue=15976" id="ctl00_cph1_JournalsDetailsControl_ic1_TreeViewIssuest1">vol. 70, br. 1</a>'

# pronalazimo elemente sa linkovima ka brojevim

brojevi_elems = browser.find_elements(By.CLASS_NAME, 'ctl00_cph1_JournalsDetailsControl_ic1_TreeViewIssues_0')

# Pravimo listu pravih linkova ka stranicama brojeva od sakupljenih elemenata
linkovi = [elem.get_attribute('href') for elem in brojevi_elems if elem.get_attribute('href').startswith('http://')]
for link in linkovi:
    print(link)

# Otvaramo fajl u koji ćemo upisati brojeve ka člancima koje ćemo pokupiti sa stranice svakog broja pojedinačno
with open('out/ceon/linkovi_ka_clancima.txt', 'w', encoding='utf-8') as f:
    for link in linkovi:
        # Kroz Selenium browser otvaramo svaku stranicu
        browser.get(link)
        # Uz pomoć xpath izraza pronalazimo elemente koji sadrže linkove ka člancima
        clanci = browser.find_elements(By.XPATH, "//div[@class='naslov']/a")
        # for clanak in clanci:
        #     print(clanak.text, clanak.get_attribute('href')) // Vidimio da je u listu upalo i nesto sto nisu clanci pa filtriramo listu

        # Iz liste elemenata članci vadimo href atribute onih elemenata gde vrednost href atributa počeinje sa zadatim stringom
        clanci_linkovi = [clanak.get_attribute('href') for clanak in clanci if clanak.get_attribute('href').startswith('http://scindeks.ceon.rs/article.aspx')]

        # Za svaki link u novoj listi: ispisujemo i upisujemo u orvoreni fajl "f"
        for clanak_link in clanci_linkovi:
            print('Sačuvano: ', clanak_link)
            f.write(clanak_link + '\n')

# Sada kada smo pogrebali linkove ka clancima preostaje nam da otvorimo svaki link i pogrebemo podatke sa stranica

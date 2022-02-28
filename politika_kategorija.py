# Predavanje_1 politika_kategorija.py
# Autor: Petar Popović
# Opis: Skript je namenjen pokaznoj vežbi na temu grebanja weba u sklopu VOA projekta.
#       Skript sakuplja članke sa web sajta politike koji pripadaju određenoj kategoriji.

# Datum: 28.02.2022

from requests import get
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import time

# Element koji tražimo na početnoj strani
"""
<a href="/scc/clanak/499740/Vece-profite-nisu-pratila-i-veca-ulaganja-u-nove-projekte" class="roboto-slab mb1 mt1 dark-gray bold">
                                            Веће профите нису пратила и већа улагања у нове пројекте</a>
"""

# Url sa kog sakupljamo linkove ka pojedinačnim člancima
url = 'https://www.politika.rs/scc/rubrika/6/Ekonomija'

# 1. Http zahtev
resp = get(url)
# 2. Kreiramo supu iz koje ćemo ekstraktovati podatke
soup = BeautifulSoup(resp.content, 'html.parser')
# 3. Pronalazimo linkove ka člancima
clanci = soup.find_all('a', {'class': 'roboto-slab mb1 mt1 dark-gray bold'})

prefix = 'https://www.politika.rs'
for idx, clanak in enumerate(clanci, start=1):
    print(idx, clanak['href'])
    # 4. Konstruišemo url ka članku
    url = prefix + clanak['href']
    # 5. Vršimo inicijalizaciju objekata u kojima ćemo držati sakupljene podatke sa stranice članka
    # Kreiramo "strukturu xml elemenata" za jedan članak
    # <clanak>
    #     <naslov/>
    #     <tekst/>
    #     <komentari/>
    # </clanak>
    clanak_elem = ElementTree.Element('div', {'type': 'article'})
    title_elem = ElementTree.SubElement(clanak_elem, 'title')
    text_elem = ElementTree.SubElement(clanak_elem, 'text')
    comments_elem = ElementTree.SubElement(clanak_elem, 'comments')

    # 6. Konstruisemo link ka članku i prihvatamo odgovor servera
    _resp = get('https://www.politika.rs' + clanak['href'])
    # 7. Ponovo pravimo supu od odgovora kako bi je pretražili
    _soup = BeautifulSoup(_resp.content, 'html.parser')

    try:
        # Tražimo i čuvamo podatak o datumu izdavanja
        datum = _soup.find('span', {'itemprop': 'datePublished'}).text
    except AttributeError:
        # U slučaju greške
        datum = '---'
    # Čuvamo podatak o datumu kao atrubut elementa 'clanak' koji smo u koraku pet inicijalizovali
    clanak_elem.attrib.update({'datum': datum})
    try:
        # Tražimo tekst naslova i čuvamo ga u elementu koji smo predvideli za njega
        title_elem.text = _soup.find('h1', {'itemprop': 'headline'}).text
    except AttributeError:
        title_elem.text = '---'
    try:
        # Tražimo tekst članka i čuvamo ga u elementu koji smo predvideli za njega
        paragraphs = _soup.find('div', {'class': 'article-content'}).find_all('p')
        for p in paragraphs:
            _p = ElementTree.SubElement(text_elem, 'p')
            _p.text = p.text
    except AttributeError:
        text_elem.text = '---'

    # 8. Konstruisemo putanju na kojoj ćemo sačuvati naš xml dokument
    xml_path = 'out/politika_kategorija/%s.xml' % clanak['href'].split('/')[3]
    print(xml_path)
    # 9. Upisujemo naš xml objekat u fajl
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(ElementTree.tostring(clanak_elem, encoding='unicode', method='xml'))
    # Odmaramo 10 sekundi
    time.sleep(10)

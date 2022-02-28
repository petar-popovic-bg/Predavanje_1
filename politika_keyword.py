# Predavanje_1 politika_keyword.py
# Autor: Petar Popović
# Opis: Skript je namenjen pokaznoj vežbi na temu grebanja weba u sklopu VOA projekta.
#       Skript sakuplja članke sa web sajta politike prema parametru ključna reč. Te koristi pretragu sajta

# Datum: 28.02.2022

from requests import get
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from time import sleep

# Početni url sa kog krećemo da sakupljamo nove linkove
base_url = 'https://www.politika.rs/search/index/keyword:ekonomija/sort:date/'

# Inicijalizujemo brojač stranica na 1
i = 1

# Ulazimo u petlju u kojoj ćemo povećavati brojač dok uslov za izlazak iz petlje ne bude ispunjen
# tj. broj vraćenih rezultata na stranici bude manji od 20
while True:
    # Konstruišemo url sa kojim ćemo dobiti rezultate pretrage (dodajemo page:1 kao deo url-a)
    url = base_url + '/page:%d/' % i
    # Saljemo zahtev serveru i čuvamo njegov odgovor u promenljivoj resp
    resp = get(url)
    # Pravimo supu od odgovora
    soup = BeautifulSoup(resp.content, 'html.parser')
    # Pretražujemo supu kako bi pronašli linkove ka člancima koje smo dobili kao odgovor od servera na naš upit
    # 1. Pronalazimo deo strane (element) u kome se nalaze linkovi kako bi suzili mogućnost greške
    container = soup.find('article', {'id': 'article-title', 'class': 'sm-col sm-col-12 md-col-12 lg-col-8 px2 mt0 sm-mt2 mb0'})
    # 2. Pronalazimo sve "a" elemente sa css atributom dark-gray
    # to su elementi koji sadrže linkove ka člancima()
    clanci = container.find_all('a', 'dark-gray')
    # 3. Kreiramo listu linkova ka člancima
    # Tako što ekstraktujemo potreban deo linka iz href atributa
    linkovi = [clanak['href'] for clanak in clanci]
    # 4. Vršimo iteraciju po listi linkova pokupljenih sa trenutne strane
    for link in linkovi:
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
        _resp = get('https://www.politika.rs' + link)
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
        xml_path = 'out/politika_keyword/%s.xml' % link.split('/')[3]
        print(xml_path)
        # 9. Upisujemo naš xml objekat u fajl
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(ElementTree.tostring(clanak_elem, encoding='unicode', method='xml'))
        # Odmaramo 10 sekundi
        sleep(10)

    # 10. U koliko je broj sakupljenih linkova sa stranice manji od 20 to znači da je to poslednja
    # stranica i izlazimo iz petlje
    if len(linkovi) < 20:
        break
    # Ako je broj linkova 20 ili veći pokušavamo da dobijemo sledeću stranu tako što povećavamo brojač za 1,
    # konstruišemo novi link /page:2/ i ponovo ulazimo u proces
    else:
        i = i + 1
        continue

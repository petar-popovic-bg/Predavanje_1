# Predavanje_1 b92_najnovije.py
# Autor: Petar Popović
# Opis: Skript je namenjen pokaznoj vežbi na temu grebanja weba u sklopu VOA projekta.
#       Skript sakuplja najnovije članke sa b92 po datumu

# Datum: 28.02.2022


import datetime
from requests import get
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from time import sleep, strptime

# Osnova url-a na koju ćemo nadograđvati parametre
base_url = 'https://www.b92.net/info/vesti/index.php?'

# postavaljenje parametara za godinu, mesec i dan
day = datetime.datetime.today().day
month = datetime.datetime.today().month
year = datetime.datetime.today().year
start = 0

print(day, month, year)

# Kreiranje dictionary objekta, koji će biti prosleđen get funkciji iz requests biblioteke
params = {'dd': day,
          'mm': month,
          'yyyy': year,
          'start': start
          }

# Ulazak u petlju "spoljnu" petlju
while True:
    print(base_url, params)
    # Responnse objekat kao rezultat Http
    resp = get(base_url, params)
    # Kreiramo BS objekat iz kog ćemo izvući linkove ka pojedinačnim člancima
    soup = BeautifulSoup(resp.content, 'html.parser')
    # Nalazimo elemente koje sadrže linkove
    clanci = soup.find('section', 'blog').find_all('article', 'item')
    # Postavljamo promenljivu "izlazak" na False, koju ćemo kasnije iskoristiti za izlazak iz "spoljne" petlje
    izlazak = False
    # Ulazimo u unutrašnju petlju
    for clanak in clanci:
        # kreiramo strukturu elemenata u koje ćemo upisivati pronađene informacije
        clanak_elem = ElementTree.Element('div', {'type': 'article'})
        title_elem = ElementTree.SubElement(clanak_elem, 'title')
        text_elem = ElementTree.SubElement(clanak_elem, 'text')
        comments_elem = ElementTree.SubElement(clanak_elem, 'comments')

        # Kreiramo link zasebnoj stranici članka uz pomoć osnove URL-a i pronađenih linkova
        link = 'https://www.b92.net' + clanak.find('div', 'text').h2.a.get('href')

        _resp = get(link)
        _soup = BeautifulSoup(_resp.content, 'html.parser')

        # Izdvajamo i proveravamo datum objavljivanja članka
        datum = _soup.find('time').get('datetime')
        print(datum, link)
        # Parsiramo tekstualni zapis datuma i datetime,
        _datum = strptime(datum, '%d-%m-%Y')

        # Kada naletimo na članak u listi koji nije od danas, znači da nema biše današnjih članaka i izlazimo iz petlje
        if (_datum.tm_mday != day) or (_datum.tm_mon != month) or (_datum.tm_year != year):
            # postavljamo proemnljivu izlazak na True kako bi izašli iz spoljne petlje
            izlazak = True
            print('Pojavio se %s' % datum)
            break
        # Ako je datum članka današnji nastavljamo dalje sa procedurom
        else:
            clanak_elem.attrib['datum'] = datum
            try:
                title_elem.text = _soup.find('div', 'article-header').h1.text
            except AttributeError:
                title_elem.text = '---'
            try:
                paragraphs = _soup.find('article', {'class': 'item-page', 'id': 'article-content'}).find_all('p')
                for paragraph in paragraphs:
                    p = ElementTree.SubElement(text_elem, 'p')
                    p.text = paragraph.text
            except AttributeError:
                text_elem.text = '---'

            file_path = 'out/b92_najnovije/' + link.split('nav_id=')[1] + '.xml'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(ElementTree.tostring(clanak_elem, encoding='unicode', method='xml'))
            # pauziramo izvršavanje koda na 10 sekundi kako ne bi opteretili server
            sleep(10)
    # Ako je promenljiva izlazak podešena na True izlazimo iz petlje
    if izlazak:
        break
    else:
        # Ako ne treba da izađemo iz spoljnje petlje uvećavamo start parametar zahteva kako bi učitali
        # sledećih devet članala u narednom krugu
        params['start'] = params['start'] + 9


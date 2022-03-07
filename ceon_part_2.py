# Predavanje_1 ceon_part_2.py
# Autor: Petar Popović
# Opis: Skript je namenjen pokaznoj vežbi na temu grebanja weba u sklopu VOA projekta.
#       Skript otvara linkove prikupljene u prethodnoj vežbi, prikuplja metapodatke sa stranice i preuzima pdf datoteke.
#       Prikupljene metapodatke čuva u json formatu na disku.
# Datum: 28.02.2022

from requests import get
from bs4 import BeautifulSoup
import json

# Otvaramo fajl koji smo kreirali u prethodnoj vežbi i učitavamo linkove koje smo zabeležili u njega u listu
with open('out/ceon/linkovi_ka_clancima.txt', 'r') as f:
    cl_linkovi = [link.replace('\n', '') for link in f.readlines()]

print(cl_linkovi)
print(len(cl_linkovi))

# Kreiramo Python dictionary objekat sa ključem 'clanci' čija je vrednost prazna lista
clanci = {
    'clanci': []
}

# Vršimo iteraciju kroz llistu linkova koje smo učitali iz fajla
for link in cl_linkovi[0:10]:
    # Uz pomoć request biblioteke otvaramo link
    resp = get(link)
    # Sadržaja odgovora parsiramo u Beautiful Soup objekat 'soup'
    soup = BeautifulSoup(resp.content, 'html.parser')

    # Naslov
    try:
        naslov = soup.find('div', 'cl_nas').text
    except Exception as e:
        naslov = '---'
    # Autor
    try:
        autor = soup.find('div', 'cl_aut').a.text
    except Exception as e:
        autor = '---'
    # Kljucne reci
    try:
        kljucne_reci = soup.find('span', string='Ključne reči').parent.text
    except Exception as e:
        kljucne_reci = '---'
    # Sazetak
    try:
        sazetak = soup.find('div', 'cl_saz cl_saz_ab').text
    except Exception as e:
        sazetak = '---'

    # Kreiramo Python dictionary objekat 'clanak_meta' u kome ćemo držati pogrebane metapodatke, link ka pdf fajlu, i
    # lokaciju na kojoj smo sačuvali .pdf  fajl.

    clanak_meta = {'naslov': naslov,
                   'autor': autor,
                   'kljucne_reci': kljucne_reci,
                   'sazetak': sazetak,
                   'pdf': {
                       'link': '---',
                       'lokacija': '---'
                   }
                   }

    try:
        pdf_link = soup.find('div', 'cl_badges').a['href']
    except Exception as e:
        print(e)
        pdf_link = None

    if pdf_link is not None:
        clanak_meta['pdf']['link'] = pdf_link
        r_pdf = get(pdf_link)
        lokacija_pdf_fajla = 'out/ceon/pdf/' + pdf_link.split('/')[-1]
        # out/ceon/pdf/0042-84692201001Z.pdf
        with open(lokacija_pdf_fajla, "wb") as f:
            f.write(r_pdf.content)
        clanak_meta['pdf']['lokacija'] = lokacija_pdf_fajla

    # Dodajemo popunjen Dictionary objekat "clanak_meta" u listu unutar Dictionary objekta "clanci"
    clanci['clanci'].append(clanak_meta)

# Otvaramo fajl u koji upisujemo serijalizovani "clanci" objekat
with open('out/ceon/ceon_metadata.json', 'w', encoding='utf-8') as jf:
    jf.write(json.dumps(clanci, ensure_ascii=False, indent=4))

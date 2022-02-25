from requests import get
from bs4 import BeautifulSoup
import json


with open('out/ceon/linkovi_ka_clancima.txt', 'r') as f:
    cl_linkovi = [link.replace('\n', '') for link in f.readlines()]

print(cl_linkovi)
print(len(cl_linkovi))

clanci = {
    'clanci': []
}
for link in cl_linkovi[0:10]:
    resp = get(link)
    soup = BeautifulSoup(resp.content, 'html.parser')
    clanak_meta = {'naslov': soup.find('div', 'cl_nas').text,
                   'autor': soup.find('div', 'cl_aut').a.text,
                   'sazetak': soup.find('div', 'cl_saz cl_saz_ab').text,
                   'pdf': {
                       'link': '',
                       'lokacija': ''
                   }
                   }

    pdf_link = soup.find('div', 'cl_badges').a['href']
    clanak_meta['pdf']['link'] = pdf_link
    r_pdf = get(pdf_link)
    lokacija_pdf_fajla = 'out/ceon/pdf/' + pdf_link.split('/')[-1]
    with open(lokacija_pdf_fajla, "wb") as f:
        f.write(r_pdf.content)
    clanak_meta['pdf']['lokacija'] = lokacija_pdf_fajla
    clanci['clanci'].append(clanak_meta)

with open('out/ceon/ceon_metadata.json', 'w', encoding='utf-8') as jf:
    jf.write(json.dumps(clanci, ensure_ascii=False, indent=4))

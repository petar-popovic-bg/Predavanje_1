# Predavanje_1
## Opis projekta

Ovaj projekat je deo NlpWeb radionice i biće korišćen u svrhu predavanja iz oblasti grebanja weba na primeru web sajta Politike.

Grebanje weba ili ekstrakcija podataka sa weba podrazumeva prikupljanje podataka sa web sajtova. Programi za prikupljanje podataka uglavnom direktno pristupaju sadržaju na internetu putem HTTPa ili web pregledača. Grebanje weba može biti izvedeno i ručno od strane korisnika softvera, termin se obično koristi za automatizovan proces koji je deo nekog većeg sistema ili bota. Proces podrazumeva prikupljanje određenog sadžaja i njegovo pohranjivanje (obično u bazu podataka) za kasnije korišćenje ili analizu.

Prikupljanje podataka podrazumeva proces ekvivalentan onome što radi web pregledač (Chrome, Mozilla, Internet Explorer itd.) kada korisnik otvorni neku stranicu. Nakon prikupljanja sledi proces ekstrakcije podataka u kome pribavljamo podatke koji su nam potrebni iz prethodno parsiranog ili pretraženog dokumenta.

Skripte u ovom primeru korišćenjem `requests` biblioteke upućuje zahtev serveru a potom iz dobijenog odgovora uz pomoć `BeautifulSoup` i `Selenium` paketa ekstraktuje potrebne podatke koje potom čuva u .xml formatu uz pomoć `ElementTree` modula na odgovarajućem mestu na disku.
- [requests](https://pypi.org/project/requests/)

  `requests` je mala biblioteka koja nam omogućava slanje HTTP zahteva pomoću pajtona.
  
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
  
  `BeautifulSoup` je biblioteka za Python koja nam olakšava navigaciju kroz HTML

- [Selenium](https://pypi.org/project/selenium/)

  `Selenium` je paket za automatizaciju interakcije sa web browserom.
  
- [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)

  `ElementTree` je modul za parsiranje i kreiranje podataka u XML formatu.
  
Prvi skript namenjen je grebanju određene sekcije(kategorije) sajta: svet, politika, društvo, ekonomija...

Drugi skript namenjen je grebanju članaka koji se dobijaju korišćenjem pretrage sajta.

Treći skript namenjen je skidanju .pdf fajlova i prikupljanju metapodataka

### Podešavanje okruženja
- Potrebno: Python 3, pip, internet konekcija
- Poželjno: PyCharm

1. Skinuti projekat sa github stanice
Projekat se može preuzeti sa ove github stranice u formatu .zip datoteke ili ga skinuti direktno u IDE npr. PyCharm
Link za download .zip verzije projekta [Predavanje_1](https://github.com/petar-popovic-bg/Predavanje_1/archive/refs/heads/master.zip)

### Instalacija
2. Instalirati potrebne biblioteke
Biblioteke korišćene u projektu su requests i Beautiful Soup 4. Kako bi instalirali sve neophodne biblioteke korišćene u projektu potrebno je izvršiti komandu:
`pip install -r requirements.txt`
ili
Kako se obe biblioteke nalaze na PyPi mogu se i zasebno instalirati komandama
`pip install beautifulsoup4` i `pip install requests`

### Korišćenje
U samim skriptama potrebno je promeniti potrebne parametre i pokrenuti skriptu.

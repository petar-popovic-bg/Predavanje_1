# Predavanje_1
### Opis projekta

Ovaj projekat je deo NlpWeb radionice i biće korišćen u svrhu predavanja iz oblasti grebanja weba na primeru web sajta Politike.
Skript korišćenjem requests biblioteke upućuje zahtev serveru a potom iz dobijenog odgovora uz pomoć BeautifulSoup biblioteke ekstraktuje potrebne podatke koje pritom čuva u .xml formatu u odgovarajućem folderu.
Prvi skript namenjen je grebanju određene sekcije(kategorije) sajta: svet, politika, društvo, ekonomija...

Drugi skript namenjen je grebanju članaka koji se dobijaju korišćenjem pretrage sajta.

### Podešavanje okruženja
Potrebno: Python 3, pip, internet konekcija.
Poželjno: PyCharm.

1. Skinuti projekat sa github stanice
Projekat se može preuzeti sa ove github stranice u formatu .zip datoteke ili ga skinuti direktno u IDE npr. PyCharm
Link za download .zip verzije projekta ...

### Instalacija
2. Instalirati potrebne biblioteke
Biblioteke korišćene u projektu su requests i Beautiful Soup 4. Kako bi instalirali sve neophodne biblioteke korišćene u projektu potrebno je izvršiti komandu:
pip install -r requirements.txt
ili
Kako se obe biblioteke nalaze na PyPi mogu se i zasebno instalirati komandama pip install beautifulsoup4 i pip install requests
### Korišćenje
U samim skriptama potrebno je promeniti potrebne parametre i pokrenuti skriptu.

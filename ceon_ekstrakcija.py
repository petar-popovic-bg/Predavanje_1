import os
from tika import parser


files = ['out/ceon/pdf/' + file for file in os.listdir('out/ceon/pdf')]

for file in files:
    print('Processing ', file)

    # Kreiramo pdf objekat
    parsed_pdf = parser.from_file(file)

    # Ekstraktovani tekst
    data = parsed_pdf['content']

    # Kreiramo putanju na kojoj ćemo otvoriti fajl
    outpath = 'out/ceon/txt/' + os.path.basename(file).replace('.pdf', '.txt')
    # otvaramo fajl u kojem čuvamo ektraktovani tekst
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(data)

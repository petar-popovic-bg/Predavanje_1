import os
import re

files = ['out/ceon/txt/' + file for file in os.listdir('out/ceon/txt')]

for file in files:
    print('Processing file: ', file)
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    # Kompajliramo regularni izraz za više novih redova
    vise_nr = re.compile(r'[\n\r]{2,}')
    # Srednja crta novi red
    crtica_nr = re.compile(r'-\n\r')
    # Link
    link_nr = re.compile(r'https?://.+[\r\n \.]')

    # re.sub vrši zamenu
    text = re.sub(vise_nr, '\n', text)
    text = re.sub(crtica_nr, '', text)
    text = re.sub(link_nr, '', text)

    # Izbacujemo svaku liniju kraću od četiri karaktera
    lines = text.split('\n')
    new_lines = []
    for idx, line in enumerate(lines):
        if len(line) > 4:
            new_lines.append(line)

    text = '\n'.join(new_lines)

    # Upisujemo modifikovani tekst
    with open(file, 'w', encoding='utf-8') as g:
        g.write(text)

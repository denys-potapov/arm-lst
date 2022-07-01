"""ARM instrucion set."""
import glob
import re

from bs4 import BeautifulSoup as bs

PATH = 'ISA_A64_xml_A_profile-2022-03/ISA_A64_xml_A_profile-2022-03/'

INDEXES = {
    'fpsimd': 'fpsimdindex.xml',
    'base': 'index.xml',
    'sme': 'mortlachindex.xml',
    'sve': 'sveindex.xml'
}

def get_text(el):
    return re.sub('\s+', ' ', el.get_text()).strip()


def diag_pp(diag):
    str = '|'
    for box in diag.find_all('box'):
        value = get_text(box)
        if not value:
            value = box.get('name', '')

        width = int(box.get('width', 1)) * 2 - 1
        value = value.ljust(width)[:width]
        str += value + '|'

    return str


def asm_pp(asm):
    str = get_text(asm).replace('<', '').replace('>', '')
    return str


def parse(file):
    b = bs(open(file).read(), "lxml")
    for c in b.find_all('iclass'):
        diag = diag_pp(c.find('regdiagram'))
        asm = ' / '.join(asm_pp(asm) for asm in c.find_all('asmtemplate'))

        yield diag + '  % ' + asm + '\n'

for name, filename in INDEXES.items():
    f = open(name + '.lst', 'w')

    idx = bs(open(PATH + filename).read(), "lxml")
    for form in idx.find_all('iform'):
        formfile = form.get('iformfile')
        f.writelines(parse(PATH + formfile))

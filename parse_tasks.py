from bs4 import BeautifulSoup
from collections import namedtuple
from log import log

def execute_tasks(html):
    return parse_faraa(html)

def parse_faraa(html):
    soup = BeautifulSoup(html, 'html.parser')
    output = []
    tables = soup.findAll('table')
    tables = [t for t in tables if t is not None if t.get('id') if 'report_' in t.get('id')]
    row = namedtuple('faraa', 'date name reg_number url doc_type')
    for t in tables:
        rows = t.findAll('tr')
        for r in rows:
            name = r.find('td',{'headers': 'REGISTRANTNAME'} )
            number = r.find('td', {'headers': 'REGISTRATIONNUMBER'})
            pdf_url_el = r.find('td', {'headers': 'DOCUMENT'})
            doc_type = r.find('td', {'headers': 'DOCUMENTTYPE'})
            date = r.find('td', {'headers': 'STAMPED/RECEIVEDDATE'})

            if name:
                output.append(row(
                    name= name.text,
                    reg_number= number.text,
                    url= pdf_url_el.a.get('href'),
                    doc_type= doc_type.text,
                    date= date.text,
                    ))
    return output
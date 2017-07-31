from config import config
from log import log

def parse_for_slack(data):
    return parse_faraa(data)

def parse_faraa(data):
    header = 'scrape_date received_date name reg_number doc_type url'
    lines = [header]

    for d in data['parsed']:
        scrape_date = '%s'%data['date']
        received_date = '%s'%d.date
        name = '*%s*'%d.name
        reg_number = '%s'%d.reg_number
        url = '<%s | PDF>'%d.url
        doc_type = '%s'%d.doc_type
        line = ', '.join([scrape_date, received_date, name, reg_number, doc_type, url])
        lines.append(line)

    return '\n'.join(lines)

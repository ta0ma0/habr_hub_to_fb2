import requests
from  bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import sys
import re
import logging
import json
from os.path import exists


logging.basicConfig(level=logging.DEBUG, filename='get_hubr_data.log',
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


link = sys.argv[1]
base_link = link + 'page'

def get_page(link):
    url = link
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    page = s.get(url)
    logger.info('Got page data')
    return page.text

def get_count_of_pages(main_page):
    """Return number of last page from paginator"""
    hub_links_list = []
    soup = BeautifulSoup(main_page, 'html.parser')
    hub_links = soup.find('div', {'class':'tm-pagination__pages'})
    numer_pages = hub_links.findAll('a')
    last_page = numer_pages[-1].text
    last_page = [line for line in last_page.split('\n') if line.strip() != ''][0].strip()
    logger.info(f'Got last page {last_page}')
    return last_page

def build_pages_links(count_of_pages, base_link):
    """Build list links to all pages with articles"""
    pages_links = []
    for el in range(int(count_of_pages)):
        el = el + 1
        page_link = base_link + str(el)
        pages_links.append(page_link)
    return pages_links

def save_page(page, sequence):
    file_name = 'page_data/' + str(sequence) + '_page_data.json'
    if exists(file_name):
        exist_question = 'y'
        exist_question = input('File is exist, continue download y/n: ')
        if exist_question == 'y':
            with open(file_name, 'w') as f:
                f.write(json.dumps(page))
                logger.info(f'{sequence}_page_data.json page saved')
        elif exist_question == 'n':
            return False
    else:
        with open(file_name, 'w') as f:
                f.write(json.dumps(page))
                logger.info(f'{sequence}_page_data.json page saved')


def read_page(sequence, file_postfix):
    with open(f'{sequence}{file_postfix}') as f:
        page_data = json.loads(f.read())
    return page_data

def get_article_links(page_link):
    pass

def save_article(link):
    pass

main_page = get_page(link)
count_of_pages = get_count_of_pages(main_page)
page_links = build_pages_links(count_of_pages, base_link)

for el in range(int(count_of_pages)):
    sequence = el + 1
    page = get_page(page_links[el])
    save_process = save_page(page, sequence)
    if save_process == False:
        break




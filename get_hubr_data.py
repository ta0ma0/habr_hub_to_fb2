import requests
from  bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import sys
import re

link = sys.argv[1]

def get_page(link):
    url = link
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    page = s.get(url)
    return page.text

def get_count_of_pages(main_page):
    """Return number of last page from paginator"""
    hub_links_list = []
    soup = BeautifulSoup(main_page, 'html.parser')
    hub_links = soup.find('div', {'class':'tm-pagination__pages'})
    numer_pages = hub_links.findAll('a')
    last_page = numer_pages[-1].text
    last_page = [line for line in last_page.split('\n') if line.strip() != ''][0].strip()
    return last_page



main_page = get_page(link)
count_of_pages = get_count_of_pages(main_page)




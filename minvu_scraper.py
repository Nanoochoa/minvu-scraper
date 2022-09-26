import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import pandas as pd
from tqdm.auto import tqdm

def init_request_session():
    # Configure request session
    req_session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )
    req_session.mount('http://', HTTPAdapter(max_retries=retries))
    return req_session

def scrape_monthyear(url:str, timeout) -> pd.DataFrame:
    
    # Get paginator hrefs from soup of single page
    def get_paginator_hrefs(soup:BeautifulSoup) -> list:
        center_blocks = soup.find_all(lambda tag: tag.name == 'center')
        try:
            hrefs = [a['href'] for a in center_blocks[0].find_all(href=True)]
        except IndexError:
            return []
        return hrefs

    # Extract table from soup of single page
    def extract_table(soup:BeautifulSoup) -> pd.DataFrame:
        table = soup.find_all("table", {"class": "tabla"})
        try:
            table = pd.read_html(table[0].prettify())[0]
        except IndexError:
            return None 
        return table

    # Define initial parameters
    base_url, init_href = url.rsplit('/', 1)
    month = url.rsplit('_', 1)[1][0:2]
    year = url.rsplit('/', 1)[0].rsplit('/', 1)[1]

    # Request page
    req_session = init_request_session()
    page = req_session.get(url, timeout=timeout)
    soup = BeautifulSoup(page.text, 'lxml')

    # Check if there is a table to continue
    if extract_table(soup) is None:
        return None

    # Get all tables (go through pages)
    df = [extract_table(soup)]
    hrefs = get_paginator_hrefs(soup)
    for href in tqdm(hrefs, desc=f'additional pages in {month}/{year}'):
        url = base_url + '/' + href
        page = req_session.get(url, timeout=timeout)
        soup = BeautifulSoup(page.text, 'lxml')
        table = extract_table(soup)
        df.append(table)

    return pd.concat(df)


def scrape_year(year:int, timeout=3) -> pd.DataFrame:
    base_url = f'http://transparencia.minvu.cl/IRIS_FILES/Transparencia/{year}/beneficio_DS01_13reg_'
    df = []
    empty_months = []
    for month in range(1, 13):
        # Set up mont-year URL
        yymm =  f'{month:02}' + str(abs(year) % 100)
        url = base_url + yymm + '.html'

        # request page
        req_session = init_request_session()
        page = req_session.get(url, timeout=timeout)

        # try to scrape month tables only if return code is not error
        if page.status_code != 404:
            month_tables = scrape_monthyear(url, timeout=timeout)

        # skip month and report if 404 or no tables in page
        if page.status_code == 404 or month_tables is None:
            empty_months.append(month)
            print(f'\rempty months: {empty_months}', end='', flush=True)
            continue
        
        # else, append non-empty list of scraped table
        df.append(month_tables)
    
    # Concatenate dataframes and exit
    if len(df) > 0:
        return pd.concat(df)
    else:
        exit('\nno data collected')

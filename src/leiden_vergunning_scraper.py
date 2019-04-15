import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def _get_api_url():
    return 'https://vergunningen.leiden.nl/ldn.dll?appname=Ldn&prgname=Ldn&ARGUMENTS=-A03send,-A,-A,-A{},-A,-A'


def get_leiden_vergunning_data(url, date):
    page = requests.get(url.format(date))
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find_all('table', class_='opgemaakt')
    colnames = [x.get_text() for x in info[1].find_all('tr')[0].find_all('th')]
    vals = info[1].find_all('tr')[1:]
    data = [entry.get_text().split('\n')[1:-1] for entry in vals]
    return pd.DataFrame(data=data, columns=colnames)


def get_dates_leiden_vergunningen(url):
    date = '11-04-2019'
    page = requests.get(url.format(date))
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find_all('table', class_='opgemaakt')
    dates = [date.get_text().replace(' ', '') for date in info[0].find_all('option') if len(date.get_text()) > 1]
    return dates


def get_postcode(loc_info):
    code = re.search("[0-9][0-9][0-9][0-9][a-zA-Z][a-zA-Z]$", loc_info)
    if code is not None:
        code = loc_info[code.span()[0]:code.span()[1]]
        return code
    else:
        return ''


def get_adress(loc_info):
    code = re.search("[0-9][0-9][0-9][0-9][a-zA-Z][a-zA-Z]$", loc_info)
    if code is not None:
        code = loc_info[:code.span()[0]]
        return code
    else:
        return loc_info


def parse_vergunningen_df(raw_df):
    df = raw_df.copy()
    df['postcode6'] = df.LocatiePostcode.apply(get_postcode)
    df['postcode4'] = df.postcode6.apply(lambda x: x[0:4])
    df['adres'] = df.LocatiePostcode.apply(get_adress)
    df = df.drop('LocatiePostcode',axis=1)
    return df

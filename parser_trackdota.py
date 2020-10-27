import requests
from bs4 import BeautifulSoup

URL = 'https://www.datdota.com/matches?tier=all/'
PAGE_WITH_STATS = 'https://www.datdota.com'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.287',
    'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_with_stats(html):
    link_list = []
    cnt_first_links = 0
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        link_tmp = link.get('href')
        if link_tmp[1:8] == 'matches':
            cnt_first_links += 1
            if cnt_first_links > 4:
                link_list.append(link_tmp)

    return link_list


def get_patch(links):
    soup = BeautifulSoup(links, 'html.parser')
    for title in soup.find_all('img'):
        command_name = title.get('alt')
        if command_name is not None:
            print(command_name)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        pages_with_stats = get_pages_with_stats(html.text)
        index_err = 0
        for page in pages_with_stats:
            html_page_with_stats = get_html(PAGE_WITH_STATS + page)
            index_err += 1
            if html_page_with_stats.status_code == 200:
                get_stat(html_page_with_stats.text)
            else:
                print('Error status code in datdota list', index_err)
    else:
        print('Error status code in datdota main')


parse()

import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.datdota.com/matches?tier=all/'
PAGE_WITH_STATS = 'https://www.datdota.com'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
                  'Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.287',
    'accept': '*/*'}
INTERRUPT_HEADER_PARAMS = 0


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


def get_info(links):
    soup = BeautifulSoup(links, 'html.parser')
    # League, id, Patch:
    info_game_list = soup.find_all('h2')
    char_list = []
    info_game_str = info_game_list[0]

    for ind_char in range(len(info_game_str.text)):
        if info_game_str.text[ind_char] == '/':
            char_list.append(ind_char)

    League_list = info_game_str.text[:char_list[0] - 1]
    prev_ind_char = char_list[0]
    id_match_list = info_game_str.text[prev_ind_char + 2:char_list[1] - 1]
    prev_ind_char = char_list[1]
    Patch_list = info_game_str.text[prev_ind_char + 2:]

    # Date and duration:
    date_and_duration = soup.find_all('h3')
    print(date_and_duration)
    #date = date_and_duration[-1].text[:-13]
    #duration = date_and_duration[-1].text[-5:]
    #print(duration)

    return [League_list, id_match_list, Patch_list]


def get_stat(links):
    soup = BeautifulSoup(links, 'html.parser')
    # Get names commands:
    list_commands = soup.find_all(height='72', width='128')
    names_commands = []
    for name in list_commands:
        names_commands.append(name['title'])

    # Get status place (Win or lose):
    places_list = soup.find_all('span', style="font-size: 1.3em;")
    places = []
    for place in places_list:
        places.append(place.text[1:])

    head_stat_list = soup.find_all('th')
    head_stat = []
    for header in head_stat_list:
        head_stat.append(header.text)

    stat_list = soup.find_all('td')
    stat = []
    for statistic in stat_list:
        stat.append(statistic.text)

    return [names_commands, places, head_stat, stat]


def form_and_get_csv(info_about_game, statistic_game, path):
    header_info_about_game = ['Link', 'League', 'Match id', 'Patch version', 'Date', 'Duration',
                              'Name 1st command', 'Status first command', 'Stack heroes', 'Average level',
                              'Kills', 'Deaths', 'Assists', ]


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        pages_with_stats = get_pages_with_stats(html.text)
        index_err = 0
        for page in pages_with_stats:
            html_page_with_stats = get_html(PAGE_WITH_STATS + page)
            index_err += 1
            if html_page_with_stats.status_code == 200:
                get_info(html_page_with_stats.text)
                #get_stat(html_page_with_stats.text)
            else:
                print('Error status code in datdota list', index_err)
    else:
        print('Error status code in datdota main')


parse()

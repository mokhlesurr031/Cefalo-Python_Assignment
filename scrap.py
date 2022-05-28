from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from datetime import datetime



# Scrapping Duration
#requests = Execution time: 0:07:41.948418


def fetch_initial_data():
    movie_list_url = 'https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films'
    response = requests.get(movie_list_url)
    soup = BeautifulSoup(response.text, "lxml")
    selector = 'tbody tr'
    all_link_el = soup.select(selector)

    start_time = datetime.now()

    for link_el in all_link_el:
        get_movie_list_data(link_el)

    end_time = datetime.now()
    print("Data Parsing Done. Execution time: {}".format(end_time - start_time))


def get_movie_list_data(link_el):
    try:
        link = link_el.td.next.next['href']
        link = urljoin('https://en.wikipedia.org', link)
        data = link_el.text.split('\n')
        movie_lists_dict = {
            'name': data[1],
            'path': link,
            'year': data[2],
            'awards': data[3],
            'nominations': data[4]
        }
        fetch_movie_detail(link)
        print(movie_lists_dict)
    except:
        pass

    try:
        link = link_el.td.next.next.next['href']
        link = urljoin('https://en.wikipedia.org', link)
        data = link_el.text.split('\n')

        movie_lists_dict = {
            'name': data[1],
            'path': link,
            'year': data[2],
            'awards': data[3],
            'nominations': data[4],
        }
        fetch_movie_detail(link)

        print(movie_lists_dict)

    except:
        pass


def fetch_movie_detail(link):
    response = requests.get(link)

    soup = BeautifulSoup(response.text, 'lxml')
    selector = '.infobox  tbody tr'
    movie_detail_data_all = soup.select(selector)
    details = {}
    for movie_data in movie_detail_data_all:
        title = movie_data.contents[0].text
        try:
            val = movie_data.contents[1].text.split('\n')
        except:
            val = ''
        val = [i for i in val if i]
        details[title] = val
    # return details
    print(details)


fetch_initial_data()
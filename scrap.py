from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def fetch_initial_data():
    movie_list_url = 'https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films'
    response = requests.get(movie_list_url)
    soup = BeautifulSoup(response.text, "lxml")
    selector = 'tbody tr'
    all_link_el = soup.select(selector)

    for link_el in all_link_el:
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
            print(movie_lists_dict)

        except:
            pass

fetch_initial_data()
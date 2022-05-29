from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime
from os import cpu_count
from tinydb import TinyDB, Query
from flask import Flask
import json
app = Flask(__name__)


# Scrapping Duration
#requests = Execution time: 0:07:41.948418
#thread = Execution time: 0:02:30.763098

# Data Scrapping and write to db
#scrap and write to db = Execution time: 0:11:39.054897 (requests)
#scrap and write to db = Execution time: 0:03:06.477507 (thread)


# TinyDB Configuration
movie_list = TinyDB('movie_list.json')
movie_details = TinyDB('movie_details.json')
movieList = Query()
movieDetails = Query()


movies = []


def fetch_initial_data():
    print("Please wait for a few moments......\n\n")
    movie_list_url = 'https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films'
    response = requests.get(movie_list_url)
    soup = BeautifulSoup(response.text, "lxml")
    selector = 'tbody tr'
    all_link_el = soup.select(selector)

    start_time = datetime.now()

    with ThreadPoolExecutor(max_workers = cpu_count()*5) as p:
        p.map(get_movie_list_data, all_link_el)

    movies_data = movies

    flag = 1
    for movie in movies_data:
        movie['id']=flag
        try:
            movie_list.insert(movie)
            print("List row added")
        except:
            print("List insert failed for {}".format(movie))
        try:
            movie_details.insert(fetch_movie_detail(movie))
            print("Detail row added")
        except:
            print("Details insert failed for {}".format(movie))
        flag+=1

    # print("Movie Data from first page parsing completed\n\nPlease wait till movie details data scrapping is done.....\n\n")

    # with ThreadPoolExecutor(max_workers = cpu_count()*2) as p:
    #     p.map(fetch_movie_detail, movies_data)

    end_time = datetime.now()
    print("Data Parsing Done. Execution time: {}".format(end_time-start_time))


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
        movies.append(movie_lists_dict)
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
        movies.append(movie_lists_dict)
    except:
        pass


def fetch_movie_detail(link):
    movie_id = link['id']
    movie_name = link['name']
    link = link['path']
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")
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
    movie_details_dict = {
        'name': movie_name,
        'movie_id': movie_id,
        'details': details
    }
    return movie_details_dict


def serve_data():
    @app.route('/')
    def movie_list_view():
        all_movie_list = movie_list.all()
        res = {"Movies List": all_movie_list}
        result = json.dumps(res)
        loaded_res = json.loads(result)
        return loaded_res

    @app.route('/<movie_id>')
    def movie_detail_view(movie_id):
        movie_detail = movie_details.search(movieDetails.movie_id == int(movie_id))
        res = {"Details": json.dumps(movie_detail)}
        result = json.dumps(res)
        loaded_res = json.loads(result)
        return loaded_res


    if __name__=='__main__':
        app.run()


try:
    arguments = sys.argv[1]
except:
    arguments = 'serve'

if arguments =='parse':
    fetch_initial_data()
elif arguments=='serve':
    serve_data()
else:
    print("please enter right command")
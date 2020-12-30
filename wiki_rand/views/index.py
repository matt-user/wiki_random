"""
Wiki Rand (main) view
URLS include:
/
"""

import flask
import requests

import wiki_rand

# API endpoint
URL = "https://en.wikipedia.org/w/api.php"
SESSION = requests.Session()

@wiki_rand.app.route('/', methods=['GET', 'POST'])
def show_index():
    '''Display / route.'''
    if flask.request.method == 'POST':
        # TODO this breaks if the user isn't friendly w input
        try:
            num_pages = int(flask.request.form['num_pages'])
        except ValueError:
            num_pages = 1
        titles = get_random_page_title(num_pages)
        pages_info = { title: get_page_info(title) for title in titles }
        image_info = { title: fetch_image_data(title) for title in titles }
        context = { "pages_info": pages_info, "image_info": image_info }
    else:
        context = { "pages_info": {}, "image_info": {} }
    return flask.render_template("index.html", **context)


def fetch_image_data(title):
    '''Fetch the image data for the given titles.'''
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "images",
        "titles": title
    }
    data = SESSION.get(url=URL, params=params).json()
    # not all pages have an image so we have to except key error
    try:
        filename = data["query"]["pages"][0]["images"][0]["title"]
        image_src = fetch_image_src(filename)
    except KeyError:
        filename = ""
        image_src = f"{title} does not have any images"
    image_page_url = "https://en.wikipedia.org/wiki/" + title
    image_data = {
        "filename": filename,
        "image_page_url": image_page_url,
        "image_src": image_src
    }
    return image_data


def fetch_image_src(filename):
    '''Fetch image source for the given filename.'''
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": filename
    }
    data = SESSION.get(url=URL, params=params).json()
    page = next(iter(data["query"]["pages"].values()))
    image_info = page["imageinfo"][0]
    image_url = image_info["url"]
    return image_url


def get_random_page_title(num_pages=1):
    '''Fetch a random page title.'''
    # Parameters for fetching a random page
    # only grabs articles
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": 0,
        "rnlimit": num_pages
    }
    data = SESSION.get(url=URL, params=PARAMS).json()
    random_pages = data["query"]["random"]
    titles = [ random_pages[i]['title'] for i in range(len(random_pages)) ]
    return titles


def get_page_info(title):
    '''Fetch the info for the page with title, title.'''
    # parameters for getting the content of the page
    PAGE_PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "rvslots": "*",
        "rvprop": "content",
        "formatversion": 2
    }
    data = SESSION.get(url=URL, params=PAGE_PARAMS).json()
    # return page info
    return data["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
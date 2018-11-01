from urllib.request import urlopen
import threading
import os
import ssl
from searching_href import SearchingHref
import queue
import return_domain


# create directory and txt files when it is the first time running the program
def create_dir_and_files(first_url, directory):
    global base_url
    base_url = first_url
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print("the address already exists")
    crawled_url = os.path.join(directory, 'crawled_url.txt')
    if not os.path.exists(crawled_url):
        print("create the crawled_url.txt")
        f = open(crawled_url, 'w+')
        f.close()
    global path
    path = crawled_url
    # put the first url into queue
    set_to_queue(url_queue, open_url(first_url))


# open a website and return all urls inside the website
def open_url(page_url):
    crawled_set.add(page_url)
    write_data_to_crawled_file(page_url)
    try:
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(page_url)
        if 'text/html' in response.getheader('Content-type'):
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8", "ignore")
            finder = SearchingHref(base_url, page_url)
            finder.feed(html_string)
    except Exception as e:
        print("from main.open_url "+str(e))
        return set()
    return finder.url_found()


# threads get work from queue and crawl websites
def thread_work():
    while not url_queue.empty():
        work = url_queue.get()
        print(threading.current_thread().name + " is working on " + work)
        url_set = open_url(work)
        set_to_queue(url_queue, url_set)
        url_queue.task_done()


# convert set to queue
def set_to_queue(update_queue, url_set):
    for url in url_set:
        if return_domain.get_domain_name(base_url) != return_domain.get_domain_name(url):
            continue
        if url in crawled_set:
            continue
        update_queue.put(url)


# write crawled urls into crawled_url.txt
def write_data_to_crawled_file(data):
    with open(path, 'a') as f:
        f.write(data+"\n")


crawled_set = set()
path = ""
base_url = ''
url_queue = queue.Queue()
create_dir_and_files('https://www.google.ca', 'web_crawling')
for i in range(8):
    thread = threading.Thread(target=thread_work)
    thread.daemon = True
    thread.start()

url_queue.join()




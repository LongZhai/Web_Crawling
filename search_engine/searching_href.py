from html.parser import HTMLParser
from urllib import parse


class SearchingHref(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.url_set = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attributes_name, value) in attrs:
                if attributes_name == 'href':

                    url = parse.urljoin(self.base_url, value)
                    self.url_set.add(url)

    def url_found(self):
        return self.url_set

    def error(self, message):
        print("there is error in searching_href.py")

from bs4 import BeautifulSoup
import requests
import time
import send_email


# open the website and returns news in the web page
def get_news(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    news_links = soup.select("li.searchHit")
    news_set = set()
    for l in news_links:
        news_set.add((l.find("h3").text.strip(), l.find("a")['href']))
    print(news_set)
    return news_set


news_history = set()
while True:
    news = get_news("https://www.cp24.com/search-results/search-cp24-7.127?q=shooting")
    update = news - news_history
    if len(update) > 1:
        format_string = ""
        for element in update:
            title, link = element
            format_string = format_string + title + "\n" + link + "\n\n"
        send_email.send_email(format_string)
    else:
        print("no updates")
    news_history = news
    # check updates every half hour
    time.sleep(1800)

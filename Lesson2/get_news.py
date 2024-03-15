import json
from pprint import pprint

from newsapi import NewsApiClient
import requests


def get_news(keyword):
    apiKey = "9b48fe6447fe4d0383f50e30af3198b9"
    newsapi = NewsApiClient(apiKey)
    news = newsapi.get_everything(q=keyword, language='ru', page_size=15)
    news_articles = news['articles']
    print(news_articles[0])
    with open("./news.js", "w", encoding='utf8') as outfile:
        json.dump(news_articles, outfile, ensure_ascii=False)
    for i, value in enumerate(news_articles):
        print(f"{i}:{value}")
    return "done"


def get_news2():
    url = "https://newsnow.p.rapidapi.com/newsv2"

    payload = {
        "query": "AI",
        "time_bounded": True,
        "from_date": "01/02/2021",
        "to_date": "05/06/2021",
        "location": "us",
        "language": "en",
        "page": 1
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "bb34451c5amsh747657229b5637fp13048fjsnd8b660e7b293",
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    pprint(response.json())


def get_news3():
    import requests

    url = "https://google-news13.p.rapidapi.com/latest"

    querystring = {"lr": "en-US"}

    headers = {
        "X-RapidAPI-Key": "bb34451c5amsh747657229b5637fp13048fjsnd8b660e7b293",
        "X-RapidAPI-Host": "google-news13.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    pprint(response.json())


if __name__ == "__main__":
    get_news("dogs")
    # get_news3()

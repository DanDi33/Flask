import json
from newsapi import NewsApiClient


def get_news(keyword):
    apiKey = "9b48fe6447fe4d0383f50e30af3198b9"
    newsapi = NewsApiClient(apiKey)
    news = newsapi.get_everything(q=keyword, language='ru', page_size=15)
    news_articles = news['articles']
    print(news_articles[0])
    with open("./news.js", "w", encoding='utf8') as outfile:
        json.dump(news_articles, outfile, ensure_ascii=False)
    for i,value in enumerate(news_articles):
        print(f"{i}:{value}")
    return "done"


if __name__ == "__main__":
    get_news("dogs")

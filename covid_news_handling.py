import sched
import time
import json
import logging
import requests
from newsapi import NewsApiClient
from flask import Markup

newscheduler = sched.scheduler(time.time, time.sleep)

logging.basicConfig(filename='logfile.log', level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode="w+",
                    datefmt='%m/%d/%Y %I:%M:%S %p')

news_terms = json.loads(open("config.json").read())["news_terms"]
confidential_api_key = json.loads(open("config.json").read())["api_key"]


def news_API_request(covid_terms:str=news_terms) -> list:
    """news_API_request returns a stream of relevant articles from the news API and
       returns them as a list. A unique, personally acquired api key is required in order
       for data from the API to be returned. Acquire this at the link provided
       in the README file and paste it in the config.json file residing in the same directory
       as the .py files for the application. If api key is incorrect and the NewsApiClient()
       function can't be run correctly then a list will be returned containing a single dictionary
       for a single article of which details that a user needs to obtain a legitimate API key.
       This will be seen on the front-end template if the user visits the correct URL.

       Args:
           covid_terms(:obj:`str`, optional):
           A string of terms that are used as keywords to filter the articles obtained from the news
           API by. Any articles with these terms in their titles will be returned from the API.


       Returns: 3 possible returns depending on conditional statement
           list:
           all_articles: a list of dictionaries containing all relevant news articles (after being
           refined using covid_terms parameter passed to function) and their associated metadata.
           This returned if news try block of code can occur successfully in news_API_request\
           function body and status code returned from api website after request is 200.

           None: returned if status code is not 200

           list:
           [warning_article]: returned if try block of code fails in body of news_API_request;\
           particularly, NewsApiCLient() fails to be called. It is a list with a single dictionary\
           inside it, that tells a user to obtain a valid api key needed to make NewsApiClient to\
           be called effectively.

    """
    try:
        keywords=covid_terms.split(" ")
        newsapi = NewsApiClient(api_key=confidential_api_key)
        all_articles=[]
        results = requests.get("https://newsapi.org")
        if results.status_code == 200:
            for i in keywords:
                some_articles = newsapi.get_everything(q=i, language='en')["articles"]
                all_articles += some_articles
            return all_articles#[0:8]
        else:
            return None
    except:
        logging.warning("INVALID API KEY: Please alter the value of the key in config.json")
        description=("You need to change the API Key present in config.json. Get an api key:\
<a href={}>here</a>".format("https://newsapi.org/register"))
        description=Markup(description)
        warning_article = {'title': "INVALID API KEY", 'description':description}
        return [warning_article]

news_api_request = news_API_request()

def update_news(update_name:str) -> None:
    """update_news updates the covid news articles stored by calling news_API_request
       and appends a dictionary for each respective article returned from the news_API_request
       function call to an array which thus serves as an array storing
       each news article.

       Args:
           update_name(str):
           The name of the news update operation that update_news performs. This
           is not assigned to any variable or used as a parameter for any function so is trivial
           in this case.

       Returns:
           None
    """
    """THIS FUNCTION IS NOT ACTUALLY USED IN MAIN.PY; INSTEAD FUNCTIONALITY IS EMPLOYED ELSEWHERE\
IN MAIN.PY"""
    newsarticles = []
    newsdata = news_API_request()
    for j in newsdata:
        news_dictionary = {'title':j['title'], 'content':j['description']}
        newsarticles.append(news_dictionary)


#print(news_API_request())

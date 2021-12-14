from main import covid_updates
from main import schedule_covid_updates
from main import remove_articles
from main import add_news_articles
from main import schedule_add_news_articles
from covid_news_handling import news_API_request
import random
import time
import sched

removed_articles=[]
    
def test_covid_updates():
    original_updates=None
    original_local_covid_data = None
    original_national_covid_data = None
    original_local_area_7day_infections = None
    original_national_area_7day_infections = None
    original_hospital_cases_for_nation = -1
    #the hospital cases uses -1 as a defualt value because sometimes COVID API returns None as value for particular day's hospital cases
    original_deaths_total_for_nation = None
    updates, local_covid_data, national_covid_data, local_area_7day_infections, national_area_7day_infections, hospital_cases_for_nation, deaths_total_for_nation = covid_updates()
    assert updates != original_updates
    assert local_covid_data != original_local_covid_data
    assert national_covid_data != original_national_covid_data
    assert local_area_7day_infections != original_local_area_7day_infections
    assert national_area_7day_infections != original_national_area_7day_infections
    assert hospital_cases_for_nation != original_hospital_cases_for_nation
    assert deaths_total_for_nation != original_deaths_total_for_nation

    

def test_schedule_covid_updates():
    covidscheduler = sched.scheduler(time.time,time.sleep)
    covidscheduler.run(blocking = False)
    queue = schedule_covid_updates(random.randint(1,1000), "Example Title")
    print(covidscheduler.queue)
    assert len(queue) == 1
    assert queue[0].argument[0]=="Example Title"
    assert queue[0].argument[1]==False
        
def test_remove_articles():
    test_data = [{'title':"Title 1"}, {'title':"Title 2"}, {'title':"Title 3"}, {'title':"Title 4"}]
    global removed_articles
    removed_articles = ["Title 1", "Title 2"]
    test_data = remove_articles(test_data, removed_articles)
    for i in test_data:
        assert i['title'] not in removed_articles

def test_add_news_articles():
    news_articles=[]
    news_articles = add_news_articles()
    assert len(news_articles)!=0
    for i in news_articles:
        assert i['title']!= None
        assert i['content'] != None
    

def test_schedule_add_news_articles():
    newscheduler = sched.scheduler(time.time,time.sleep)
    newscheduler.run(blocking = False)
    queue = schedule_add_news_articles(random.randint(1,1000), "Example Title")
    assert len(queue) == 1
    assert queue[0].argument[0]=="Example Title"
    assert queue[0].argument[1]==False


if __name__ == "__main__":
    try:
        test_covid_updates()
    except AssertionError:
        print("covid_updates(): FAILED")
    try:
        test_schedule_covid_updates()
    except AssertionError:
        print("schedule_covid_updates(): FAILED")

    try:
        test_remove_articles()
    except AssertionError:
        print("remove_articles(): FAILED")

    try:
        test_add_news_articles()
    except AssertionError:
        print("add_news_articles: FAILED")
    try:
        test_schedule_add_news_articles()
    except AssertionError:
        print("schedule_add_news_articles: FAILED")
        

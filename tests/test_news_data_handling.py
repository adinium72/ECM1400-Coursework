from covid_news_handling import news_API_request
from covid_news_handling import update_news

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news():
    update_news('test')

if __name__ == "__main__":
    try:
        test_news_API_request()
    except AssertionError:
        print("news_API_request: FAILED")
    try:
        test_update_news()
    except:
        print("update_news: FAILED")

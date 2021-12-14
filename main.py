import datetime
import sched
import time
import json
import logging
from typing import Tuple
from flask import Flask
from flask import request
from flask import render_template
from covid_data_handler import covid_API_request
from covid_news_handling import news_API_request
from Lab_4_time_conversions import *


logging.basicConfig(filename='logfile.log', level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode="w+",
                    datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)

logging.info('Flask app has been initialised')

newscheduler = sched.scheduler(time.time, time.sleep)
logging.info('News scheduler object has been initialised')
covidscheduler = sched.scheduler(time.time,time.sleep)
logging.info('Covid scheduler object has been initialised')


#COVID API DATA HANDLING

nation = json.loads(open("config.json").read())["nation"]

try:
    local_covid_data = covid_API_request()["data"]
    logging.info('covid_API_request call for local area data has occurred')
except:
    logging.warning('WARNING: covid_API_request: FAILED - Public Health\
England Covid-19 API is not working correctly - unable to obtain\
national data from the API')
local_area_7day_infections = 0
for i in range(0,7):
    local_area_7day_infections += local_covid_data[i]['newCasesByPublishDate']
try:
    national_covid_data = covid_API_request(nation, "nation")["data"]
    logging.info('covid_API_request call for national data has occurred')
except:
    logging.warning('WARNING: covid_API_request: FAILED - Public Health\
England Covid-19 API is not working correctly\
- unable to obtain national data from the API')
national_area_7day_infections = 0
for i in range(0,7):
    national_area_7day_infections += national_covid_data[i]['newCasesByPublishDate']
hospital_cases_for_nation = national_covid_data[0]["hospitalCases"]
deaths_total_for_nation = national_covid_data[1]['cumDeaths28DaysByDeathDate']

logging.info('The initial data from the Covid API has been retrieved and stored')

updates = [
            ]
logging.info('List called updates, for holding the title, time and repeat \
status of a scheduled update has been initialised')

historical_covid_updates = []
historical_news_updates=[]

covideventdict={}
covidcounter = 0
newscounter = 0

cancelledupdatesarray=[]




def covid_updates(update_title:str=None, repeat:bool=None) -> Tuple[list, dict,
                                                                    dict, int, int, int, int]:
    """covid_updates is called when a scheduled update of COVID API data is to occur. The function
    makes 2 COVID API calls for national and local data respectively (using the
    covid_API_request() function) and updates the global variables (defined in the
    global namespace) for each of the relevant COVID-19 metrics that the data
    dashboard displays. If the scheduled update the function is called in response to
    is not a repeated update, then the update dictionary in the global list, updates,
    that is corresponding to the displayed update widget for the scheduled covid update
    is deleted from the front-end due to the update having been completed. This is done
    through removing said dictionary from the updates list.


    Args:
        update_title(:obj:`str`, optional):
        The title of the scheduled update that was scheduled by the user using the front-
        end widgets. This variable is passed as a parameter to covid_updates in order to be used to
        remove the corresponding update widget in the front-end after the update of COVID API data
        has taken place.

        repeat(:obj:`bool`, optional):
        The repeat status of the particular scheduled update that covid_updates was called in
        response to. This boolean is used to determine whether the update widget in the front-end
        corresponding to the scheduled update is removed after the update of COVID API data has
        taken place.

    Returns:
        Multi-varibale return

        Note: these returns are only used in the accompanying testing functions to this application

        list:
        updates - global list variable which holds dictionaries for each scheduled news/covid update
        (in this case it is returned after a an update dictionary may have been deleted from it.

        dict:
        local_covid_data - a global variable holding a dictionary returned from a call of
        covid_API_request with its default parameter values

        dict:
        national_covid_data - a global variable holding a dictionary returned from a call of
        covid_API_request with the parameter values of "England" and "nation" for location and
        location_type respectively.

        int:
        local_area_7day_infections - global integer variable for the local 7 day infection rate

        int:
        national_area_7day_infections - global integer variable for the national 7 day infection
        rate

        int:
        hospital_cases_for_nation - global integer variable for number of hospital cases

        int:
        deaths_total_for_nation - global integer variable for cumulative deaths within 28 days of a
        positive test by death date

    """
    update_title=update_title
    global updates
    global local_covid_data
    global national_covid_data
    global local_area_7day_infections
    global national_area_7day_infections
    global hospital_cases_for_nation
    global deaths_total_for_nation
    try:
        local_covid_data = covid_API_request()["data"]
        logging.info('covid_API_request call for local area data has occurred')
    except:
        logging.warning('WARNING: covid_API_request: FAILED - Public Health England Covid-19 API is\
 not working correctly unable to obtain local data from the API')
    local_area_7day_infections = 0
    for i in range(0,7):
        local_area_7day_infections += local_covid_data[i]['newCasesByPublishDate']
    try:
        national_covid_data = covid_API_request("England", "nation")["data"]
        logging.info('covid_API_request call for national data has occurred')
    except:
        logging.warning('WARNING: covid_API_request: FAILED - Public Health England Covid-19 API is\
 not working correctly - unable to obtain national data from the API')
    national_area_7day_infections = 0
    for i in range(0,7):
        national_area_7day_infections += national_covid_data[i]['newCasesByPublishDate']
    hospital_cases_for_nation = national_covid_data[0]["hospitalCases"]
    deaths_total_for_nation = national_covid_data[1]['cumDeaths28DaysByDeathDate']
    if repeat == False:
        if update_title != None:
            for i in range(len(updates)):
                if updates[i]['title'] == update_title:
                    logging.info('Covid update widget has been deleted as\
 scheduled update has occurred at desired time and update was not repeating')
                    del updates[i]
                    break
    #print("Covid Done")
    #print(deaths_total_for_nation)

    logging.info("Newest data from the Covid API has been retrieved and stored")
    return (updates, local_covid_data, national_covid_data, local_area_7day_infections,
            national_area_7day_infections, hospital_cases_for_nation, deaths_total_for_nation)

def schedule_covid_updates(update_interval:int, update_title:str, repeat:bool=False) -> list:
    """ schedule_covid_updates is called when a user wishes to schedule an update of COVID-19 data\
        from the COVID API on the dashboard at a given time. The function adds each scheduled event\
        to a dictionary that serves as a historical logging of every covid data update event ever\
        scheduled.

    Args:
        update_interval(int):
        The integer delay interval in seconds that is passed to the covidscheduler scheduler object\
        using the enter() method, to specify the duration the scheduler should wait before calling\
        the function associated with the scheduled event; in this case, covid_updates. This\
        interval is user-specified and is the time they enter for when they want an update
        of the COVID API data to take place.

        update_title(str):
        The title of the update that is to be scheduled. This title was inputted by the user
        using the front-end input widgets. This variable is passed as a parameter to\
        schedule_covid_updates in order to be passed to covid_updates when the update is scheduled\
        using the covidscheduler object's enter() method and covid_updates is called after the\
        correct delay has elapsed.

        repeat(:obj:`bool`, optional):
        The repeat status for the particular update to be scheduled that schedule_covid_updates was\
        called in response to. This boolean is used to determine whether the update widget in the\
        front-end corresponding to the scheduled update is removed after the update of COVID API\
        data has taken place. This is done in the function covid_updates, so it is passed as a\
        parameter to schedule_covid_updates in order to be passed to covid_updates when the update\
        is scheduled using the covidscheduler object and covid_updates is called after the correct\
        delay has elapsed.

    Returns:

        Note: this return is only used in the accompanying testing functions to this application

        list:
        covidscheduler.queue:
        list containing all events currently in the scheduler queue. This list increases in size\
        each time schedule_covid_updates is called/each time a new update event is scheduled.
    """
    update_title=update_title
    global covideventdict
    print(covidcounter-1)
    covideventdict['c%s' % str(covidcounter-1) ] = covidscheduler.enter(
        update_interval, 1, covid_updates, argument = (update_title, repeat))
    #print(covideventdict)
    return covidscheduler.queue

#NEWS DATA HANDLING

removed_articles=[]

news_articles = []

logging.info('List called news_articles for holding the data returned from news_API_request \
has been initialised')

news_data = news_API_request()

def remove_articles(news_data:list, removed_articles:list) -> list:
    """remove_articles from within add_news_articles in order to ensure no news articles a user has\
    previously deleted from the front-end of the dashboard via each article widget 'X' button are\
    displayed again when new news article data is returned from
    the news API.

    Args:
        news_data(list):
        The list of dictionaries returned from the news API (through the news_API_request\
        function), with each dictionary representing a respective news article. This is iterated\
        over in order to index the 'title' key of each dictionary (article) to see if it is in the\
        array of removed articles (described below). If a title is found in both the news API data\
        and the removed articles list, then the news articles with that title is removed from the\
        news API data.

        removed_articles(list):
        The list of titles of removed articles which is appended to each time a user deletes an\
        article widget, with the corresponding title of said widget.

    Returns:

        Note: this return is only used in the accompanying testing functions to this application

        list:
        news_data - returns an updated version of the news_data variable passed as an argument to\
        the function which was the list of dictionaries returned from the news API (through the\
        news_API_request function). This new version of news_data will have all articles removed\
        with titles that are contained in the removed_articles list.

    """
    i = 0
    while i!= len(news_data):
        if news_data[i]['title'] in removed_articles:
            news_data.remove(news_data[i])
            if i>=1:
                i-=1
            else:
                i=0
                pass
        else:
            i+=1
    return news_data

newseventdict = {}


def add_news_articles(update_title:str=None, repeat:bool=None) -> list:
    """add_news_articles is called initially when the program is run to display the first set of\
    covid news articles returned from the news API on the front-end template and subsequent times\
    when a scheduled update of news API data is to occur. The function makes 1 news API call\
    (using the news_API_request function), followed by a call of remove_articles to ensure all news\
    articles previously deleted by a user are removed from the list returned from the API request.\
    Next, it updates the global list news_articles (defined in the global namespace) in order to\
    update the news article widgets the data dashboard displays. It does this by appending
    a dictionary to said list corresponding to each news article in the list returned from the API\
    request function (with removed articles not included). If the scheduled update the function is\
    called in response to is not a repeated update, then the update dictionary in the global list,\
    updates, that is corresponding to the displayed update widget for the scheduled news update is\
    deleted from the front-end due to the update having been completed.


    Args:
        update_title(:obj:`str`, optional):
        The title of the scheduled update that was scheduled by the user using the front-
        end widgets. This variable is passed as a parameter to add_news_articles in order to be\
        used to remove the corresponding update widget in the front-end after the update of news\
        API data has taken place.

        repeat(:obj:`bool`, optional):
        The repeat status of the particular scheduled update that add_news_articles was called in
        response to. This boolean is used to determine whether the update widget in the front-end\
        corresponding to the scheduled update is removed after the update of news API data has\
        taken place.

    Returns:

        Note: this return is only used in the accompanying testing functions to this application

        list: news_articles - global list variable which holds dictionaries for each news article.\
        Returned containing a dictionary for each article in the news API data list, minus the\
        articles of which their titles reside in the removed_articles list and were subsequently\
        removed from the news API data.
    """
    global updates
    global news_data
    update_title=update_title
    news_data = news_API_request()
    logging.info('news_API_request call has occurred')
    news_articles.clear()
    remove_articles(news_data, removed_articles)
    logging.info('any news articles previously deleted by the user have been removed from the News \
API data just returned from news_API_request')
    for j in news_data:
        newsdictionary = {'title':j['title'], 'content':j['description']}
        news_articles.append(newsdictionary)
    if repeat == False:
        if update_title != None:
            for i in range(len(updates)):
                if updates[i]['title'] == update_title:
                    logging.info('News update widget has been deleted as\
 scheduled update has occurred at desired time and update was not repeating')
                    del updates[i]
                    break
    #print("News Done")
    logging.info("Newest Data from the News API has been retrieved and stored")
    return news_articles

def schedule_add_news_articles(update_interval:int, update_title:str, repeat:bool=False) -> list:
    """schedule_add_news_articles is called when a user wishes to schedule an update of news data\
    from the news API on the dashboard at a given time. The function adds each scheduled event to a\
    dictionary that serves as a historical logging of every news data update event ever scheduled.

    Args:
        update_interval(int):
        The integer delay interval in seconds that is passed to the newscheduler scheduler object\
        using the enter() method, to specify the duration the scheduler should wait before calling\
        the function associated with the scheduled event; in this case, add_news_articles. This\
        interval is user-specified and is the time they enter for when they want an update of the\
        news API data to take place.

        update_title(str):
        The title of the update that is to be scheduled. This title was inputted by the user
        using the front-end input widgets. This variable is passed as a parameter to\
        schedule_add_news_articles in order to be passed to add_news_articles when the update is\
        scheduled using the newscheduler object's enter() method and add_news_articles is called\
        after the correct delay has elapsed.

        repeat(:obj:`bool`, optional):
        The repeat status for the particular update to be scheduled that schedule_add_news_articles\
        was called in response to. This boolean is used to determine whether the update widget in\
        the front-end corresponding to the scheduled update is removed after the update of news API\
        data has taken place. This is done in the function add_news_articles, so it is passed as a\
        parameter to schedule_add_news_articles in order to be passed to add_news_articles when the\
        update is scheduled using the newscheduler object and add_news_articles is called after the\
        correct delay has elapsed.

    Returns:

        Note: this return is only used in the accompanying testing functions to this application

        list:newscheduler.queue:
        list containing all events currently in the scheduler queue. This list increases in size\
        each time schedule_add_news_articles is called/each time a new update event is scheduled.
    """
    update_title=update_title
    global newseventdict
    newseventdict['n%s' % str(newscounter-1) ] = newscheduler.enter(
        update_interval, 1, add_news_articles, argument = (update_title, repeat))
    #print(newseventdict)
    return newscheduler.queue


add_news_articles()
logging.info('Data returned from news_API_request has been used for the initial news articles \
displayed upon first running of the program/application')


#DECORATOR METHOD

@app.route('/index')
def index():
    """index is a decorator method which is called whenever the http://127.0.0.1:5000/index URL is\
    visited by a user in a web browser. This function handles the user's inputs by calling\
    different functions based on given front-end events in the template, such as, users entering\
    a time for an update, entering a title for said update, selecting whether they would like to\
    update covid and/or news data via the respective checkbox widgets and selecting whether they\
    want the update to repeat each day by selecting the repeat checbox widget. This function also\
    calls the above defined schedule functions after calculating the delay until an update of a\
    particular type of data is to take place. This decorator also handles the possibility that the\
    time for a scheduled update that the user has inputted in the interface is less than the\
    current time and in that case, would schedule the event for the next day at that time. The\
    function also handles the manual deletion of news article widgets and update widgets from the\
    front-end interface by the user. When a user manually deletes an update widget, the update\
    event in the scheduler queue is cancelled. This could be in the covidscheduler queue or the\
    newscheduler queue depending on the update type. The decorator also ensures that for any\
    repeated scheduled updates, on each 60 second page refresh, it checks whether that update\
    hasn't already been cancelled and whether there is an update event with the same title\
    currently in the scheduler queue. If there isn't one in the queue and the update hasn't been\
    cancelled, then a new repeat of that update is scheduled for the next day 24hrs later. This\
    would happen immediately after the given day's repeat of that update has occurred. Likewise,\
    if the update has been cancelled, then a repeat of it is not scheduled for any further day.


    Args:
        None-type

    Returns:

        render_template function with required variables passed as parameters in order to render\
        the front-end template (index.html) correctly with intended covid and news API data upon a\
        user visiting the URL, http://127.0.0.1:5000/index and each subsequent page refresh.


    """
    newscheduler.run(blocking=False)
    covidscheduler.run(blocking = False)
    global covidcounter
    global newscounter
    global news_articles
    update_time = request.args.get("update")
    global updates
    global historical_covid_updates
    global historical_news_updates

    if update_time:
        update_label = request.args.get("two")
        if update_label:
            repeating=False
            if "repeat" in request.args:
                repeating = True
            if "covid-data" in request.args:
                no_duplicate_names = False
                while no_duplicate_names == False:
                    no_duplicate_names = True
                    for item in updates:
                        update_title_present_already = item["title"]
                        if "Covid Update: " + update_label + " at" == update_title_present_already:
                            update_label += " i"
                            no_duplicate_names = False
                if "News" in update_label:
                    """To prevent a covid update with "News" in its title being mistaken for a
covid update widget when being deleted from the interface"""
                    update_label=update_label.replace("N","n")
                if repeating == True:
                    dictionary= {'title': "Repeating Covid Update: " + update_label + " at",
                             'content': update_time, 'repeat': repeating}
                else:
                    dictionary= {'title': "Covid Update: " + update_label + " at",
                             'content': update_time, 'repeat': repeating}
                updates.append(dictionary)
                logging.info('Dictionary for given Covid update has been added to global "updates" \
list')
                historical_covid_updates.append(dictionary)
                covidcounter+=1

                current_time = datetime.datetime.now()
                logging.info('The current time has been retrieved in datetime format')
                update_time_split = update_time.split(":")
                wanted_time = current_time.replace(hour=int(update_time_split[0]),
                                                   minute=int(update_time_split[1]), second=0)
                logging.info('The desired update time inputted by the user at the front end was \
converted to datetime format')
                if wanted_time < current_time:
                    wanted_time.replace(day=wanted_time.day + 1)
                    delay = abs(wanted_time - current_time).total_seconds()
                    logging.info('The inputted desired update time has been updated to be the same \
time but for the next day/tomorrow')
                    logging.info('The delay in seconds until the inputted update time has been \
calculated')
                    #print(delay)

                else:
                    current_time = str(datetime.datetime.now().hour)+":"+str(
                        datetime.datetime.now().minute)
                    delay = hhmm_to_seconds(str(update_time)) - hhmm_to_seconds(current_time)
                    logging.info('The delay in seconds until the inputted update time has been\
calculated')
                    #print(delay)

                schedule_covid_updates(delay, dictionary['title'], repeating)
                logging.info('Covid Data Update "' + update_label + '" Scheduled at '+str(
                    update_time))
                if repeating ==True:
                    logging.info('The update is a repeating update')
                else:
                    logging.info('The update is not a repeating update')

            if "news" in request.args:
                no_duplicate_names = False
                while no_duplicate_names == False:
                    no_duplicate_names = True
                    for item in updates:
                        update_title_present_already = item["title"]
                        if "News Update: " + update_label + " at" == update_title_present_already:
                            update_label += " i"
                            no_duplicate_names = False
                if "Covid" in update_label:
                    """To prevent a news update with "Covid" in its title being mistaken for a
covid update widget when being deleted from the interface"""
                    update_label=update_label.replace("C","c")
                if repeating == True:
                    dictionary= {'title': "Repeating News Update: " + update_label + " at",
                             'content': update_time, 'repeat': repeating}
                else:
                    dictionary= {'title': "News Update: " + update_label + " at",
                             'content': update_time, 'repeat': repeating}
                updates.append(dictionary)
                logging.info('Dictionary for given news update added to updates list')
                historical_news_updates.append(dictionary)
                newscounter+=1

                current_time = datetime.datetime.now()
                logging.info('The current time has been retrieved in datetime format')
                update_time_split = update_time.split(":")
                wanted_time = current_time.replace(hour=int(update_time_split[0]), minute=int(
                    update_time_split[1]), second=0)
                logging.info('The desired update time inputted by the user at the front end was \
converted to datetime format')
                if wanted_time < current_time:
                    wanted_time.replace(day=wanted_time.day + 1)
                    delay = abs(wanted_time - current_time).total_seconds()
                    logging.info('The inputted desired update time has been updated to be the same \
time but for the next day/tomorrow')
                    logging.info('The delay in seconds until the inputted update time has been \
calculated')
                    #print(delay)

                else:
                    current_time = str(datetime.datetime.now().hour)+":"+str(
                        datetime.datetime.now().minute)
                    delay = hhmm_to_seconds(str(update_time)) - hhmm_to_seconds(current_time)
                    logging.info('The delay in seconds until the inputted update time has been \
calculated')
                    #print(delay)

                schedule_add_news_articles(delay, dictionary['title'], repeating)
                logging.info('News Data Update "' + update_label +  '" Scheduled at '+str(
                    update_time))
                if repeating ==True:
                    logging.info('The update is a repeating update')
                else:
                    logging.info('The update is not a repeating update')
            else:
                logging.warning('WARNING: No update was scheduled as neither the "Update covid \
data" nor the "Update news articles" checkboxes were selected by the user')


    delete_news_widget = request.args.get("notif")
    if delete_news_widget:
        for article in news_articles:
            if article['title'] == delete_news_widget:
                removed_articles.append(article['title'])
                #print (removed_articles)
                news_articles.remove(article)
                #print(news_articles)
                break

    delete_update_widget = request.args.get("update_item")
    if delete_update_widget:
        if "Covid" in delete_update_widget:
            for j in range(len(historical_covid_updates)):
                if historical_covid_updates[j]['title'] == delete_update_widget:
                    try:
                        if historical_covid_updates[j]['repeat']==True:
                            for i in covidscheduler.queue:
                                if i.argument[0]== historical_covid_updates[j]['title']:
                                    covidscheduler.cancel(i)
                                    for z in covideventdict:
                                        if covideventdict[z].argument[0]== historical_covid_updates[
                                            j]['title']:
                                            cancelledupdatesarray.append(z)

                            logging.info('Covid Update has been cancelled')
                            logging.info('All scheduled repeats of this update have also been \
cancelled and the update will not be rescheduled')
                        else:
                            for i in covidscheduler.queue:
                                if i.argument[0]== historical_covid_updates[j]['title']:
                                    covidscheduler.cancel(i)
                                    for z in covideventdict:
                                        if covideventdict[z].argument[0]== historical_covid_updates[
                                            j]['title']:
                                            cancelledupdatesarray.append(z)
                            logging.info('Covid Update has been cancelled')

                    except ValueError:
                        break
            print(covidscheduler.queue)

        else:
            print(historical_news_updates)
            print(newseventdict)
            for j in range(len(historical_news_updates)):
                if historical_news_updates[j]['title'] == delete_update_widget:
                    try:
                        if historical_news_updates[j]['repeat']==True:
                            for i in newscheduler.queue:
                                if i.argument[0]== historical_news_updates[j]['title']:
                                    newscheduler.cancel(i)
                                    for z in newseventdict:
                                        if newseventdict[z].argument[0]== historical_news_updates[
                                            j]['title']:
                                            cancelledupdatesarray.append(z)
                            logging.info('News Update has been cancelled')
                            logging.info('All scheduled repeats of this update have also been \
cancelled and the update will not be rescheduled')
                        else:
                            for i in newscheduler.queue:
                                if i.argument[0]== historical_news_updates[j]['title']:
                                    newscheduler.cancel(i)
                                    for z in newseventdict:
                                        if newseventdict[z].argument[0]== historical_news_updates[
                                            j]['title']:
                                            cancelledupdatesarray.append(z)
                            logging.info('News Update has been cancelled')
                    except ValueError:
                        break


        for i in range(len(updates)):
            if updates[i]['title'] == delete_update_widget:
                if "Covid" in updates[i]['title']:
                    logging.info('Covid update widget has been deleted')
                else:
                    logging.info('News update widget has been deleted')
                del updates[i]
                break


    if len(covidscheduler.queue)>=0:
        for i in range(len(covideventdict)):
            list_of_queued_titles = []
            for k in covidscheduler.queue:
                list_of_queued_titles.append(k.argument[0])

            print(list_of_queued_titles)
            print(covideventdict)
            try:
                list_of_queued_titles.index(covideventdict['c%s' % str(i)].argument[0])
                reschedule_flag = False
            except:
                reschedule_flag = True


            if reschedule_flag == False:
                pass

            print(reschedule_flag)
            if ('c%s' % str(i)) not in cancelledupdatesarray:
                if (covideventdict['c%s' % str(i)].argument[1] == True) and reschedule_flag == True:
                    if len(covidscheduler.queue)!=0:
                        covidcounter+=1
                    #print("1 added to the counter within repeat conditional")

                    schedule_covid_updates(24*60*60, covideventdict['c%s' % str(i)].argument[0] ,
                                           True)
                    print(covideventdict['c%s' % str(i)].argument[0], "rescheduled")
                    logging.info("Covid update event has been rescheduled")
                    reschedule_flag == False

    if len(newscheduler.queue)>=0:
        for i in range(len(newseventdict)):
            list_of_queued_titles = []
            for k in newscheduler.queue:
                list_of_queued_titles.append(k.argument[0])

            print(list_of_queued_titles)
            print(newseventdict)
            try:
                list_of_queued_titles.index(newseventdict['n%s' % str(i)].argument[0])
                reschedule_flag = False
            except:
                reschedule_flag = True


            if reschedule_flag == False:
                pass

            print(reschedule_flag)
            if ('n%s' % str(i)) not in cancelledupdatesarray:
                if (newseventdict['n%s' % str(i)].argument[1] == True) and reschedule_flag == True:
                    if len(newscheduler.queue)!=0:
                        newscounter+=1
                    #print("1 added to the counter within repeat conditional")

                    schedule_add_news_articles(24*60*60, newseventdict['n%s' % str(i)].argument[0] ,
                                               True)
                    print(newseventdict['n%s' % str(i)].argument[0], "rescheduled")
                    logging.info("News update event has been rescheduled")
                    reschedule_flag == False





    print(covidscheduler.queue)
    print(newscheduler.queue)
    #print(covidcounter)
    #print(newscounter)
    return render_template('index.html',
                           title='COVID-19 Data Dashboard',
                           location = 'Exeter',
                           local_7day_infections = local_area_7day_infections,
                           nation_location = 'England',
                           hospital_cases = "National Hospital Cases: " + str(
                               hospital_cases_for_nation),
                           national_7day_infections = national_area_7day_infections,
                           deaths_total= "Cumulative Deaths Within 28 Days Of A Positive Test By\
Death Date: "+ str(deaths_total_for_nation),
                           updates = updates,
                           news_articles = news_articles[0:8],
                           image = "covid19-information-and-updates.jpg")


if __name__ == '__main__':
    app.run()

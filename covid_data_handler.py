import json
import sched
import time
from typing import Tuple
from uk_covid19 import Cov19API



covid19scheduler = sched.scheduler(time.time, time.sleep)

def parse_csv_data(csv_filename: str) -> list:
    """ parse_csv_data extracts data from a csv file and formats it as a list
        of strings with each string in the list representing a unique row in
        the csv file

        Args:
            csv_filename(str):
            The file name of the csv file contained within the same directory of covid_handler.py
            that is to be opened and read from by this function

        Returns:
            list:
            allrows: A list of strings with each respective string representing a given row from
            the csv file.

    """
    csv_file = open(csv_filename, 'r')
    allrows = csv_file.readlines()
    csv_file.close()
    return allrows


#print(parse_csv_data("nation_2021-10-28.csv"))


def process_covid_csv_data(covid_csv_data:list) -> Tuple[int,int,int]:
    """process_csv_data processes CSV data to find the total COVID cases over the past 7
       days, the most recent number of hospital cases and the cumulative deaths.

        Args:
            covid_csv_data(list):
            A list of strings returned from parse_csv_data with each string in the list
            representing a unique row in the csv file passed to the parse_csv_data function

        Returns: multi-variable return
            int:
            last7days_cases: An integer showing the total number of COVID-19 cases over
            the past 7 days in the static csv file

            int:
            current_hospital_cases: An integer showing the total number of hospital cases
            at the most recent date in the csv data

            int:
            total_deaths:
            An integer showing the total/cumulative deaths due to COVID-19 from the data
            in the static csv file
    """
    last7days_cases = 0
    day_counter=0
    first_entry_checked=False
    for row in covid_csv_data:
        if row.split(',')[5] != "" and row.split(',')[5]!="hospitalCases":
            current_hospital_cases = int(row.split(',')[5].strip())
            break
    for row in covid_csv_data:
        if row.split(',')[4]!= "" and row.split(',')[4]!= "cumDailyNsoDeathsByDeathDate":
            total_deaths= int(row.split(',')[4].strip())
            break
    for row in covid_csv_data:
        sublist=row.split(',')
        #print((row.split(',')[6]))
        if ((sublist[6]).strip()!= "") and ((sublist[6]).strip()!="newCasesBySpecimenDate"):
            if first_entry_checked==True:
                day_counter+=1
                #print((row.split(',')[6]))
                last7days_cases += int((row.split(',')[6]).strip())
                if day_counter == 7:
                    break
            else:
                first_entry_checked=True
                continue

    return last7days_cases, current_hospital_cases, total_deaths

#print(process_covid_csv_data(parse_csv_data ('nation_2021-10-28.csv' )))

location_name = json.loads(open("config.json").read())["location"]
location_type_json= json.loads(open("config.json").read())["location_type"]

def covid_API_request(location:str=location_name, location_type:str=location_type_json) -> dict:
    """covid_API_request filters the data returned from the Public Health England COVID-19 API to
       only include data relevant to the specific location type and location name which were
       passed as parameters to the covid_API_request function. It further filters the data returned
       to only include the relevant metrics to be displayed on the front-end template. Finally the\
       data returned from the API which is in the form of a list is returned from the\
       covid_API_request function as a dictionary

       Args:
           location(:obj:`str`, optional):
           The string name of a location for which the api should return statistical data for.
           Particularly, this could be the name of a local or national location. In this\
           application, the parameter takes the value of "England" and "Exeter" respectively on\
           different occasions.

           location_type(:obj:`str`, optional):
           The string detailing the type of location for which data from the api
           should be returned for, there are a limited number of options but for this program,
           "ltla" and "nation" are 2 classifications used in the different calls of
           covid_API_request.

       Returns:
           dict:
           covidapidictionary: The dictionary returned containing all the relevant data from the\
           Public Health England API, satisfying the location classifications and metric limits.
    """
    filts = [
        'areaType='+location_type,
        'areaName='+location
    ]

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "hospitalCases": "hospitalCases",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
    }

    api = Cov19API(filters=filts, structure=cases_and_deaths)

    data = api.get_json()["data"][0:30]

    covidapidictionary={}
    covidapidictionary["data"]=data

    return covidapidictionary

def schedule_covid_updates(update_interval:int, update_name:str) -> None:
    """schedule_covid_updates schedules a new call of the covid_API_request
       function to happen after the delay passed as the value of the parameter
       update_interval has elapsed. This happens by an event being added to the
       queue of the covid19scheduler object.

       Args:
           update_interval(str):
           The integer delay interval in seconds that is passed to the covid19scheduler scheduler\
           object using the enter() method, to specify the duration the scheduler should wait\
           before calling the function associated with the scheduled event;
           in this case, covid_API_request.

           update_name(str):
           The name of the scheduled covid_API_request call
           This is not assigned to a variable at all so is trivial in this situation.

       Returns:
           None
    """
    """THIS FUNCTION (FROM THIS MODULE) IS NOT ACTUALLY USED IN MAIN.PY INSTEAD FUNCTIONALITY IS\
EMPLOYED ELSEWHERE IN MAIN.PY WITHIN FUNCTION OF SAME NAME"""
    covid19scheduler.enter(update_interval, 1, covid_API_request)
    covid19scheduler.run(blocking=False)


#print(covid_API_request("England", "nation"))

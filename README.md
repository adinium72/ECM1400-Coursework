# ECM1400 Personalised COVID-19 Data Dashboard Coursework

This application is a personalised (automated) COVID-19 data dashboard for the "ECM1400 - Programming" module's continuous assessment coursework. 
The coursework is 100% of the module's grade and adheres to the specification and mark scheme guidelines detailed in the links below:

+ [Coursework Specification](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/CA-specification.pdf)
+ [Coursework Mark Scheme](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/CA-mark-scheme.pdf)

The data dashboard application coordinates information about the UK's local and national COVID infection rates from the official Public Health England API 
and news stories (articles) about COVID-19 from the news API provided by https://newsapi.org/.

The dashboard helps a user visualize the data streams provided by these APIs and enables users to schedule and cancel updates for the COVID data and news 
articles respectively by retrieving the newest data from each of the APIs via use of a front-end web template. Users can also choose to make these updates 
repeat at the same time daily.

## Features

Here is an example of what the personalised data dashboard looks like. Particularly this is the front-end web template the data dasboard makes use of to provide
a graphical user interface to the user:

![Dash board photo](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Capture%200.PNG)

## Getting Started

### Prerequisites

The Python version used for development of this application/program was:
+ [Python 3.8.0](https://www.python.org/downloads/release/python-380/)

This can be downloaded by clicking the link above.

Any subsequent releases of python (3.8.0+) can also be used

The following packages will also need to be installed for successful use of the application:
+ [flask](https://flask.palletsprojects.com/en/2.0.x/installation/)
+ [requests](https://pypi.org/project/requests/)
+ [uk-covid19](https://github.com/publichealthengland/coronavirus-dashboard-api-python-sdk)
+ [newsapi](https://newsapi.org/docs/client-libraries/python)
+ [pytest](https://docs.pytest.org/en/6.2.x/getting-started.html)

Guidance regarding how to install these Python packages in the command prompt within Windows®
is contained in the links above as well as below in this README file.

The following modules built in to Python (within the Python Standard Library) are also required:

+ [json](https://docs.python.org/3/library/json.html)
+ [csv](https://docs.python.org/3/library/csv.html)
+ [datetime](https://docs.python.org/3/library/datetime.html)
+ [sched](https://docs.python.org/3/library/sched.html)
+ [time](https://docs.python.org/3/library/time.html)
+ [logging](https://docs.python.org/3/library/logging.html)
+ [typing](https://docs.python.org/3/library/typing.html)


The above links are to bring you to the appropriate documentation for each respective Python module in the list.

Furthermore, the module [***Lab_4_time_conversions.py***](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Lab_4_time_conversions.py) 
(which should reside in the same directory as main.py and is provided in the GitHub repository) which was created by the author 
of this application is required, as it is imported in the body of ***main.py***.

### Installation

1. First get a unique personal API key for using the News API and its data within the application from [here](https://newsapi.org/register)
2. Put this API key into the provided config.json file. This can be found [here](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/config.json) 
3. Install Python 3.8+ (using the link provided in ***Prerequisites***)
4. Install the required Python packages (no virtual environments used) by typing the following commands 
into the Windows® command prompt:

    ```sh
    pip install Flask
    ```
    ```sh
    python -m pip install requests
    ```
    ```sh 
    pip install uk-covid19
    ```
    ```sh 
    pip install newsapi-python
    ```
    

## Usage

To run the application open the Windows® command prompt, navigate to the correct directory in which main.py has
been downloaded into from this repository, by means of the ***cd*** command and then type the command:
```sh
python main.py
```

Next, open a browser; preferably Google Chrome™ and enter the following URL into the search bar: 

```sh 
http://127.0.0.1:5000/index
```

The front-end web template of the dashboard should then display as a GUI shown below with
data for different UK COVID-19 metrics (returned from the COVID API) displaying in the middle and removable widgets displaying news
articles related to COVID-19 (returned from the news API):

![Dash board photo](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Capture%201.PNG)

From here you can delete news article widgets by clicking the **'X'** button on each respective widget (see before and after below):

**Before:**


![Dash board photo](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Capture%202.PNG)

**After:**


![Dash board photo](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Capture%203.PNG)

You can also schedule a named update of the COVID API data and/or the news articles displayed from the news API at a given time.
This is done by entering a time and title into the relevant input widgets provided on the dashboard interface. The relevant checkboxes for
updating the Covid data and news data that are displayed on the dashboard should also be selected appropriately when scheduling an update. Then,
the update is scheduled when the submit button widget is clicked.

There is also a checkbox widget to select whether you want a given scheduled update to repeat at the same inputted time each day from thereon out.

After a given update (covid and/or news) has been scheduled by the user, a widget for that update appears on the left hand side of the interface.
These update widgets like the news article widgets can be manually deleted by clicking the **'X'** button on each respective widget.

Covid and news updates can be scheduled independently of each other if need be.

See below, an example of scheduling a covid and news update for 12:01PM:

![Dash board photo](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Capture%204.PNG)

See below, an example of deleting the 2 update widgets in the above picture from the interface:

**Deleting the news update widget:**


![Dash board photo](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Capture%205.PNG)


**Deleting the covid update widget:**


![Dash board photo](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Capture%206.PNG)


**Note:** When news widgets are deleted from the interface, they do not get displayed again on the interface 
to the user when a scheduled news update occurs.

**Note:** 8 news article widgets are always displayed on the interface to the user at any 1 time. Deleting 1 will cause another from the pool of relevant
news API articles to take its place.

**Note:** When update widgets are deleted from the interface, the scheduld update the respective widget represented gets cancelled and does not occur at its
planned time.

**Note:** If a non-repeating scheduled update occurs as planned and the data on the dashboard interface is updated to be the most recent from the Covid and/or 
news APIs, then the update widget associated with that update is deleted from the interface automatically.

**Note:** If a repeating scheduled update occurs as planned and the data on the dashboard interface is updated to be the most recent from the Covid and/or 
news APIs, then the update widget associated with that update remains and keeps being displayed on the interface automatically.

Here is an example of what a widget for a repeating scheduled Covid update looks like:

![Dash board photo](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi/blob/main/Capture%207.PNG)


## Testing

1. Install the required Python package, pytest, (no virtual environments used) by typing the following command 
into the Windows® command prompt:

    ```sh
    pip install -U pytest
    ```

2. To run pytest and thus run the test functions provided, open the Windows® command prompt, navigate to the correct directory in which
test_covid_data_handler.py, test_news_data_handling.py and test_main.py have been downloaded into from the GitHub repository, 
by means of the ***cd*** command and then type the command:

```sh
pytest
```

The test modules will all be executed and all test functions within them should pass successfully. This will be apparent from within the command
prompt


## Development Notes:

The Python package ***pylint*** was also used during development, particularly to shephard consistency in line length, variable
identifiers, indentation and whitespace.

This was installed via the Windows® command prompt, using the command:

```sh
pip install pylint
```
    
Pylint was then run by opening the Windows® command prompt, navigating to the correct directory in which
main.py, covid_data_handler.py and covid_news_handling.py resided together, and typing:

    ```sh
    python -m pylint main.py
    ```
    
    OR
    
    ```sh
    python -m pylint covid_data_handler.py
    ```
    
    OR
    
    ```sh
    python -m pylint covid_news_handling.py
    ```

into the Windows® command prompt. A report of styling and other programming errors present in these modules was
then returned and used by the Author to aid development and refine the code. This package does not need to be installed
by the user and this section of the README is simply for reference.


## Authors

**Author**: Adam Cherfi (*adinium72*)

**Contact Email**: amc267@exeter.ac.uk

**Project Link**: [https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi](https://github.com/adinium72/ECM1400-Coursework---Adam-Cherfi)

## Licence

Disctributed under the MIT License (see below):

**MIT License**

Copyright © <2021> Adam Cherfi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

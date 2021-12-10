# ECM1400 Personalised COVID-19 Data Dashboard Coursework

This application is a personalised (automated) COVID-19 data dashboard for the "ECM1400 - Programming" module's continuous assessment coursework. 
The coursework is 100% of the module's grade and adheres to the specification and mark scheme guidelines detailed in the links below:

+ INSERT GITHUB LINK
+ INSERT GITHUB LINK

The data dashboard application coordinates information about the UK's local and national COVID infection rates from the official Public Health England API 
and news stories (articles) about COVID-19 from the news API provided by https://newsapi.org/.

The dashboard helps a user visualize the data streams provided by these APIs and enables users to schedule and cancel updates for the COVID data and news 
articles respectively by retrieving the newest data from each of the APIs via use of a front-end web template. Users can also choose to make these updates 
repeat at the same time daily.

## Features

Here is an example of what the personalised data dashboard looks like. Particularly this is the front-end web template the data dasboard makes use of to provide
a graphical user interface to the user:

![Dash board photo]()

## Getting Started

### Prerequisites

The Python version used for development of this application/program was:
+ [Python 3.8.0](https://www.python.org/downloads/release/python-380/)

This can be downloaded by clicking the link above.

Any subsequent releases of python (3.8.0+) can also be used

The following packages will also need to be installed for successful use of the program:
+ [flask](https://flask.palletsprojects.com/en/2.0.x/installation/)
+ [requests](https://pypi.org/project/requests/)
+ [uk-covid19](https://github.com/publichealthengland/coronavirus-dashboard-api-python-sdk)
+ [newsapi](https://newsapi.org/docs/client-libraries/python)

Guidance regarding how to install these Python packages in the command prompt within Windows®
is contained in the links above as well as below in this README file.

The following modules built in to Python (within the Python Standard Library) are also required:

+ [json](https://docs.python.org/3/library/json.html)
+ [csv](https://docs.python.org/3/library/csv.html)
+ [datetime](https://docs.python.org/3/library/datetime.html)
+ [sched](https://docs.python.org/3/library/sched.html)
+ [time](https://docs.python.org/3/library/time.html)
+ [logging](https://docs.python.org/3/library/logging.html)


The above links are to bring you to the appropriate documentation for each respective Python module in the list.

### Installation

1. First get a unique personal API key for using the News API and its data within the application from [here](https://newsapi.org/register)
2. Put this API key into the provided config.json(INSERT GITHUB LINK) file.
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

![Dash board photo]()

From here you can delete news article widgets by clicking the **'X'** button on each respective widget (see before and after below):

![Dash board photo]()

You can also schedule a named update of the COVID API data and/or the news articles displayed from the news API at a given time.
This is done by entering a time and title into the relevant input widgets provided on the dashboard interface. The relevant checkboxes for
updating the Covid data and news data that are displayed on the dashboard should also be selected appropriately when scheduling an update. Then,
the update is scheduled when the submit button widget is clicked.

There is also a checkbox widget to select whether you want a given scheduled update to repeat at the same inputted time each day from thereon out.

After a given update (covid and/or news) has been scheduled by the user, a widget for that update appears on the left hand side of the interface.
These update widgets like the news article widgets can be manually deleted by clicking the **'X'** button on each respective widget.

Covid and news updates can be scheduled independently of each other if need be.

See below, an example of scheduling a covid and news update for 12:01PM:

![Dash board photo]()

See below, an example of the before and after of deleting the update widgets from the interface:

![Dash board photo]()

**Note:** When news widgets are deleted from the interface, they do not get displayed again on the interface 
to the user when a scheduled news update occurs.

**Note:** 8 news article widgets are always displayed on the interface to the user at any 1 time. Deleting 1 will cause another from the pool of relevant
news API articles to take its place.

**Note:** When update widgets are deleted from the interface, the scheduld update the respective widget represented gets cancelled and does not occur at its
planned time.

**Note** If a non-repeating scheduled update occurs as planned and the data on the dashboard interface is updated to be the most recent from the Covid and/or 
news APIs, then the update widget associated with that update is deleted from the interface automatically.

**Note** If a repeating scheduled update occurs as planned and the data on the dashboard interface is updated to be the most recent from the Covid and/or 
news APIs, then the update widget associated with that update remains and keeps being displayed on the interface automatically.

## Authors

**Author**: Adam Cherfi (*adinium72*)

**Contact Email**: amc267@exeter.ac.uk

**Project Link**: INSERT GITHUB LINK

## License

Disctributed under the MIT License (see below):

**MIT License**

Copyright © <2021>  <Adam Cherfi>

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

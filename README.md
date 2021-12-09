# ECM1400 Personalised Covid-19 Data Dashboard Coursework

The following application is the personalised Covid-19 data dashboard for the ECM1400 module's continuous assessment coursework. 
The coursework is 100% of the module's grade and adheres the specification and mark scheme guidelines detailed in the links below:

INSERT GITHUB LINK
INSERT GITHUB LINK

The data dashboard application coordinates information about the COVID infection rates from the official Public Health England API and news
stories (articles) about COVID-19 from the news API provided by "https://newsapi.org/".

The dashboard helps a user visualize the data streams provided by these APIs and enables users to schedule and cancel updates for the COVID data and news 
articles respectively by retrieving the newest data from each of the APIs. Users can also choose to make these updates repeat at the same time daily.

## Features or examples

Here is what the dashboard looks like:

![Dash board photo]()

## Requirement(s)

These are the requirements:
+ [python 3.9 +](www.python.org/downloads/release/python-399)
+ [uk-covid19](https://github.com/publichealthengland/coronavirus-dashboard-api-python-sdk)
+ [newsapi](https://newsapi.org/docs/client-libraries/python)

## Installation / Getting Started

1. First get an api from [here](https://newsapi.org/register)
2. Then put this apikey into apikey.txt.
3. Then install python3.9 +
4. You can either install the modules or use the virtual environments to run the project:
Without venvs:
    ```sh 
    pip3 install uk-covid19
    ```
    ```sh 
    pip3 install newsapi-python
    ```
    ```sh
    python3 main.py
    ```
    ```sh 
    Go to localhost:5000/index
    ```

## Usage

## Contributors

Adam Cherfi (adinium72)

## License

MIT LICENSE

Copyright (c) <2021> <Adam Cherfi>

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

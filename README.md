# team azrael <img src="https://d1lss44hh2trtw.cloudfront.net/assets/article/2015/07/06/Azrael_Returns_feature.jpg" height="40">
Mohtasim Howlader, Jack Lu, Jason Tung

**[Devlog](https://github.com/mhowlader/sd_p02/blob/master/doc/devlog.txt)**

## Testlet

### Abstract:
Teslet is a Quizlet inspired project which revolves around duplicating Quizlet’s core functionality: logging in, creating, saving, and viewing sets. Team azrael will try to also implement various ways to expedite the process of set creation and reviewing sets, most notably autofill definitions and enabled pronunciation on terms/definitions. Using javascript, we will try to update a container in while reviewing sets to imitate flipping an index card.

### How To Procure Your Own API Keys:
Our project utilizes various APIs, so the user needs a json file with the API keys formatted as such (the skeleton is provided under `/keys/<api_name>):

```
FILE: MSAzureTTS API
CONTENTS:xxxxxxxxxx
```
This will be elaborated upon in the instructions. Just fetch your API keys for now.


All of the APIs we used are hyperlinked in the table below with a brief description. The hyperlinks should be sufficient to get the user started on procuring API keys. Please note that not all of the apis need keys.

api | description
--- | ---
[calendar index](https://www.calendarindex.com/)  | Gives dates of holidays and observances
[sunrise-sunset](https://sunrise-sunset.org/api) | Provides time for sunrise, high noon, and sunset
[darksky](https://darksky.net/dev) | To get the past, current, and future weather at a location
[ipapi](https://ipapi.co/)  | To get the information about location based on ip address
[horoscope-api](https://github.com/tapaswenipathak/Horoscope-API) | To get the daily, weekly, monthly horoscope
[newsapi](https://newsapi.org/) | To get the news or anything
[poemist](https://poemist.github.io/poemist-apidoc/#misc-services) | Get a random poem
[nasa-api](https://api.nasa.gov/) | Used to fetch a picture of location based on long/lat

### Dependencies: 
Our dependencies, as listed in requirements.txt, are as follows:

dependency | version | origin | description
--- | --- | --- | ---
Click | 7.0 | Flask | unused
Flask | 1.0.2 | Flask |  microframework of choice
itsdangerous | 1.1.0 | Flask |  unused
Jinja2 | 2.10 | Flask |  templating language
MarkupSafe | 1.1.0 | Flask |  unused
Werkzeug | 0.14.1 | Flask |  unused
json | n/a | py3.7.1-stdlib |  converts json strings into python dictionaries and vice-versa
os | n/a | py3.7.1-stdlib | take care of file paths
csv | n/a | py3.7.1-stdlib | parsing csv files
sqlite3 | n/a | py3.7.1-stdlib | our db
urllib | n/a | py3.7.1-stdlib |  fetches json data from urls
urllib.request | n/a | py3.7.1-stdlib |  fetches json data from urls


Install our dependencies with the follow command in the root directory of our repo:
```
pip3 install -r requirements.txt
```

### Instructions:
1. Clone the repo

**ssh**
```
git@github.com:mhowlader/sd_p02.git
```

**https**
```
https://github.com/mhowlader/sd_p02.git
```

2. (optional) make a virtual env
```
python3 -m venv <venv_name>
```

3. (optional) activate virtual env
```
. <path-to-venv>/bin/activate
```

4. enter the repo directory
```
cd <path-to-repo>
```

5. install requirements

**python 3.7**
```
pip3 install -r requirements.txt
```

**if in virtual env with python 3.7**
```
pip install -r requirements.txt
```

6a. edit/make files `/keys/<api_name>`.

6b. fill the `<api_name>` file with your corresponding api keys in the following format (the api keys i filled out are made up):
```
FILE: MSAzureTTS API
CONTENTS:xxxxxxxxxx
```

7. run the app.py with python3

**python 3.7**
```
python3 app.py
```

**if in virtual env with python 3.7**
```
python app.py
```

8. go to localhost 127.0.0.1:5000 on any browser

   http://127.0.0.1:5000/

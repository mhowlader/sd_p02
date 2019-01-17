import json, random
from urllib.request import Request, urlopen


oxford=""
with open("../keys/oxford.json") as file:
    oxford=json.load(file)


appid=oxford["appid"]
apikey=oxford["apikey"]

print(appid)
print(apikey)


def get_defin(term):
    '''Get def of term
        URL
        https://developer.oxforddictionaries.com/documentation#!/Dictionary32entries/get_entries_source_lang_word_id
    '''
    BASE_URL = "https://od-api.oxforddictionaries.com/api/v1"
    lang = 'en'
    word_id = term
    with open("../keys/oxford.json") as file:
        oxford=json.load(file)
    appid=oxford["appid"]
    apikey=oxford["apikey"]

get_defin('velocity')

trivia = "https://opentdb.com/api.php?amount=10"

def generate_quiz():
    URL = trivia
    response = urlopen(Request(URL, headers={'User-Agent': 'Mozilla/5.0'})).read()
    info = json.loads(response)

    return info["results"]

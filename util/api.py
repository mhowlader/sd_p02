import json, random
from urllib.request import Request, urlopen


oxford=""
with open("../keys/oxford.json") as file:
    oxford=json.load(file)




def get_defin(term):
    '''Get def of term
        URL
        https://developer.oxforddictionaries.com/documentation#!/Dictionary32entries/get_entries_source_lang_word_id
    '''
    with open("../keys/oxford.json") as file:
        oxford=json.load(file)
    # base_url = "https://od-api.oxforddictionaries.com/api/v1"

    language = 'en'
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/"
    url += term.lower()
    print(url) 
    try:
        r = Request(url, headers = oxford)
        raw = urlopen(r).read()
        data = json.loads(raw)
        #print(data)
    except:
        print("OOF")
    definition = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    print(definition)
    return definition



#get_defin('velocity')

trivia = "https://opentdb.com/api.php?amount=10"

def generate_quiz():
    URL = trivia
    response = urlopen(Request(URL, headers={'User-Agent': 'Mozilla/5.0'})).read()
    info = json.loads(response)

    return info["results"]

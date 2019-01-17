import json, random
from urllib.request import Request, urlopen


oxford=""
with open("../keys/oxford.json") as file:
    oxford=json.load(file)


appid=oxford["appid"]
apikey=oxford["apikey"]

print(appid)
print(apikey)

trivia = "https://opentdb.com/api.php?amount=10"

def generate_quiz():
    URL = trivia
    response = urlopen(Request(URL, headers={'User-Agent': 'Mozilla/5.0'})).read()
    info = json.loads(response)

    return info["results"]

import json, random
from urllib.request import Request, urlopen


oxford=""
with open("../keys/oxford.json") as file:
    oxford=json.load(file)



appid=oxford["appid"]
apikey=oxford["apikey"]

print(appid)
print(apikey)

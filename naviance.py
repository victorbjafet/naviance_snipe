import requests
import json
from time import sleep



with open("node_js_fetch.txt", "r") as fetchnode:
    headers = fetchnode.read()

headers = headers[headers.find("\"headers\": ") + 11:headers.rfind("},") + 1] #isolates json headers

headers = json.loads(headers) #loads json headers to dict

params = {
    "page": "1",
    "limit": "100"
}

target = input("Target school name (must be exact): ")

refresh = None
while not refresh:
    refresh = input("Refresh time (default 5, not recommended too low or you may have issues): ")
    if not refresh:
        refresh = 5
    try:
        refresh = int(refresh)
        if refresh <= 0:
            refresh = None
            print("Refresh value must be greater than 0")
    except:
        refresh = None
        print("Invalid refresh value")

done = False
while not done:
    response = requests.get("https://blue-ridge-api.naviance.com/college-visit/search", headers=headers, params=params)

    dict = json.loads(response.text)["data"]
    for college in dict:
        if college["organizationName"] == target:
            if not college["passedMaxAttendees"]:
                print("SPOT OPEN!!! CLAIMING...")
                requests.put("https://blue-ridge-api.naviance.com/college-visit/" + str(college["id"]), headers=headers)
                print("CLAIMED!!!")
                done = True
            else:
                print("Spot still closed")
            break
    else:
        print("Target school name not found in list of schools")
        done = True
    if not done:
        sleep(5)
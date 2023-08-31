from googlesearch import search
import json
from sys import argv

import requests

dorks = json.load(open("utils/dorks.json"))
googleAPIURL = "https://www.googleapis.com/customsearch/v1"

def checkFileParam():
    if "-f" in argv and (argv.index("-f") + 1 < len(argv)):
        return argv[argv.index("-f") + 1]
    else:
        print("Please provide a file with domains")
        exit()

def getSecrets():
    cxChecks = "-cx" in argv and (argv.index("-cx") + 1 < len(argv))
    keyChecks = "-key" in argv and (argv.index("-key") + 1 < len(argv))
    if keyChecks and cxChecks:
        return {"key": argv[argv.index("-key") + 1],
                "cx": argv[argv.index("-cs") + 1]
                } 
    try:
        secrets = json.load(open("utils/secrets.json"))
        if secrets["key"] != "" and secrets["cx"] != "":
            return secrets
        raise TypeError("Please provide valid secrets")
    except:
        print("Error getting secrets")
        exit()

def removeNullStrings(fileContent):
    aux = []
    for value in fileContent:
        if value == "":
            continue
        aux.append(value)
    return aux

def makeSearchForDomain(dorkReplaced, secrets):
    params = {
        **secrets, 
        "q":dorkReplaced,
        "start": 0
    }
    nextPage = 0
    while True:
        res = requests.get(
            googleAPIURL,
            params=params
        )
        if res.status_code != 200: 
            print(res.status_code)
            print(res.json())
            print(params)
            print("Error getting data in google api")
            exit()
        
        res = res.json()
        if "nextPage" not in res["queries"]:
            break 
        urls = [items["link"] for items in res["items"]]
        printArray(urls)

        nextPage = res["queries"]["nextPage"][0]["startIndex"]
        params["start"] = nextPage
        
def printArray(array):
    for item in array:
        print(item)

def makeSearchForDork(fileContent, secrets):
    for title in dorks:
        dork = dorks[title]
        print(f"Starting dork: {title.upper()}") 
        for domain in fileContent:
            dorkReplaced = dork.replace("target", domain)
            makeSearchForDomain(dorkReplaced, secrets)

if __name__ == "__main__":
    fileName = checkFileParam()
    secrets = getSecrets()

    fileContent = open(fileName).readlines()
    fileContent = [line.replace("\n", "") for line in fileContent]
    fileContent = removeNullStrings(fileContent)
    makeSearchForDork(fileContent, secrets)

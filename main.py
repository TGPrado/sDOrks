from googlesearch import search
import json
from sys import argv

dorks = json.load(open("utils/dorks.json"))

def checkFileParam():
    if "-f" in argv and (argv.index("-f") + 1 < len(argv)):
        return argv[argv.index("-f") + 1]
    else:
        print("Please provide a file with domains")
        exit()

def makeSearchForDomain(domain, dork):
    dorkReplaced = dork.replace("target", domain)
    query = search(dorkReplaced)
    result = []
    for item in query:
        result.append(item)

    return result
    
def printArray(array):
    for item in array:
        print(item)

def makeSearchForDork(fileContent):
    for title in dorks:
        dork = dorks[title]
        print(f"Starting dork: {title.upper()}") 
        for domain in fileContent:
            result = makeSearchForDomain(domain, dork)
            printArray(result)

if __name__ == "__main__":
    fileName = checkFileParam()
    fileContent = open(fileName).readlines()
    fileContent = [line.replace("\n", "") for line in fileContent]    
    makeSearchForDork(fileContent)

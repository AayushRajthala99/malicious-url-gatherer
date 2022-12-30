import os
import wget
import pandas as pd
from datetime import datetime, timezone

urlTimeDifference = None
current_datetime = datetime.now(timezone.utc).strftime("%Y-%m-%d %X")
current_datetime = datetime.strptime(current_datetime, "%Y-%m-%d %X")

urlTimeDifference = 60

countFile = open('./operationFiles/count.txt', 'r')
count = countFile.readline(1)
countFile.close()
urlName = None
filename = None

while (True):
    os.system('clear')  # Clear Teminal on Linux System
    print("========================")
    print("\tURL GATHERER")
    print("========================")
    print("\nURL TYPE:")
    print("\n1. Online URLs\n2. Recent URLs")
    urlType = input("Input URL TYPE: ")

    if ((urlType == '1') or (urlType == '2')):
        if (urlType == '1'):
            urlName = 'Online'
            filename = f"./csvDownloads/{count}-{urlName}-{current_datetime}-UTC-urls.csv"
            wget.download(
                'https://urlhaus.abuse.ch/downloads/csv_online/', filename)
        elif (urlType == '2'):
            urlName = 'Recent'
            filename = f"./csvDownloads/{count}-{urlName}-{current_datetime}-UTC-urls.csv"
            wget.download(
                'https://urlhaus.abuse.ch/downloads/csv_recent/', filename)
        break


def recentURLCheck(urllist, currentDateTime):
    validUrl = []

    for url in zip(urllist["url"], urllist["dateadded"]):
        testValue = url[1]

        testValue = datetime.strptime(testValue, "%Y-%m-%d %X")

        # Time Difference in Minutes
        timeDifference = (((currentDateTime-testValue).seconds) / 60)

        if (timeDifference <= urlTimeDifference):
            validUrl.append(url[0])

    return validUrl


urlList = pd.read_csv(filename, skiprows=8)
# print(urlList)
urlList = urlList[["url", "dateadded"]]

if (urlTimeDifference):
    urlList["dateadded"] = urlList["dateadded"].str.replace(" UTC", "")
    freshUrlList = recentURLCheck(urlList, current_datetime)
else:
    freshUrlList = urlList[["url"]]

freshUrlList = pd.DataFrame(freshUrlList, columns=["url"])
freshUrlList.to_csv("./operationFiles/urlList.csv",
                    index=False, header=False)

count = int(count)
os.system(f"./httpx-operation.sh {count}")
count = count+1
count = str(count)

countFile = open('./operationFiles/count.txt', 'w')
countFile.write(count)
countFile.close()

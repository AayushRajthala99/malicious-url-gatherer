import os
import wget
import pandas as pd
from datetime import datetime, timezone

urlTimeDifference = 30  # Time Difference for Fresh URLs


def recentURLCheck(urllist, currentDateTime):
    validUrl = []

    for url in zip(urllist["url"], urllist["date_added"]):
        testValue = url[1]

        testValue = datetime.strptime(testValue, "%Y-%m-%d %X")

        # Time Difference in Minutes
        timeDifference = (((currentDateTime-testValue).seconds) / 60)

        if (timeDifference <= urlTimeDifference):
            validUrl.append(url[0])

    return validUrl


countFile = open('./operationFiles/count.txt', 'r')
count = countFile.readline(1)
countFile.close()

filename = './jsonDownloads/'+count+'_urls.json'

wget.download(
    'https://urlhaus-api.abuse.ch/v1/urls/recent/', filename)

urlJson = pd.read_json(filename)
urlList = pd.json_normalize(urlJson["urls"])

urlList = urlList[["url", "date_added"]]
urlList["date_added"] = urlList["date_added"].str.replace(" UTC", "")

current_datetime = datetime.now(timezone.utc).strftime("%Y-%m-%d %X")
current_datetime = datetime.strptime(current_datetime, "%Y-%m-%d %X")

freshUrlList = recentURLCheck(urlList, current_datetime)
freshUrlList = pd.DataFrame(freshUrlList, columns=["url"])
freshUrlList.to_csv("./operationFiles/urlList.csv", index=False, header=False)

count = int(count)
os.system(f"./httpx-operation.sh {count}")
count = count+1
count = str(count)

countFile = open('./operationFiles/count.txt', 'w')
countFile.write(count)
countFile.close()

#!/bin/bash

YELLOW="\e[33m"
ENDCOLOR="\e[0m"

echo -e "\n\n${YELLOW}Running HTTPx on all the URLs.${ENDCOLOR}"
httpx -l operationFiles/urlList.csv -mc 200 -nfs -maxhr 0 -retries 1 -o results/$1_resultURLs.csv
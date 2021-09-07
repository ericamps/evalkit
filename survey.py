### This gets who has submitted by course
import requests
import pandas as pd


container = pd.DataFrame()
#Discover API url filtered to movies >= 2004 and containing Drama genre_ID: 18
url = "https://alliant.evaluationkit.com/api/projects/125330/courses"

payload={}
headers = {'AuthToken': 'e35e4e8f467d2654473120dc7d0cc10d642e0328a0ebacbb9aacc85bc2e9e395', }


courselist_api = requests.request("GET", url, headers=headers, data=payload).json()

courses =  courselist_api["resultList"]
for course in courses:
    VAR_COURSEID  = course['id']
    VAR_RESPONDERS = url + '/' + str(VAR_COURSEID)
    #courselist_api = requests.request("GET", courses_url + VAR_COURSEID, headers=headers, data=payload).json()
    responders_api = requests.request("GET", VAR_RESPONDERS + '/respondents', headers=headers, data=payload).json()
    answers_api = requests.request("GET", VAR_RESPONDERS + '/rawData', headers=headers, data=payload).json()

    responders = pd.json_normalize(responders_api["resultList"])
    answers = pd.json_normalize(answers_api["resultList"])
    #print(responders)
    try:
        eric = pd.merge(responders,answers, how='left', left_on='submitDateTime', right_on='submitDate')
        container = container.append(eric, ignore_index=True)
    except:
        continue

container = container.replace(to_replace = 2.0, value = 'N')
container = container.replace(to_replace = 1.0, value = 'Y')
container.to_csv(r'survey_data.csv' , index = False, header = True, columns=['courseUniqueId_x', 'firstName', 'lastName', 'email', 'textAnswer', 'numericAnswer'])
#print(container)

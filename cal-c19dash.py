# cal-c19dash.py

import requests
import json
from datetime import datetime, timedelta

class Record():
    def __init__(self,totalcountconfirmed,totalcountdeaths,newcountconfirmed,newcountdeaths,date):
        self.totalcountconfirmed = int(float(totalcountconfirmed))
        self.totalcountdeaths = int(float(totalcountdeaths))
        self.newcountconfirmed = int(float(newcountconfirmed))
        self.newcountdeaths = int(float(newcountdeaths))
        self.date = date
    
    def __repr__(self):
        if self.newcountconfirmed == 0:
            message = f'{self.date.date()} saw {self.newcountconfirmed} new cases and remained at {self.totalcountconfirmed}. '
        elif self.newcountconfirmed == 1:
            message = f'{self.date.date()} saw {self.newcountconfirmed} new case for a total of {self.totalcountconfirmed}. '
        else:
            message = f'{self.date.date()} saw {self.newcountconfirmed} new cases for a total of {self.totalcountconfirmed}. '
        if self.newcountdeaths == 0:
            message += f'Total deaths remained at {self.totalcountdeaths}.'
        elif self.newcountdeaths == 1:
            message += f'There was {self.newcountdeaths} new death for a total of {self.totalcountdeaths}.'
        else:
            message += f'There were {self.newcountdeaths} new deaths for a total of {self.totalcountdeaths}.'
        return message
    

class County():
    def __init__(self, name):
        self.name = name
        self.data = self.getCounty(name)

    def __repr__(self):
        return self.name

    def getCounty(self, name):
        url = f'https://data.ca.gov/api/3/action/datastore_search_sql?sql=SELECT * from "926fd08f-cc91-4828-af38-bd45de97f8c3" WHERE "county" LIKE \'{name}\''
        data = requests.get(url)
        data = json.loads(data.text)
        countyData = {}
        for day in data['result']['records']:
            datadate = datetime.fromisoformat(day['date'])
            countyData[datadate.strftime('%Y-%m-%d')] = Record(totalcountconfirmed=day['totalcountconfirmed'], totalcountdeaths=day['totalcountdeaths'], newcountconfirmed=day['newcountconfirmed'], newcountdeaths=day['newcountdeaths'], date=datadate)
        return countyData


def getRecent(county, lookback=None):
    if lookback:
        lastWeek = datetime.now() - timedelta(days=lookback+1)
        for day in county:
            if county[day].date > lastWeek:
                print(county[day])
    else:
        for day in county:
            print(county[day])


if __name__ == "__main__":
    print('Data source: California Department of Public Health')
    countyName = input('Which county do you want to look up?\n')
    days = input('How far back do you want to look? Leave blank to show all available data.\n')
    if days:
        days = int(days)
    else:
        days = None
    covid = County(countyName.title())
    getRecent(covid.data, days)
    

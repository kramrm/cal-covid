# calc19dash.py

import requests
import json
from datetime import datetime, timedelta

class Record():
    def __init__(self,date):
        self.date = date

    def __repr__(self):
        return f'{self.date}'
    
    def short_desc(self):
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
    
    def long_desc(self):
        message = f'{self.date.date()}\n'
        for k in self.__dict__.keys():
            if k not in ('date', '_id'):
                message += f' - {k}: {self.__dict__.get(k)}\n'
        return message


class County():
    def __init__(self, name):
        self.name = name
        self.data = self.getCounty(name)

    def __repr__(self):
        days = [k for k in self.data.keys()]
        return f'{self.name} has {self.data[max(days)].totalcountconfirmed} total confirmed cases'
    
    def lastDay(self):
        days = [k for k in self.data.keys()]
        return f'{max(days)}'
    
    def getCounty(self, name):
        """Pull data from California Department of Public Health API.

        Args:
            name (string): County name to lookup

        Returns:
            dict
        """
        cases = f'https://data.ca.gov/api/3/action/datastore_search_sql?sql=SELECT * from "926fd08f-cc91-4828-af38-bd45de97f8c3" WHERE "county" LIKE \'{name.title()}\''
        hospital = f'https://data.ca.gov/api/3/action/datastore_search_sql?sql=SELECT * from "42d33765-20fd-44b8-a978-b083b7542225" WHERE "county" LIKE \'{name.title()}\''
        data = requests.get(cases)
        data = json.loads(data.text)
        hData = requests.get(hospital)
        hData = json.loads(hData.text)
        countyData = {}
        for day in data['result']['records']:
            datadate = datetime.fromisoformat(day['date'])
            shortDate = datadate.strftime('%Y-%m-%d')
            countyData[shortDate] = Record(date=datadate)
            for k in day.keys():
                try:
                    setattr(countyData[shortDate], k, int(float(day[k])))
                except:
                    pass
        for day in hData['result']['records']:
            if day.get('todays_date'):
                datadate = datetime.fromisoformat(day['todays_date'])
                shortDate = datadate.strftime('%Y-%m-%d')
                for k in day.keys():
                    try:
                        setattr(countyData[shortDate], k, int(float(day[k])))
                    except:
                        pass
        return countyData


def getRecent(county, lookback=None):
    """Display recent COVID-19 data

    Args:
        county (County.data): County object with the raw data.
        lookback (int, optional): Number of past days to display. Defaults to all data.
    """
    if lookback:
        lastWeek = datetime.now() - timedelta(days=lookback+1)
        for day in sorted(county):
            if county[day].date > lastWeek:
                print(county[day].short_desc())
    else:
        for day in sorted(county):
            print(county[day].short_desc())


if __name__ == "__main__":
    print('Data source: California Department of Public Health')
    countyName = input('Which county do you want to look up?\n')
    if countyName is not '':
        days = input('How far back do you want to look? Leave blank to show the most recent day.\n')
        covid = County(countyName)
        if days:
            days = int(days)
            getRecent(covid.data, days)
        else:
            print(covid.data[covid.lastDay()].long_desc())
        # getRecent(covid.data, days)
        

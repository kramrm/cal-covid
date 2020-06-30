# cal-c19dash.py

import requests
import json
from datetime import datetime, timedelta

class Record():
    def __init__(self,date,totalcountconfirmed=None,totalcountdeaths=None,newcountconfirmed=None,newcountdeaths=None,
        icu_covid_confirmed_patients=None, icu_suspected_covid_patients=None, hospitalized_covid_patients=None,
        hospitalized_suspected_covid_patients=None, icu_available_beds=None, previous_days_conversion_covid_patients=None,
        previous_days_covid_confirmed_patients=None, hospitalized_covid_confirmed_patients=None, all_hospital_beds=None,
        previous_days_suspected_covid_patients=None):
        self.date = date
        if totalcountconfirmed:
            self.totalcountconfirmed = int(float(totalcountconfirmed))
        if totalcountdeaths:
            self.totalcountdeaths = int(float(totalcountdeaths))
        if newcountconfirmed:
            self.newcountconfirmed = int(float(newcountconfirmed))
        if newcountdeaths:
            self.newcountdeaths = int(float(newcountdeaths))
        if icu_covid_confirmed_patients:
            self.icu_covid_confirmed_patients = int(float(icu_covid_confirmed_patients))
        if icu_suspected_covid_patients:
            self.icu_suspected_covid_patients = int(float(icu_suspected_covid_patients))
        if hospitalized_covid_patients:
            self.hospitalized_covid_patients = int(float(hospitalized_covid_patients))
        if hospitalized_suspected_covid_patients:
            self.hospitalized_suspected_covid_patients = int(float(hospitalized_suspected_covid_patients))
        if icu_available_beds:
            self.icu_available_beds = int(float(icu_available_beds))
        if previous_days_conversion_covid_patients:
            self.previous_days_conversion_covid_patients = int(float(previous_days_conversion_covid_patients))
        if previous_days_covid_confirmed_patients:
            self.previous_days_covid_confirmed_patients = int(float(previous_days_covid_confirmed_patients))
        if hospitalized_covid_confirmed_patients:
            self.hospitalized_covid_confirmed_patients = int(float(hospitalized_covid_confirmed_patients))
        if all_hospital_beds:
            self.all_hospital_beds = int(float(all_hospital_beds))
        if previous_days_suspected_covid_patients:
            self.previous_days_suspected_covid_patients = int(float(previous_days_suspected_covid_patients))

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
        days = [k for k in self.data.keys()]
        return f'{self.name} has {self.data[max(days)].totalcountconfirmed} total confirmed cases'
    
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
            countyData[shortDate].totalcountconfirmed = day['totalcountconfirmed']
            countyData[shortDate].totalcountdeaths = day['totalcountdeaths']
            countyData[shortDate].newcountconfirmed = day['newcountconfirmed']
            countyData[shortDate].newcountdeaths = day['newcountdeaths']
        for day in hData['result']['records']:
            if day.get('todays_date'):
                datadate = datetime.fromisoformat(day['todays_date'])
                shortDate = datadate.strftime('%Y-%m-%d')
                countyData[shortDate].icu_covid_confirmed_patients = day['icu_covid_confirmed_patients']
                countyData[shortDate].icu_suspected_covid_patients = day['icu_suspected_covid_patients']
                countyData[shortDate].hospitalized_covid_patients = day['hospitalized_covid_patients']
                countyData[shortDate].hospitalized_suspected_covid_patients = day['hospitalized_suspected_covid_patients']
                countyData[shortDate].icu_available_beds = day['icu_available_beds']
                countyData[shortDate].previous_days_conversion_covid_patients = day['previous_days_conversion_covid_patients']
                countyData[shortDate].previous_days_covid_confirmed_patients = day['previous_days_covid_confirmed_patients']
                countyData[shortDate].hospitalized_covid_confirmed_patients = day['hospitalized_covid_confirmed_patients']
                countyData[shortDate].all_hospital_beds = day['all_hospital_beds']
                countyData[shortDate].previous_days_suspected_covid_patients = day['previous_days_suspected_covid_patients']
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
                print(county[day])
    else:
        for day in sorted(county):
            print(county[day])


if __name__ == "__main__":
    print('Data source: California Department of Public Health')
    countyName = input('Which county do you want to look up?\n')
    if countyName is not '':
        days = input('How far back do you want to look? Leave blank to show all available data.\n')
        if days:
            days = int(days)
        else:
            days = None
        covid = County(countyName)
        getRecent(covid.data, days)

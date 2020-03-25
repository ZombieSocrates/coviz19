import ipdb
import pandas as pd
import pathlib
import requests

from pprint import pprint


COVID_BASE = "https://covidtracking.com/api"
COVID_STATES = f"{COVID_BASE}/states"
COVID_STATES_DAILY = f"{COVID_STATES}/daily"
COVID_COUNTIES = f"{COVID_BASE}/counties"


def current_tests_by_state():
    '''Returns a list of 56 US territories that report current testing 
    frequencies and totals. Example of what a returned object looks like:

        {'checkTimeEt': '3/24 22:29',
         'commercialScore': 1,
         'dateChecked': '2020-03-25T02:29:00Z',
         'dateModified': '2020-03-25T01:00:00Z',
         'death': 1,
         'grade': 'A',
         'hospitalized': 1,
         'lastUpdateEt': '3/24 21:00',
         'negative': 1691,
         'negativeRegularScore': 1,
         'negativeScore': 1,
         'pending': None,
         'positive': 42,
         'positiveScore': 1,
         'score': 4,
         'state': 'AK',
         'total': 1733}
    '''
    rsp = requests.get(COVID_STATES)
    if rsp.status_code != 200:
        print(f"Errored with code {rsp.status_code}")
        return
    json_data = rsp.json()
    return pd.DataFrame(data = [r for r in json_data]) 


if __name__ == "__main__":
    state_covid_df = current_tests_by_state()
    ipdb.set_trace()

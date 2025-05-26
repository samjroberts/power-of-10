import requests
from bs4 import BeautifulSoup
from .exceptions import BroadQueryError, QueryError


def get_results(club_num=None):
    '''
    Returns a list of athletes with the inputted firstname, surname or club.

            Parameters:
                    - 'firstname' (str): Optional first name agrument
                    - 'surname' (str): Optional surname argument
                    - 'club' (str): Optional club agrument

            Returns:
                    - 'list_of_athletes' (arr): List of athlete data in dict
                        - 'firstname' (str): First name of athlete
                        - 'surname' (str): Surname of athlete
                        - 'track' (str): Age group for athlete on track 
                        - 'road' (str): Age group for athlete on road
                        - 'sex' (str): Gender of athlete
                        - 'club' (str): Athletics club of althete
                        - 'athlete_id' (int): Reference id of athlete (used by PowerOf10)
    '''
    url = f'https://www.parkrun.com/results/consolidatedclub/?'
    if club_num is not None:
        url += f'clubNum={club_num.replace(" ","+")}'

    if club_num is None:
        raise QueryError('Please input a club number')
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    }
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    results = soup.find_all('a')
    #results-1 > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)
    

    list_of_athlete_links = []
    for r in results:
        list_of_athlete_links.append(r.get_text())

    if list_of_athlete_links == []:
        raise QueryError('No athletes found. Use broader search terms or amend your queries.')

    print(list_of_athlete_links)
    return list_of_athlete_links
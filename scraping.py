from bs4 import BeautifulSoup
import requests
import mysql.connector
from get_URL import get_url
from get_players_list import get_players
from update_database import populate_tables

def get_table_data(url):
    # GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html html content
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.prettify()) # print the parsed data of html

    the_table = soup.find("table")


    t_headers = []
    for th in the_table.find_all("th"):
        # remove any newlines and extra spaces from left and right
        t_headers.append(th.text.replace('\n', ' ').strip())

    #print(t_headers)
    dates = t_headers[47:]
    t_headers = t_headers[10:45]


    table_data = [] # list of dicts
    for tr, date in zip(the_table.tbody.find_all("tr"), dates): # iterate through all rows
        t_row = {}
        # t_row = {Date: '', Day: '', etc}
        t_row["Date"] = date
        for td, th in zip(tr.find_all("td"), t_headers):
            t_row[th] = td.text.replace('\n', '').strip()

        table_data.append(t_row)

    # Filter to only keep premier league games
    clean_table = [i for i in table_data if i["Comp"] == "Premier League"]

    return clean_table




premier_league_player_names = get_players()
seasons = ["2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020"]


for name in premier_league_player_names:
    for season in seasons:
        url = get_url(name, season)

        try:
            table_data = get_table_data(url)
            print(table_data[0])
        except:
            # Webpage probably doesn't exist
            continue


        populate_tables(name, season, table_data)

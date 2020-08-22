from bs4 import BeautifulSoup
import requests
import mysql.connector

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

    return table_data


def write_to_DB(table_data, table_name):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "abc314",
        database = "fantasyfootball"
    )

    mycursor = mydb.cursor()

    # Only create table if it doesn't already exist
    mycursor.execute("SHOW TABLES")
    results = mycursor.fetchall()
    results_list = [item[0] for item in results]

    if table_name not in results_list:
        # Create table
        mycursor.execute("CREATE TABLE "+table_name)



url = "https://fbref.com/en/players/e06683ca/matchlogs/2019-2020/summary/Virgil-van-Dijk-Match-Logs"
url_parts = url.split("/")
season = url_parts[-3]
season = season.replace('-', '')
name_logs = url_parts[-1]
name = name_logs[:-11]
name = name.replace('-','')
table_name = name+season


table_data = get_table_data(url)
write_to_DB(table_data, table_name)

from bs4 import BeautifulSoup
import requests
import mysql.connector

def get_table_data(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    the_table = soup.find("table")

    t_headers = []
    for th in the_table.find_all("th"):
        t_headers.append(th.text.replace('\n', ' ').strip())

    dates = t_headers[47:]
    t_headers = t_headers[10:45]
    table_data = [] # list of dicts

    for tr, date in zip(the_table.tbody.find_all("tr"), dates): # iterate through all rows
        t_row = {}
        t_row["Date"] = date
        for td, th in zip(tr.find_all("td"), t_headers):
            t_row[th] = td.text.replace('\n', '').strip()
        table_data.append(t_row)

    return table_data

def create_tables():
    mydb = mysql.connector.connect(host='localhost',database='mysql',user='root',password="499587li")
    mycursor = mydb.cursor()

    mycursor.execute("DROP DATABASE FPL")
    mycursor.execute("CREATE DATABASE FPL")
    mycursor.execute("USE FPL")
    mycursor.execute("CREATE TABLE Playerid (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), team VARCHAR(255))")
    #mycursor.execute("CREATE TABLE MATCHID (name VARCHAR(255), address VARCHAR(255))")
    #mycursor.execute("CREATE TABLE PLAYERMATCHID (name VARCHAR(255), address VARCHAR(255))")

create_tables()

"""
url = "https://fbref.com/en/players/e06683ca/matchlogs/2019-2020/summary/Virgil-van-Dijk-Match-Logs"
table_data = get_table_data(url)

clean_table = [i for i in table_data if i["Comp"] == "Premier League"]

print(clean_table[0].keys())

print()
"""
#mydb = mysql.connector.connect(host='localhost',database='mysql',user='root',password="499587li")
#mycursor = mydb.cursor()

#mycursor.execute("USE test")
#mycursor.execute("INSERT INTO Players VALUES (1, 'Carl', 'Adian', 4, 3)")
#mydb.commit()

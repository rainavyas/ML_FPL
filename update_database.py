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

    mycursor.execute("CREATE TABLE Players (Player_id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255) NOT NULL, Team VARCHAR(255), Position VARCHAR(255))")
    mycursor.execute("CREATE TABLE Matches (Match_id INT AUTO_INCREMENT PRIMARY KEY, Season VARCHAR(255) NOT NULL, Round VARCHAR(255), Date DATE, Team VARCHAR(255) NOT NULL, Opponent VARCHAR(255) NOT NULL, Venue VARCHAR(255) NOT NULL, Result VARCHAR(255) NOT NULL)")
    mycursor.execute("CREATE TABLE Playermatches (Playermatch_id VARCHAR(255) PRIMARY KEY, Player_id INT NOT NULL, Match_id INT NOT NULL, Start VARCHAR(255), Min INT, Gls INT, Ast INT, PK INT, PKA INT, Sh INT, SoT INT, CrdY INT, CrdR INT, Tch INT, Prs INT, Tkl INT, Intr INT, Blc INT, xG FLOAT, npxG FLOAT, xA Float, SCA INT, GCA INT, cmp INT, Attp INT, PrgD INT, SuccD INT, AttD INT, FOREIGN KEY(Player_id) REFERENCES Players(Player_id), FOREIGN KEY(Match_id) REFERENCES Matches(Match_id))")

def populate_tables(Name, Season, season_table):
    mydb = mysql.connector.connect(host='localhost',database='FPL',user='root',password="499587li")
    mycursor = mydb.cursor()

    Team = season_table[0]['Squad']
    mycursor.execute(f"SELECT player_id FROM Players WHERE Name = '{Name}' AND Team = '{Team}'")
    player_id = mycursor.fetchone()

    if player_id == None:
        print('here')
        mycursor.execute(f"INSERT INTO Players (Name, Team, Position) VALUES ('{Name}', '{Team}', '{season_table[-1]['Pos']}')")
        mycursor.execute(f"SELECT player_id FROM Players WHERE Name = '{Name}' AND Team = '{Team}'")
        player_id = mycursor.fetchone()[0]

    for g in season_table:
        mycursor.execute(f"SELECT match_id FROM Matches WHERE Date = '{g['Date']}' AND Team = '{g['Squad']}'")
        match_id = mycursor.fetchone()
        if match_id == None:
            mycursor.execute(f"INSERT INTO Matches (Season, Round, Date, Team, Opponent, Venue, Result) VALUES ('{Season}', '{g['Round']}', '{g['Date']}', '{g['Squad']}' , '{g['Opponent']}', '{g['Venue']}', '{g['Result']}')")
            mycursor.execute(f"SELECT match_id FROM Matches WHERE Date = '{g['Date']}' AND Team = '{g['Squad']}'")
            match_id = mycursor.fetchone()[0]

        mycursor.execute(f"INSERT INTO Playermatches (Playermatch_id, Player_id, Match_id, Start, Min, Gls, Ast, PK, PKA, Sh, SoT, CrdY, CrdR, Tch, Prs, Tkl, Intr, Blc, xG, npxG, xA, SCA, GCA, cmp, Attp, PrgD, SuccD, AttD) VALUES ('{str(player_id)+'-'+str(match_id)}', '{player_id}', '{match_id}', '{g['Start']}', '{g['Min']}', '{g['Gls']}', '{g['Ast']}', '{g['PK']}', '{g['PKatt']}', '{g['Sh']}', '{g['SoT']}', '{g['CrdY']}', '{g['CrdR']}', '{g['Touches']}', '{g['Press']}', '{g['Tkl']}', '{g['Int']}', '{g['Blocks']}', '{g['xG']}', '{g['npxG']}', '{g['xA']}', '{g['SCA']}', '{g['GCA']}', '{g['Cmp']}', '{g['Att']}', '{g['PrgDist']}', '{g['Carries']}', '{g['Succ']}')")

    mydb.commit()

    #mycursor.execute("INSERT INTO Players (Name, Team) ")
create_tables()

url = "https://fbref.com/en/players/e06683ca/matchlogs/2019-2020/summary/Virgil-van-Dijk-Match-Logs"
table_data = get_table_data(url)
clean_table = [i for i in table_data if i["Comp"] == "Premier League"]
populate_tables("Van Dijk", "2019-2020", clean_table)

#mydb = mysql.connector.connect(host='localhost',database='mysql',user='root',password="499587li")
#mycursor = mydb.cursor()

#mycursor.execute("USE test")
#mycursor.execute("INSERT INTO Players VALUES (1, 'Carl', 'Adian', 4, 3)")
#mydb.commit()

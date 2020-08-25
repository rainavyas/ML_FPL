from bs4 import BeautifulSoup
import requests


def get_players():
    url_base = "https://www.worldfootball.net/players_list/eng-premier-league-2019-2020/nach-name/"

    players = []
    for page_num in range(1,15):
        url = url_base + str(page_num)
        html_content = requests.get(url).text

        # Parse the html content
        soup = BeautifulSoup(html_content, "lxml")
        the_table = soup.find("table", {"class":"standard_tabelle"})

        rows = the_table.find_all("tr")
        # Read each row in turn
        for tr in rows[1:]:
            row_data = tr.find_all("td")
            name = row_data[0].text.replace('\n', '').strip()
            players.append(name)

        return players

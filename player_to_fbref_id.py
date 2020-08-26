'''
    Save each player and associated playerid on fbref.com
'''

from get_players_list import get_players
from get_URL import get_name_id

names = get_players()

f_name = "player_fbref_ids.txt"
f = open(f_name, 'w')
f.write("")
f.close()
f = open(f_name, 'a')

for name in names:
    try:
        fb_name, id = get_name_id(name)
    except:
        f.write(name + ": None")
        continue
    f.write(fb_name + ": " + str(id)+'\n')

f.close()

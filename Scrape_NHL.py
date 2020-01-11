from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from pandas import ExcelWriter
import settings
import regex as re


SLEEP_SECONDS = 3

login_url = "https://hockey.fantasysports.yahoo.com/hockey/18691/players"
driver = webdriver.Chrome(executable_path=r'C:\Users\benny\AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\chromedriver.exe')

# load page
driver.get(login_url)

# input username
username = driver.find_element_by_name('username')
username.send_keys(settings.YAHOO_USERNAME)
username.send_keys(Keys.ENTER)

# time out to wait for page to load
time.sleep(SLEEP_SECONDS)

#input password
password = driver.find_element_by_name('password')
password.send_keys(settings.YAHOO_PASSWORD)
password.send_keys(Keys.ENTER)

# load players stats page
url = 'https://hockey.fantasysports.yahoo.com/hockey/18691/players'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

#find table
table_body = soup.find('table', {'class':'Table Ta-start Fz-xs Table-mid Table-px-xs Table-interactive'})
# print(table_body)

#print a list of player names
table = table_body.find_all('a', class_="Nowrap")
player_name = [name.text for name in table]
# print(player_name)
# print(len(player_name))

#print a list of player's team and position
table = table_body.find_all('span', class_="Fz-xxs")
team_list = [team_pos.text for team_pos in table]
team_sorted = team_list[::2]
# print(team_sorted)
join_list = (' - '.join(team_sorted))
# print(join_list)
re_list = re.split("\s", join_list)
# print(re_list)
team_list = re_list[::4]
# print(team_list)
pos_list = re_list[2::4]
# print(pos_list)


##print a list of games played by each player
table = table_body.find_all('td')
table_stats = [gp.text for gp in table]
game_played = table_stats[5::21]
# print(game_played)
# print(len(game_played))

# sort table elements into appropriate lists
table = table_body.find_all('td', class_="Ta-end")
# print(table)
game_stats = [stats.text for stats in table]
LY_rank = game_stats[::13]
Cur_rank = game_stats[1::13]
owned = game_stats[3::13]
Goals = game_stats[4::13]
Assists = game_stats[5::13]
Points = game_stats[6::13]
PPP = game_stats[7::13]
SHP = game_stats[8::13]
GWG = game_stats[9::13]
SOG = game_stats[10::13]
HIT = game_stats[11::13]
BLK = game_stats[12::13]

# converts stats from string to int or float when applicable
game_played_int = [int(stats) for stats in game_played]
LY_rank_int = [int(stats) for stats in LY_rank]
Cur_rank_int = [int(stats) for stats in Cur_rank]
Goals_int = [int(stats) for stats in Goals]
Assists_int = [int(stats) for stats in Assists]
Points_int = [int(stats) for stats in Points]
PPP_int = [int(stats) for stats in PPP]
SHP_int = [int(stats) for stats in SHP]
GWG_int = [int(stats) for stats in GWG]
SOG_int = [int(stats) for stats in SOG]
HIT_int = [int(stats) for stats in HIT]
BLK_int = [int(stats) for stats in BLK]


#arrange lists into Pandas DataFrame
df = pd.DataFrame({
    'names':player_name,
    'team':team_list,
    'position':pos_list,
    'game played':game_played_int,
    'pre season Rank':LY_rank_int,
    'current rank':Cur_rank_int,
    'goals':Goals_int,
    'assists':Assists_int,
    'points':Points_int,
    'ppp':PPP_int,
    'shp':SHP_int,
    'gwg':GWG_int,
    'sog':SOG_int,
    'hits':HIT_int,
    'blocks':BLK_int,
})
# with pd.option_context('display.max_rows', None, 'display.max_columns', df.shape[1]):
#     print(df)
# df.to_clipboard()
# print(test_df.info())
# df = pd.read_csv
# df.head()
# df.shape
excel_file = r"C:\Users\benny\Desktop\fantasy.xlsx"
writer = ExcelWriter(excel_file)
df.to_excel(writer, index=False)
writer.save()

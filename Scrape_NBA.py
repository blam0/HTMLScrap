from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
import settings

SLEEP_SECONDS = 3

url = "https://login.yahoo.com/config/login?.src=spt&.intl=us&.done=https%3A%2F%2Fbasketball.fantasysports.yahoo.com%2Fnba%2F19362%2F5&specId=usernameRegWithName"
url2 = 'https://basketball.fantasysports.yahoo.com/nba/19362/players?status=ALL&pos=P&cut_type=33&stat1=S_AS_2019&myteam=0&sort=AR&sdir=1'
driver = webdriver.Chrome(executable_path=r'C:\Users\benny\AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\chromedriver.exe')

# load page
driver.get(url)

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
driver.get(url2)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# soup = BeautifulSoup(html, 'lxml')

# Retrieve all of the anchor tags
# tags = soup('a')
# for tag in tags:
#   print(tag.get('href', None))

# print(soup.prettify())
# print(soup.get_text())
#
# for string in soup.stripped_strings:
#     print(repr(string))
# print(soup.p)
#
# table = soup.find_all('td', class_="Alt Ta-end")
# table = soup.find_all(['td','sup'])
# table_header = soup.find('thead')
# table = table_header.find_all('a')
# column_title = [column_header.text for column_header in table]
# print(column_title)

table_body = soup.find('table', {'class':'Table Ta-start Fz-xs Table-mid Table-px-xs Table-interactive'})
# print(table_body)

table = table_body.find_all('a', class_="Nowrap")
player_name = [name.text for name in table]
print(player_name)

# for player_name in table_body.find_all('a', class_="Nowrap"):
#     print(player_name.text)

table = table_body.find_all('span', class_="Fz-xxs")
team_list = [team_pos.text for team_pos in table]
team_sorted = team_list[::2]
print(team_sorted)


table = table_body.find_all('td', class_="Ta-end")
game_stats = [stats.text for stats in table]
GP = game_stats[::19]
LY_rank = game_stats[1::19]
Cur_rank= game_stats[2::19]
owned = game_stats[3::19]
MPG= game_stats[4::19]
FGM = game_stats[5::19]
FGA = game_stats[6::19]
FG_percent = game_stats[7::19]
FTM = game_stats[8::19]
Three_PTM = game_stats[9::19]
Three_PTA = game_stats[10::19]
Three_percent = game_stats[11::19]
PPG = game_stats[12::19]
REB = game_stats[13::19]
AST = game_stats[14::19]
ST = game_stats[15::19]
BLK = game_stats[16::19]
TO = game_stats[17::19]
PF = game_stats[18::19]

# converts stats from string to float when applicable
GP_float = [int(stats) for stats in GP]
LY_rank_float = [float(stats) for stats in LY_rank]
Cur_rank_float = [float(stats) for stats in Cur_rank]
FGM_float = [float(stats) for stats in FGM]
FTM_float = [float(stats) for stats in FTM]
Three_PTM_float = [float(stats) for stats in Three_PTM]
PPG_float = [float(stats) for stats in PPG]
REB_float = [float(stats) for stats in REB]
AST_float = [float(stats) for stats in AST]
ST_float = [float(stats) for stats in ST]
BLK_float = [float(stats) for stats in BLK]
TO_float = [float(stats) for stats in TO]
PF_float = [float(stats) for stats in PF]



test_df = pd.DataFrame({
    'names': player_name,
    'team':team_sorted,
    'game played':GP_float,
    'minutes/game':MPG,
    'field goals made':FGM_float,
    'field goal %': FG_percent,
    'free throw made':FTM_float,
    '3pt made':Three_PTM_float,
    '3pt %':Three_percent,
    'points/gm':PPG_float,
    'rebounds/gm':REB_float,
    'assist/gm':AST_float,
    'steals/gm':ST_float,
    'blocks/gm':BLK_float,
    'turnovers/gm':TO_float,
    'personal fouls':PF_float
})
with pd.option_context('display.max_rows', None, 'display.max_columns', test_df.shape[1]):
    print(test_df)
# print(test_df.info())
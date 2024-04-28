import requests
import csv
import os
import time
import random
from bs4 import BeautifulSoup

# TODO:
# - docstrings
# - parameters
# - encapsulation
# - unit tests
# - external color dict
# - random pooling timer
# - variable renaming

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def scrape_table_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table')
    
    data_dict = {}
    for index, tr in enumerate(table.find_all('tr')):
        row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
        data_dict[index] = row_data
    
    return data_dict
players = []
with open('./texts/viplist.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', )
    for row in csvreader:
        player_tuple = (row[0],row[1])
        players.append(player_tuple)
        #print(player_tuple)

def show_data(data):
    os.system('cls')
    print("---------------EXPANDED VIP---------------")
    for key, value in data.items():
        try:
            for player, type in players:
                if player.lower().strip() == value[1].lower().split("(")[0]:
                    if type == "enemy":
                        color = bcolors.WARNING
                    elif type == "friend":
                        color = bcolors.OKGREEN
                    else:
                        color = bcolors.OKCYAN
                    print(f"{color}{player}{bcolors.ENDC}")
        except IndexError:
            pass

url = 'https://tibiantis.info/stats/online'
while True:
    data = scrape_table_data(url)
    show_data(data)
    time.sleep(5*60+int(random.random()*50))


# imports
import requests
import csv
import os
import re
import time
import sqlite3
from bs4 import BeautifulSoup
from google.cloud import bigquery

# get online player list
def scrape_table_data():
    url = 'https://tibiantis.info/stats/online'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table')
    
    data_dict = {}
    for index, tr in enumerate(table.find_all('tr')):
        row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
        data_dict[index] = row_data
    return data_dict

# get player login timestamps
def scrape_player_logns(data):
    url = 'https://tibiantis.info/stats/player/'
    for key, value in data.items():
        try:
            player = value[1].lower().split("(")[0]
            print("PLAYER NAME: ",player)
            player_url = url + player.replace(" ", "%20")
            response = requests.get(player_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table')

            data_dict = {}
            flag_record = False
            flag_message = 'Last 20 login and logout dates'
            print("LOGIN TIMESTAMPS")
            for index, tr in enumerate(table.find_all('tr')):
                #header_data = [th.get_text(strip=True) for th in tr.find_all('th')]
                if flag_message in tr.text:
                    flag_record = True
                row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
                if flag_record and len(row_data)>0 and "still online" not in row_data:
                    data_dict[index] = row_data
                    print("RECORD: ",row_data)
                    record_data(player, row_data)
        except IndexError:
            pass

def show_data(data):
    os.system('cls')
    for key, value in data.items():
        try:
            print(value[1].lower().split("(")[0].replace(" ", "%20"))
        except IndexError:
            pass

# create database
def create_database():
    conn = sqlite3.connect('tibiantis.db')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS logins (
        name TEXT,
        login TEXT,
        logout TEXT,
        duration TEXT,
        level INTEGER,
        UNIQUE(name,login,logout,duration,level)
        )
    """)
    conn.commit()
    conn.close()

# record data
def record_data(player, row_data):
    name = player
    login = row_data[0]
    logout = row_data[1]
    duration = row_data[2]
    level = row_data[3]

    pattern = r'[^a-zA-Z0-9 ]'
    pre_statement = f'"{re.sub(pattern, "", name)}","{login}","{logout}","{duration}","{level}"'
    print(pre_statement)
    try:
        conn = sqlite3.connect('tibiantis.db')
        c = conn.cursor()
        c.execute(f"""
        INSERT OR IGNORE INTO logins (name,login,logout,duration,level)
        VALUES({pre_statement})
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)

def export_to_csv():
    os.system('sqlite3 -header -csv tibiantis.db "select * from logins" > ./texts/logins.csv')
    print('File exported.')

def upload_to_bigquery():
    project_id = 'noob-utility-tools'
    dataset = 'tibiantisinfo'
    table = 'logins'
    table_id = f'{project_id}.{dataset}.{table}'

    sa_path = './configs/noob-utility-tools-1c2633471287.json'
    client = bigquery.Client().from_service_account_json(sa_path)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  
        source_format=bigquery.SourceFormat.CSV,  
        field_delimiter=",",  
        skip_leading_rows=1
    )

    with open('./texts/logins.csv', 'rb') as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()
    print('Database uploaded.')

# loop
while True:
    create_database()
    data = scrape_table_data()
    scrape_player_logns(data)
    export_to_csv()
    upload_to_bigquery()
    time.sleep(600)
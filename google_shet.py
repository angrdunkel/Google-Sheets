from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

import requests
from time import sleep
import psycopg2

import numpy
import datetime

import xml.etree.ElementTree as ET
#Читаем данные из google sheets
def read_sheet(service):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:D99999',
        majorDimension='ROWS'
    ).execute()
    return values

#Получаем данные курса USD
def get_rub(val):
    res = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    tree = ET.fromstring(res.content) 
    for i in tree:
        if i[1].text == 'USD':
            print(i[4].text)
            result = i[4].text
    result = str(result).split(',')
    
    return float(f'{result[0]}.{result[1]}') * float(val)


#Подключаемся к google sheets и google drive API
CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1jUnWXmaUVli-QnTcfVWJjbKBjuIZtcKAfQKcIQs2iSA'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
service2 = apiclient.discovery.build('drive', 'v3', http = httpAuth)
response = service2.changes().getStartPageToken().execute()
page_token = response.get('startPageToken')

#Обновление БД
def update_datebase(service):
    dbname = 'Your_db_name'
    user = 'Your_db_user'
    password = 'Your_db_password'

    sheet_datas = read_sheet(service)
    conn = psycopg2.connect(dbname=dbname, user=user, 
                        password=password, host='localhost')
    cursor = conn.cursor()
    cursor.execute('TRUNCATE public.table RESTART IDENTITY;')
    conn.commit()
    

    cursor = conn.cursor()
    for x, row in enumerate(sheet_datas['values']):
        print(f'{x} - {row}')        
        rub = get_rub(row[2])
        cursor.execute(f"INSERT INTO public.table (num, orders, price, rub, d_time) VALUES ({row[0]}, {int(row[1])}, {row[2]}, {rub}, TIMESTAMP '2011-05-16');")
        conn.commit()
    conn.close()

#Проверка изменений в документе, если есть тогда делаем обновления в базе
while True:
    response = service2.changes().list(pageToken=page_token,
                                            spaces='drive').execute()
    
    if response.get('changes') != []:
        for change in response.get('changes'):
            print(response.get('changes'))
            print('Change found for file: %s' % change.get('fileId'))
            print(change.get('file')['name'])
            if 'newStartPageToken' in response:   
                saved_start_page_token = response.get('newStartPageToken')
            next_page_token = response.get('newStartPageToken')
            print('Next ', next_page_token)
            if next_page_token != page_token:
                page_token = next_page_token
                update_datebase(service)
                print('Done')
                sleep(50)
   
    sleep(20)      






import os
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from google.oauth2.service_account import Credentials


def run():
    # 設定憑證檔案路徑和試算表名稱
    credential_file = os.path.abspath('src/credentials.json')
    print(f'{credential_file}')

    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # 取得憑證物件
    creds = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
    # creds = ServiceAccountCredentials.from_json_keyfile_name(credential_file)

    # 建立 Google Sheets API 的客戶端物件
    client = gspread.authorize(creds)
    
    for spreadsheet in client.list_spreadsheet_files():
        print(f'{spreadsheet}')

    # 開啟試算表
    spreadsheet_name = 'binance-data'
    spreadsheet = client.open(spreadsheet_name)

    # spreadsheet_id = '12OpPTryLqm4T_cAU8of-D6A0dtCsg6xEgAVDsQ_GxEI'
    # spreadsheet = client.open_by_key(spreadsheet_id)

    worksheet = spreadsheet.worksheet('sheet1')
    
    # 讀取資料
    data = worksheet.get_all_records()
    print(f'data:{data}')

    # 寫入資料到另一個試算表
    # new_sheet = client.create('My New Sheet')
    # worksheet = new_sheet.add_worksheet('sheet2')

    worksheet.append_row(values=['2021-01-04', 'BNBUSDT', '99'])

    # 以下是一個讀寫 Google Sheets 的 Python 範例，使用的是 Google Sheets API 和 gspread 套件。這個範例可以讀取一個 Google Sheets 試算表中的資料，並將資料寫入到另一個試算表中。你可以根據自己的需求修改程式碼。

    # 你需要先在 Google Cloud Platform 上建立一個專案，並啟用 Google Sheets API。接著，你需要建立一個服務帳戶，並下載憑證 JSON 檔案。最後，你需要安裝 gspread 套件，並使用上述程式碼來讀寫 Google Sheets 試算表。
    # (1) Python 讀寫 Google Sheets 教學 - HackMD. https://hackmd.io/@Yun-Cheng/GoogleSheets.
    # (2) [Pandas教學]一定要學會的Pandas套件讀寫Google Sheets試算表資料秘訣 - Learn Code With Mike. https://www.learncodewithmike.com/2021/06/pandas-and-google-sheets.html.
    # (3) [Python爬蟲教學]解析如何串接Google Sheet試算表寫入爬取的資料 - Learn Code With Mike. https://www.learncodewithmike.com/2020/08/python-write-to-google-sheet.html.

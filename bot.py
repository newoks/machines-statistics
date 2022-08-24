import sqlite3
import xlsxwriter
from datetime import datetime

from source_data import pool_names, tz_irk, BOT, TELEGRAM_ID_VLAD
from matplot_table import create_table
from xlsx_create import create_worksheet

con = sqlite3.connect('example.db')
cur = con.cursor()
sql_select_last_4 = '''SELECT * FROM hashrate WHERE id > (SELECT MAX(id) FROM hashrate) - 4'''


def send_all_statistics():
    cur.execute(sql_select_last_4)
    last_4_db = cur.fetchall()
    create_table(last_4_db)
    img = open('stat.png', 'rb')
    BOT.send_photo(TELEGRAM_ID_VLAD, img)


def send_xlsx_statistics():
    date_ = datetime.now(tz_irk).strftime("%d.%m.%Y")
    time_ = datetime.now(tz_irk).strftime("%H:%M")
    workbook = xlsxwriter.Workbook(f'statistics.xlsx')

    for sheet in pool_names:
        cur.execute(
            f'SELECT time_, hs_avg, online_machines, difference FROM {sheet} WHERE id > (SELECT MAX(id) FROM {sheet}) - 4')
        last_4_db = cur.fetchall()
        create_worksheet(workbook, sheet, last_4_db)

    workbook.close()
    document = open("./Statistics.xlsx", "rb")
    caption = f'{date_} {time_}'
    BOT.send_document(TELEGRAM_ID_VLAD, document, caption=caption)
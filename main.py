from tqdm import tqdm
from datetime import datetime
import time
import sqlite3

from scripts import data_antpool, avg_hs, data_f2pool, data_binance
from source_data import source_data, URL_MACHINES, URL_HS, URL_F2POOL, URL_BINANCE, switch_user_id, tz_irk, source_total_machines
from bot import send_all_statistics, send_xlsx_statistics

con = sqlite3.connect('example.db')
cur = con.cursor()

sql_insert = '''INSERT INTO hashrate (hs_avg, online_machines, offline_machines, total_machines, date_, time_) VALUES (?, ?, ?, ?, ?, ?)'''
count_for = 0

# while True:
#     if count_for < 4:
#         print(f'start {count_for}')
#         list_hs = []
#         total_online = 0
#         error_log = None
#         try:
#             for user_id, access_key_and_count in tqdm(source_data.items()):
#                 access_key, count = access_key_and_count
#                 date_ = datetime.now(tz_irk).strftime("%d.%m.%Y")
#                 time_ = datetime.now(tz_irk).strftime("%H:%M")
#
#                 if user_id in switch_user_id.keys():
#                     name = switch_user_id[user_id]
#
#                 if user_id.find('m20s') != -1 or user_id == 'hulucas001':
#                     total_online_machines, hs_now, total_machines = data_antpool(URL_HS, URL_MACHINES, access_key, user_id)
#                     list_hs.append(float(hs_now))
#                     total_online += total_online_machines
#                     cur.execute(f'''INSERT INTO {name} (hs_avg, online_machines, difference, date_, time_) VALUES (?, ?, ?, ?, ?)''',
#                                 (hs_now, total_online_machines, total_online_machines - count, date_, time_))
#                     con.commit()
#                 elif len(user_id) == 2 or user_id == 'Stolbova_BTC':
#                     total_online_machines, hs_now, total_machines = data_f2pool(URL_F2POOL, access_key)
#                     list_hs.append(float(hs_now))
#                     total_online += total_online_machines
#                     cur.execute(
#                         f'''INSERT INTO {name} (hs_avg, online_machines, difference, date_, time_) VALUES (?, ?, ?, ?, ?)''',
#                         (hs_now, total_online_machines, total_online_machines - count, date_, time_))
#                     con.commit()
#                 else:
#                     total_online_machines, hs_now = data_binance(URL_BINANCE, access_key)
#                     list_hs.append(float(hs_now))
#                     total_online += total_online_machines
#                     cur.execute(
#                         f'''INSERT INTO {name} (hs_avg, online_machines, difference, date_, time_) VALUES (?, ?, ?, ?, ?)''',
#                         (hs_now, total_online_machines, total_online_machines - count, date_, time_))
#                     con.commit()
#
#         except Exception as e:
#             print(e)
#             error_log = str(e)
#         if not error_log:
#             result_hs = ('{:.2f}'.format(avg_hs(list_hs)))
#             # print(list_hs, total_online)
#             # print(result_hs)
#             date_ = datetime.now(tz_irk).strftime("%d.%m.%Y")
#             time_ = datetime.now(tz_irk).strftime("%H:%M")
#
#             cur.execute(sql_insert, (result_hs, total_online, total_online-1000 , date_, time_))
#             con.commit()
#             # print('success db')
#     else:
#         count_for = 0
#         send_all_statistics()
#         send_xlsx_statistics()
#         continue
#     count_for += 1
#     print(f'end {count_for}')
#     time.sleep(5)

while count_for < 4:
    print(f'start {count_for}')
    list_hs = []
    total_online = 0
    total_offline = 0
    error_log = None
    try:
        for user_id, access_key_and_count in tqdm(source_data.items()):
            access_key, count = access_key_and_count
            date_ = datetime.now(tz_irk).strftime("%d.%m.%Y")
            time_ = datetime.now(tz_irk).strftime("%H:%M")

            if user_id in switch_user_id.keys():
                name = switch_user_id[user_id]

            if user_id.find('m20s') != -1 or user_id == 'hulucas001':
                total_online_machines, hs_now = data_antpool(URL_HS, URL_MACHINES, access_key, user_id)
                total_machines = count
                list_hs.append(float(hs_now))
                total_online += total_online_machines
                total_offline += total_machines - total_online_machines
                cur.execute(
                    f'''INSERT INTO {name} (hs_avg, online_machines, offline_machines, total_machines, date_, time_) VALUES (?, ?, ?, ?, ?, ?)''',
                    (hs_now, total_online_machines, total_machines - total_online_machines, total_machines, date_, time_))
                con.commit()
            elif len(user_id) == 2 or user_id == 'Stolbova_BTC':
                total_online_machines, hs_now = data_f2pool(URL_F2POOL, access_key)
                total_machines = count
                list_hs.append(float(hs_now))
                total_online += total_online_machines
                total_offline += total_machines - total_online_machines
                cur.execute(
                    f'''INSERT INTO {name} (hs_avg, online_machines, offline_machines, total_machines, date_, time_) VALUES (?, ?, ?, ?, ?, ?)''',
                    (hs_now, total_online_machines, total_machines - total_online_machines, total_machines, date_, time_))
                con.commit()
            else:
                total_online_machines, hs_now = data_binance(URL_BINANCE, access_key)
                total_machines = count
                list_hs.append(float(hs_now))
                total_online += total_online_machines
                total_offline += total_machines - total_online_machines
                cur.execute(
                    f'''INSERT INTO {name} (hs_avg, online_machines, offline_machines, total_machines, date_, time_) VALUES (?, ?, ?, ?, ?, ?)''',
                    (hs_now, total_online_machines, total_machines - total_online_machines, total_machines, date_, time_))
                con.commit()

    except Exception as e:
        print(e)
        error_log = str(e)
    if not error_log:
        result_hs = ('{:.2f}'.format(avg_hs(list_hs)))
        # print(list_hs, total_online)
        # print(result_hs)
        date_ = datetime.now(tz_irk).strftime("%d.%m.%Y")
        time_ = datetime.now(tz_irk).strftime("%H:%M")

        cur.execute(sql_insert, (result_hs, total_online, total_offline, source_total_machines, date_, time_))
        con.commit()
        # print('success db')
        count_for += 1
        time.sleep(3)
        print(f'end {count_for}')
else:
    count_for = 0
    send_all_statistics()
    send_xlsx_statistics()

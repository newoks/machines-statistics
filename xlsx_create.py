import sqlite3

con = sqlite3.connect('example.db')
cur = con.cursor()


def create_worksheet(workbook, worksheet_name, last_4_db):
    worksheet = workbook.add_worksheet(worksheet_name)

    fontsize_format = workbook.add_format({'font_size': 22})
    header_format = workbook.add_format({'bold': True, 'font_color': 'green', 'font_size': 16})
    total_format = workbook.add_format({'num_format': '#,##0.00', 'bold': True, 'font_size': 22})
    time_column_format = workbook.add_format({'bold': True, 'font_color': 'green', 'font_size': 22})

    data_table = [list(row) for row in last_4_db]

    header = ['Average PTH', 'Online', 'Offline', 'Total']
    time_min = [':15', ':30', ':45', ':00']

    for row in data_table:
        row[0] = row[0][0:2]

    for i in range(4):
        data_table[i][0] = data_table[i][0] + time_min[i]

    worksheet.write_row(0, 1, header, header_format)

    row_for_data_add = 1
    for item in data_table:
        worksheet.write_row(row_for_data_add, 0, item)
        row_for_data_add += 1

    worksheet.write(row_for_data_add, 0, 'Total')
    worksheet.write(row_for_data_add, 1, '=AVERAGE(B2:B5)', total_format)
    worksheet.write(row_for_data_add, 2, '=AVERAGE(C2:C5)', total_format)
    worksheet.write(row_for_data_add, 3, '=AVERAGE(D2:D5)', total_format)
    worksheet.write(row_for_data_add, 4, '=AVERAGE(E2:E5)', total_format)

    worksheet.set_column('A:A', 15, time_column_format)
    worksheet.set_column('B:E', 15, fontsize_format)
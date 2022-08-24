import sqlite3

con = sqlite3.connect('example.db')
cur = con.cursor()

# workbook = xlsxwriter.Workbook(f'Statistics.xlsx')


def create_worksheet(workbook, worksheet_name, last_4_db):
    worksheet = workbook.add_worksheet(worksheet_name)

    fontsize_format = workbook.add_format({'font_size': 22})
    header_format = workbook.add_format({'bold': True, 'font_color': 'green', 'font_size': 18})
    total_format = workbook.add_format({'num_format': '#,##0.00', 'bold': True, 'font_size': 22})
    time_column_format = workbook.add_format({'bold': True, 'font_color': 'green', 'font_size': 22})

    data_table = [list(row) for row in last_4_db]
    header = ['Average HS', 'Online', 'Difference', 'Notes']

    worksheet.write_row(0, 1, header, header_format)

    row_for_data_add = 1
    for item in data_table:
        worksheet.write_row(row_for_data_add, 0, item)
        row_for_data_add += 1

    worksheet.write(row_for_data_add, 0, 'Total')
    worksheet.write(row_for_data_add, 1, '=AVERAGE(B2:B5)', total_format)
    worksheet.write(row_for_data_add, 2, '=AVERAGE(C2:C5)', total_format)
    worksheet.write(row_for_data_add, 3, '=AVERAGE(D2:D5)', total_format)

    worksheet.set_column('A:A', 15, time_column_format)
    worksheet.set_column('B:E', 15, fontsize_format)


# workbook.close()

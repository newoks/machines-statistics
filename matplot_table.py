from datetime import datetime
import matplotlib.pyplot as plt
from source_data import tz_irk


def create_table(last_4_db):
    rows = []
    data_table = []
    total_row = [0, 0, 0, 0]
    time_min = [':15', ':30', ':45', ':00']

    for row in last_4_db:
        time_hours = row[4][0:2]
        rows.append(time_hours)
        row = list(row)
        row.pop(4)
        total_row[0] += row[0]/4
        total_row[1] += row[1]/4
        total_row[2] += row[2]/4
        total_row[3] += row[3] / 4
        data_table.append(row)

    total_row[0] = ('{:.2f}'.format(total_row[0]))
    data_table.append(total_row)
    data = data_table
    val1 = ['Average PTH', 'Online', 'Offline', 'Total']

    for i in range(len(rows)):
        rows[i] = rows[i]+time_min[i]
    rows.append('')

    fig, ax = plt.subplots()
    ax.set_axis_off()
    table = ax.table(
        cellText=data,
        rowLabels=rows,
        colLabels=val1,
        rowColours=["palegreen"] * 10,
        colColours=["palegreen"] * 10,
        cellLoc='center',
        loc='center left',
        colWidths=[0.3, 0.23, 0.23, 0.23])

    date_ = datetime.now(tz_irk).strftime("%d.%m.%Y")
    time_second = datetime.now(tz_irk).strftime("%H")
    time_first = int(datetime.now(tz_irk).strftime("%H")) - 1
    ax.set_title(f'{date_}\n'
                 f'{time_first}:00 - {time_second}:00',
                 fontweight="bold", loc='center').set_fontsize(18)
    table.auto_set_font_size(False)
    table.set_fontsize(18)
    table.scale(1.1, 2.0)

    fig.savefig('stat.png', dpi=fig.dpi)

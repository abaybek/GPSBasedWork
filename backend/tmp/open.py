import pandas as pd

from datetime import datetime

# datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

d = pd.read_excel('2018-05-30 17_06_52.xlsx', header=2)


def remove_comma(x):
    return float(x.replace(',', '.'))

def dat(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def get_year(x):
    return datetime.strftime(x, '%Y-%m-%d')

def get_day(x):
    return datetime.strftime(x, '%H:%M:%S')

def datetime_to_float(d):
    return d.timestamp()

d['Longitude'] = d['Longitude'].apply(remove_comma)
d['Latitude'] = d['Latitude'].apply(remove_comma)
d['Altitude (m)'] = d['Altitude (m)'].apply(remove_comma)
d['Date'] = d['Date'].apply(dat)
d['Y'] = d['Date'].apply(get_year)
d['D'] = d['Date'].apply(get_day)
d['F'] = d['Date'].apply(datetime_to_float)
print(d.head())
print(d.dtypes)


heading = """Geolife trajectory
WGS 84
Altitude is in Feet
Reserved 3
0,2,255,My Track,0,0,2,8421376
0"""

print(heading)

with open('export3.plt', 'a') as out:
    out.write(heading)

    for i, row in d.iterrows():
        myList = [row.Latitude, row.Longitude, 0, int(row['Altitude (m)']), row['F'], row['Y'], row['D']]
        myList = ','.join(map(str, myList))
        myList+='\n'
        # print()
        out.write(myList)


print('Done')

import pandas as pd

from datetime import datetime

# datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

parse_dates = ['time']

d = pd.read_csv('dataset/20180605.csv', parse_dates=parse_dates)


d['Longitude'] = d['lon']
d['Latitude'] = d['lat']
d['Date'] = d['time']

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

d['Altitude (m)'] = d['elevation']
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
0
"""

print(heading)

with open('dataset/20180605.plt', 'a') as out:
    out.write(heading)

    for i, row in d.iterrows():
        myList = [row.Latitude, row.Longitude, 0, int(row['Altitude (m)']), row['F'], row['Y'], row['D']]
        myList = ','.join(map(str, myList))
        myList+='\n'
        # print()
        out.write(myList)


print('Done')

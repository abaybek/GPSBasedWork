import pandas as pd
import os
import datetime as dt
import numpy as np
import pyproj

geod = pyproj.Geod(ellps='WGS84')

headers_trajectory = ['lat', 'long', 'null', 'altitude','timestamp_float', 'date', 'time']

# Distance between 2 points
def calculate_distance(long1, lat1, long2, lat2):
    if lat1 == lat2 and long1 == long2:
        return 0
    if False in np.isfinite([long1, long2, lat1, lat2]):
        return np.nan
    if lat1 < -90 or lat1 > 90 or lat2 < -90 or lat2 > 90:
        #raise ValueError('The range of latitudes seems to be invalid.')
        return np.nan
    if long1 < -180 or long1 > 180 or long2 < -180 or long2 > 180:
        return np.nan
        #raise ValueError('The ranя ge of longitudes seems to be invalid.')
    angle1,angle2,distance = geod.inv(long1, lat1, long2, lat2)
    return distance


# Get velocity distance/timedelta
def calculate_velocity(distance, timedelta):
    if timedelta.total_seconds() == 0: return np.nan
    return distance / timedelta.total_seconds()


# Get acceleration diff(velocity)/timedelta
def calculate_acceleration(velocity, velocity_next_position, timedelta):
    delta_v = velocity_next_position - velocity
    if timedelta.total_seconds() == 0: return np.nan
    return delta_v / timedelta.total_seconds()


# Convert str datetime to datetime format
def to_datetime(string):
    return dt.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

# Load labels in the folder
def load_labels_df(filename):
    df = pd.read_csv(filename, sep='\t')
    df['start_time'] = df['Start Time'].apply(lambda x: dt.datetime.strptime(x, '%Y/%m/%d %H:%M:%S'))
    df['end_time'] = df['End Time'].apply(lambda x: dt.datetime.strptime(x, '%Y/%m/%d %H:%M:%S'))
    df['labels'] = df['Transportation Mode']
    df = df.drop(['End Time', 'Start Time', 'Transportation Mode'], axis=1)
    return df

# Load trajectory
def load_trajectory_df(full_filename):
    subfolder = full_filename.split('/')[-3]
    trajectory_id = full_filename.split('/')[-1].split('.')[0]
    
    df = pd.read_csv(full_filename, skiprows = 6, header = None, names = headers_trajectory)
   
    df['datetime'] = df.apply(lambda z: to_datetime(z.date + ' ' + z.time), axis=1)
    df['datetime_next_position'] = df['datetime'].shift(-1)
    df['timedelta'] = df.apply(lambda z: z.datetime_next_position - z.datetime, axis=1)
    df = df.drop(['datetime_next_position'], axis=1)
    df = df.drop(['null', 'timestamp_float', 'date', 'time'], axis=1)
    
    df['long_next_position'] = df['long'].shift(-1)
    df['lat_next_position'] = df['lat'].shift(-1)
    df['distance'] = df.apply(lambda z: calculate_distance(z.long, z.lat, z.long_next_position, z.lat_next_position), axis=1)
    df = df.drop(['long_next_position', 'lat_next_position'], axis=1)
    
    df['velocity'] = df.apply(lambda z: calculate_velocity(z.distance, z.timedelta), axis=1)
    df['velocity_next_position'] = df['velocity'].shift(-1)
    df['acceleration'] = df.apply(lambda z: calculate_acceleration(z.velocity, z.velocity_next_position, z.timedelta), axis=1)
    df = df.drop(['velocity_next_position'], axis=1)
    
    df['trajectory_id'] = trajectory_id
    df['subfolder'] = subfolder
    df['labels'] = ''
    calculate_agg_features(df)
    
    # data cleaning, after aggregation some mess can happen 
    # df = df.dropna()
    # df = df.reset_index(drop=True)
    # output only 15nth row
    # every_nth_row = 15
    # df = df[df.index % every_nth_row == 0]
    return df

#This method calculates the aggregated feature and 
#saves them in the original df
def calculate_agg_features(df):
    # Rolling number, in this dataset it would be near 1 minute (2 seconds between data points)
    roll = 30
    
    # Speed on whole road
    df.loc[:, 'v_ave'] = np.nanmean(df['velocity'].values)
    df.loc[:, 'v_med'] = np.nanmedian(df['velocity'].values)
    df.loc[:, 'v_max'] = np.nanmax(df['velocity'].values)
    df.loc[:, 'v_min'] = np.nanmin(df['velocity'].values)
    df.loc[:, 'v_std'] = np.nanstd(df['velocity'].values)
    
    # Speed on some piece of road
    df.loc[:, 'v_rol'] = df['velocity'].rolling(roll).mean()
    df.loc[:, 'v_rsd'] = df['velocity'].rolling(roll).std()
    df.loc[:, 'v_qu1'] = df['velocity'].rolling(roll).quantile(0.25)
    df.loc[:, 'v_qu2'] = df['velocity'].rolling(roll).quantile(0.5)
    df.loc[:, 'v_qu3'] = df['velocity'].rolling(roll).quantile(0.75)
    
    # Acceleration on whole road
    df.loc[:, 'a_ave'] = np.nanmean(df['acceleration'].values)
    df.loc[:, 'a_med'] = np.nanmedian(df['acceleration'].values)
    df.loc[:, 'a_max'] = np.nanmax(df['acceleration'].values)
    df.loc[:, 'a_min'] = np.nanmin(df['acceleration'].values)
    df.loc[:, 'a_std'] = np.nanstd(df['acceleration'].values)
    
    # Acceleration on piece of road
    df.loc[:, 'a_rol'] = df['acceleration'].rolling(roll).mean()
    df.loc[:, 'a_rsd'] = df['acceleration'].rolling(roll).std()
    df.loc[:, 'a_qu1'] = df['acceleration'].rolling(roll).quantile(0.25)
    df.loc[:, 'a_qu2'] = df['acceleration'].rolling(roll).quantile(0.5)
    df.loc[:, 'a_qu3'] = df['acceleration'].rolling(roll).quantile(0.75)
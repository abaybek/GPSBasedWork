import os
from django.db import models
from django.core.files import File
from .utils import load_trajectory_df
import gmplot

# ML model
from catboost import CatBoostClassifier
from sklearn import preprocessing
from django.conf import settings
import numpy as np
model = CatBoostClassifier().load_model(settings.MODEL_FILE)
encoder = preprocessing.LabelEncoder()
encoder.classes_ = np.load(settings.MODEL_HEADER)
X_columns = ['distance', 'velocity', 'acceleration',
             'v_rol', 'v_rsd', 'v_qu1', 'v_qu2', 'v_qu3',  
             'a_rol', 'a_rsd', 'a_qu1', 'a_qu2', 'a_qu3']

colors_map = {
    '0.0': 'royalblue',
    '1.0': 'green',
    '2.0': 'coral',
    '3.0': 'blueviolet'
}

encode_map = {
    '0.0': 'bike',
    '1.0': 'train',
    '2.0': 'vehicle',
    '3.0': 'walk'
}

# Create your models here.

class GpsData(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=70)
    data = models.FileField(upload_to='data/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    mapfile = models.FileField(upload_to='maps/', null=True, blank=True)

    def __str__(self):
        return f"Author: {self.name} - email: {self.email}"
    
    def filename(self):
        return os.path.basename(self.data.name)
    
    @property
    def get_pandas(self):
        return load_trajectory_df(self.data.path)
    
    def get_map(self):
        def predict(df):
            ans = model.predict(df[X_columns])
            df['ans'] = ans
            return df
            
        def get_lat_lon(df):
            outArray = []
            lastAns = -1
            for i, val in df.iterrows():
                c = colors_map[str(val.ans)]
                if lastAns == -1:
                    tmp = {c: []}
                    lastAns = val.ans
                if val.ans != lastAns:
                    outArray.append(tmp)
                    tmp = {c: [(val.lat, val.long)]}
                    lastAns = val.ans
                elif val.ans == lastAns:
                    tmp[c].append((val.lat, val.long))
            return outArray

        def write_map(outArray):
            first = True
            for cArray in outArray:
                for key, value in cArray.items():
                    golden_gate_park_lats, golden_gate_park_lons = zip(*value)
                    if first:
                        gmap = gmplot.GoogleMapPlotter(golden_gate_park_lats[0], golden_gate_park_lons[0], 13, 'AIzaSyAmwiUhqobHQDom0pYa8mdwR8nx7y6GvlM')
                        first = False
                    gmap.plot(golden_gate_park_lats, golden_gate_park_lons, key, edge_width=10)

            gmap.draw("my_map.html")
            with open('my_map.html', 'r') as myfile:
                data=myfile.read()
                self.mapfile.save(self.name, File(myfile))
            return data

        def preprocess():
            df = self.get_pandas
            df = predict(df)
            grouped = df.groupby(['ans'])['distance'].sum()
            grouped=grouped.to_json()

            print(df.head())
            print(df.columns)
            print(df['velocity'])
            print(df['velocity'].max(), df['velocity'].min())
            # print(df.velocity)

            array = get_lat_lon(df)
            html = write_map(array)
            return html, grouped

        html, grouped = preprocess()
        return html, grouped
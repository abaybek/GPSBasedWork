import os
from django.db import models
from .utils import load_trajectory_df
import gmplot

# Create your models here.

class GpsData(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=70)
    data = models.FileField(upload_to='data/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Author: {self.name} - email: {self.email}"
    
    def filename(self):
        return os.path.basename(self.data.name)
    
    def get_map(self):
        def get_lat_lon(df):
            outArray = []
            for i, val in df.iterrows():
                outArray.append((val.lat, val.long))
            return outArray

        def write_map(outArray):
            gmap = gmplot.GoogleMapPlotter(outArray[0][0], outArray[0][1], 13, 'AIzaSyAmwiUhqobHQDom0pYa8mdwR8nx7y6GvlM')
            golden_gate_park_lats, golden_gate_park_lons = zip(*outArray)
            gmap.plot(golden_gate_park_lats, golden_gate_park_lons, 'cornflowerblue', edge_width=10)
            gmap.draw("my_map.html")
            with open('my_map.html', 'r') as myfile:
                data=myfile.read()
            return data

        def preprocess(datapath):
            df = load_trajectory_df(datapath)
            array = get_lat_lon(df)
            html = write_map(array)
            return html

        path = self.data.path
        html = preprocess(path)
        return html
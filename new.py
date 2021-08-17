import csv

import requests
from folium.plugins import HeatMapWithTime

import main_america
import io
import sys
import math
import folium
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from main import set_traffic_jam
from main_america import group_it
class MyApp(QWidget):
    def __init__(self,window_width,window_height,width,height,location,df):
        super().__init__()
        self.setWindowTitle('folium map')
        self.window_width, self.window_length = window_width, window_height
        self.setMaximumSize(self.window_width, self.window_length)

        df = df[['name', 'highway', 'osm_id', 'Y', 'X']]
        points=[]
        for point in zip(df['Y'],df['X']):
            points.append([point])
            # print(df['Y'],df['X'])

        print(points)
        m = folium.Map(width=width, height=height, location=location, tiles='openstreetmap', zoom_start=13,
                           min_zoom=3, max_zoom=19)
        f = folium.FeatureGroup("loading move ")
        folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)
        f.add_to(m)

        # folium.PolyLine(group_it(points), color="red", weight=2.5, opacity=1).add_to(m)
        # moves = df['hour'].max()+1
        # lat_long_list = []
        # for i in range(1, moves):
        #     temp = []
        #     for index, instance in df[df['hour'] == i].iterrows():
        #         temp.append([instance['VehicleLoc.lat'], instance['VehicleLoc.long']])
        #     lat_long_list.append(temp)
            # if len(temp)>1:
            #     folium.PolyLine(group_it(temp), color="red", weight=2.5, opacity=1).add_to(m)
        # points=[]
        # for point in zip(df['VehicleLoc.lat'], df['VehicleLoc.long']):
        #     points.append(point)
        # folium.PolyLine(group_it(points), color="blue", weight=2.5, opacity=1).add_to(m)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # for points in lat_long_list:
        #
        # HeatMapWithTime(lat_long_list, radius=10, auto_play=True,position='bottomright',
        #                 gradient={.6: 'blue', .98: 'lime', 1: 'red'}).add_to(m)
        folium.LayerControl().add_to(m)
        # folium.Marker(
        #     location=[47.3489, -124.708],
        #     popup=folium.Popup(max_width=450).add_child(
        #         folium.Vega(vis1, width=450, height=250))
        # ).add_to(m)
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

import os
files = []
directory = r'C:\Users\Ronit.Iconics\PycharmProjects\pythonProject10'  # taking all what we have' no need to match every time
for filename in os.listdir(directory):

        if  filename.startswith('traffic_recordings'):
            files.append(filename)
            print(filename)
if __name__ == '__main__':
    #removing empty rows:
    name='traffic_recordings08_06_21'
    df=pd.read_csv(name+".csv",error_bad_lines=False)
    df=df.dropna()
    header=['road','point','hour','traffic_percent','currentSpeed','freeFlowSpeed']
    data=[]
    # response = requests.get(
    #     "https://api.tomtom.com/routing/1/calculateRoute/52.50931,13.42936:52.50274,13.43872/json?&key=JFF6W4ZnqWnNSJarr8RsiTP4GeqCkJND")
    #    # "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/xml?key=JFF6W4ZnqWnNSJarr8RsiTP4GeqCkJND")
    # print(response.json()["routes"][0]["legs"][0]["points"])
    for index,instance in df.iterrows():
        road=instance['road']
        point=instance['point']
        if instance['freeFlowSpeed']>0:
            traffic=(int((1-instance['currentSpeed']/instance['freeFlowSpeed'])*100))
        else:
            traffic=0
        # traffic=str(instance['traffic_percent']*100)+'%'
        # data.append([instance['road'],instance['point'],instance['hour'],traffic,instance['currentSpeed'],instance['freeFlowSpeed']])
        # if 'Eastren' in road:
        #     road=road.replace('Eastren','Eastern')
        #     print(road)
        # if 'Westren' in road:
        #     road=road.replace('Westren','western')
        data.append([road,point,instance['hour'],traffic,instance['currentSpeed'],instance['freeFlowSpeed']])
    # print(data)

    with open(name+'_1.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    # https://api.tomtom.com/routing/1/calculateRoute/52.50931%2C13.42936%3A52.50274%2C13.43872/json?avoid=unpavedRoads&key=*****
    # # Load map centred on London
    # uk = folium.Map(location=[36.1387,-81.1725], zoom_start=15)
    #
    # # add a marker for each toilet
    # for each in points:
    #     folium.Marker(each).add_to(uk)

    # Save map
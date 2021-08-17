import io
import sys
import math
import folium
import pandas as pd
from datetime import datetime

import pytz
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from folium.plugins import HeatMapWithTime

import numpy as np
from geopy import Nominatim


def airline_distance(point1, point2):
    return math.sqrt(math.pow((np.float32(point1[0]) - np.float32(point2[0])), 2)
                     + math.pow((np.float32(point1[1]) - np.float32(point2[1])), 2))


def closest_point(point, group):
    closest_point_index, distance = 0, 1
    for any_point in group:
        current_distance = airline_distance(any_point, point)
        if current_distance < distance:
            distance = current_distance
            closest_point_index = group.index(any_point)

    return distance, closest_point_index

def find_index(point, group, index_closest, index_before_closest):
    if index_closest==0:
        return 0
    dis1=airline_distance(group[index_closest], group[index_before_closest])
    # dis2=airline_distance(point, group[index_closest])
    dis3=airline_distance(point, group[index_before_closest])
    if (dis3<dis1):
        return index_closest
    else:
       return index_closest + 1

# def sort(group):


def group_it(temp):
    groups, group = [], []
    if len(temp) > 0:
        # print('first:',len(temp),len(group))
        group.append(temp[0])
        temp.pop(0)
        # print('second: ',len(temp),len(group))
        while len(temp) > 0:  # each iteration doing several transfers from temp until it empty
            for element in temp:
                # dis, ind = closest_point(element, group)
                dis=airline_distance(element,group[len(group)-1])
                if dis < 5e-4:
                    # group.insert(find_index(element,temp,ind,ind-1), element)
                    group.append(element)
                    temp.remove(element)
            groups.append(group)
            # print('loop: ',len(temp),len(group))
            if len(temp) > 0:
                group = [temp[0]]
                # print('afterloop: ', len(temp), len(group))
    return groups

# def group_groups(groups):
#     ret_group=[]
#     i=1
#     while i in range(len(groups)):
#        if airline_distance(groups[i-1][len(groups[i-1])-1],groups[i][0])<5e-3:
#            ret_group.append(groups[i-1]+groups[i])


def set_traffic_jam(coords, f, str):
    color = "blue"
    if len(coords) > 60:
        color = "purple"
    elif len(coords) > 30:
        color = "red"
    folium.vector_layers.PolyLine(coords, popup='<b>Path of Vehicle_</b>' + str,
                                  tooltip='Vehicle' + str,
                                  color=color, weight=10).add_to(f)


def set_traffic_jam_group(coords, f, strings, m):
    for group,str in zip(coords,strings):
        set_traffic_jam(group, f, str)
    f.add_to(m)
    # i = 0
    # while i in range(len(coords) - 1):
    #     # print(coords[i],coords[i+1],coords[i]+coords[i+1])
    #     group=coords[i]+coords[i+1]
    #     set_traffic_jam(group, f, str)
    #     f.add_to(m)
    #     i+=1


class MyApp(QWidget):
    def __init__(self, window_width, window_height, width, height, location, df):
        super().__init__()
        self.setWindowTitle('folium map')
        self.window_width, self.window_length = window_width, window_height
        self.setMaximumSize(self.window_width, self.window_length)

        df = df[['RecordedAtTime', 'VehicleRef', 'VehicleLocation.Latitude',
                 'VehicleLocation.Longitude']]  # take only relevant columns
        tz_NY = pytz.timezone('America/New_York')
        datetime_NY = datetime.now(tz_NY)

        df.duplicated().value_counts()
        df = df.drop_duplicates()
        df.isnull().sum()
        df['RecordedAtTime'] = pd.to_datetime(df['RecordedAtTime'])
        # df['RecordedAtTime']=df['RecordedAtTime']
        # print(df['RecordedAtTime'][9].strftime("%H"),datetime_NY.strftime("%H"))
        # Creating hour column rows = [row for row in file if row['Name'] in Names]
        # df= [current_hour for current_hour in df
        #                      if current_hour['RecordedAtTime'].strftime("%H")==datetime_NY.strftime("%H")]
        df['hour'] = df['RecordedAtTime'].apply(lambda x: x.hour + 1)
        df2 = pd.DataFrame(df.groupby(['hour', 'VehicleRef'])['RecordedAtTime'].max())
        df2.reset_index(inplace=True)
        df3 = pd.merge(df2, df, left_on=['hour', 'VehicleRef', 'RecordedAtTime'],
                       right_on=['hour', 'VehicleRef', 'RecordedAtTime'])
        df3.head()

        # Creating hour column

        m = folium.Map(width=width, height=height, location=location, tiles='cartodbpositron', zoom_start=13,
                       min_zoom=3, max_zoom=18)
        moves = df['hour'].max() + 1
        strings,lat_long_list= [],[]
        # for i in range(1, moves):
        for i in range(1, moves):
            temp = []
            for index, instance in df[df['hour'] == i].iterrows():
                temp.append([instance['VehicleLocation.Latitude'], instance['VehicleLocation.Longitude']])
            lat_long_list.append(temp)

        # coords, all_coords_list = [] ,[]


        # print(datetime_NY.strftime("%H"))
        roads = {}
        # vahicleRef = 'car 1'
        geolocator = Nominatim(user_agent="name_of_your_app")
        for lat,long in zip(df['VehicleLocation.Latitude'], df['VehicleLocation.Longitude']):
            # print(lat,long)
            location = geolocator.reverse(str(lat)+", "+str(long))
            nameOfStreet = (location.address).split(",")
            first_value = nameOfStreet[0]
            if first_value.isnumeric():  # or first_value.split("-")[0].isnumeric()
                nameOfStreet.remove(first_value)
            road = nameOfStreet[0], nameOfStreet[1], nameOfStreet[2]
            # if nameOfStreet[0].split("-")[0].isnumeric():
            # print(road)
            if road not in roads:
                roads[road] = [[lat,long]]
            else:
                roads[road] += [[lat,long]]
                # all_coords_list.append(coords)
        # print(vehicles)
                # coords = []
                # strings.append(str(i))
                # i+=1
            # coords.append(point)
        # print(strings)
        f = folium.FeatureGroup("")
        for road in roads:
            set_traffic_jam(roads[road],f,road)
        f.add_to(m)
        # set_traffic_jam_group(all_coords_list, f, strings, m)

        layout = QVBoxLayout()
        self.setLayout(layout)

        HeatMapWithTime(lat_long_list, radius=10, auto_play=True, position='bottomright',
                        gradient={.6: 'blue', .98: 'lime', 1: 'red'}).add_to(m)
        folium.LayerControl().add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)


# print(df['hour'].to_string())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    df = pd.read_csv('mta/mta_1706_0_0_1.csv', error_bad_lines=False)
    myApp = MyApp(window_width=1600, window_height=1400, width=600, height=480,
                  location=[40.644800, -73.916721], df=df)
    myApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("closing window")

# app = QApplication(sys.argv)


# print((np.float32(instance['VehicleLoc.long'])-np.float32(instance['VehicleLoc.long'])))
# print(airline_distance(temp[0],temp[1]))
#         colors=['blue','red','green']
#         f1 = folium.FeatureGroup("Vehicle 1")
#         f2 = folium.FeatureGroup("Vehicle 2")
#         f3 = folium.FeatureGroup("Vehicle 3")
#         line_1 = folium.vector_layers.PolyLine(coords[0], popup='<b>Path of Vehicle_1</b>', tooltip='Vehicle_1',
#                                                color='blue', weight=10).add_to(f1)
#         line_2 = folium.vector_layers.PolyLine(coords[1], popup='<b>Path of Vehicle_2</b>', tooltip='Vehicle_2',
#                                                color='red', weight=10).add_to(f2)
#         line_3 = folium.vector_layers.PolyLine(coords[2], popup='<b>Path of Vehicle_3</b>', tooltip='Vehicle_3',
#                                                color='green', weight=10).add_to(f3)
#         f1.add_to(self.m)
#         f2.add_to(self.m)
#         f3.add_to(self.m)

# folium.Marker(
#     location=[47.3489, -124.708],
#     popup=folium.Popup(max_width=450).add_child(
#         folium.Vega(vis1, width=450, height=250))
# ).add_to(m)
# if len(temp)>1:
#     folium.PolyLine(group_it(temp), color="red", weight=2.5, opacity=1).add_to(m)
# points=[]
# for point in zip(df['VehicleLoc.lat'], df['VehicleLoc.long']):
#     points.append(point)

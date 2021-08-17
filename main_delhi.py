import io
import sys
import math
import folium
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from folium.plugins import HeatMapWithTime
# from branca.element import Figure
import numpy as np
from main_america import group_it,set_traffic_jam,set_traffic_jam_group


class MyApp(QWidget):
    def __init__(self, window_width, window_height, width, height, location, df):
        super().__init__()
        self.setWindowTitle('folium map')
        self.window_width, self.window_length = window_width, window_height
        self.setMaximumSize(self.window_width, self.window_length)
        df = df[['RecordedAtDate', 'Time', 'VehicleRef', 'VehicleLoc.lat', 'VehicleLoc.long']]

        df['Time'] = pd.to_timedelta(df['Time'])

        # Creating hour column

        df['hour'] = 0

        # uniqe values of cars
        carListInAction = []
        for x in df['VehicleRef']:  # initialize cars
            if x not in carListInAction:
                carListInAction.append(x)
                # print(df['VehicleLoc.lat'],df['VehicleLoc.long'])
        CarSteps = [0] * len(carListInAction)
        loopHours = 0
        for x in df['VehicleRef']:
            for i in range(0, len(carListInAction)):
                carPlace = i + 1
                if (x.find(str(carPlace)) != -1 and len(str(carPlace)) == (len(x) - 4)):
                    CarSteps[i] += 1
                    df['hour'][loopHours] = CarSteps[i]
                    loopHours += 1
                    break
        # print(str(carPlace))
        m = folium.Map(width=width, height=height, location=location, tiles='cartodbpositron', zoom_start=13,
                       min_zoom=3, max_zoom=18)
        moves = df['hour'].max() + 1
        all_coords,lat_long_list, all_coords_list,strings,strings2 = [], [],[],[],[]

        for i in range(1, moves):
            temp = []
            for index, instance in df[df['hour'] == i].iterrows():
                temp.append([instance['VehicleLoc.lat'], instance['VehicleLoc.long']])
            strings.append(str(i))
            lat_long_list.append(temp)
            # all_coords += temp
            # strings2+=" "

            # set_traffic_jam(temp,f,str(i))
        coords,vehicles=[], {}
        vahicleRef='car 1'
        for vehicle,point in zip(df['VehicleRef'],zip(df['VehicleLoc.lat'],df['VehicleLoc.long'])):
            print(vehicle,point,point)
            if vehicle not in vehicles:
                vehicles[vehicle]=[point]
            else:
                vehicles[vehicle]+=[point]
                # all_coords_list.append(coords)
                # coords=[]
            # coords.append(point)
        print(vehicles)
        f = folium.FeatureGroup("")
        # set_traffic_jam_group(all_coords_list, f, strings, m)
        for vehicle, i in zip(vehicles, range(len(vehicles))):
            set_traffic_jam(vehicles[vehicle], f, str(i + 1))
        f.add_to(m)
        # set_traffic_jam_group(group_it(all_coords),f,strings2,m)
        # folium.PolyLine(group_it(points), color="blue", weight=2.5, opacity=1).add_to(m)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    df = pd.read_csv('traffic.csv', error_bad_lines=False)

    myApp = MyApp(window_width=1600, window_height=1400, width=600, height=480,
                  location=[28.644800, 77.216721], df=df)

    myApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("closing window")



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

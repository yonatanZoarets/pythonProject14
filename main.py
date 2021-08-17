import io
import sys
import math
import folium
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from folium.plugins import HeatMapWithTime
import time
from datetime import datetime
import numpy as np

def airline_distance(point1, point2):
    return math.sqrt(math.pow((np.float32(point1[0]) - np.float32(point2[0])), 2)
                     + math.pow((np.float32(point1[1]) - np.float32(point2[1])), 2))
def set_traffic_jam(coords, f, str):
    color = "blue"
    if len(coords) > 60:
        color = "purple"
    elif len(coords) > 30:
        color = "red"
    folium.vector_layers.PolyLine(coords, popup='<b>Path of traffic_</b>' + str,
                                  tooltip='Traffic' + str,
                                  color=color, weight=10).add_to(f)


# def closest_point(point, group):
#     closest_point_index, distance = 0, 1
#     for any_point in group:
#         current_distance = airline_distance(any_point, point)
#         if current_distance < distance:
#             distance = current_distance
#             closest_point_index = group.index(any_point)

#     return distance, closest_point_index

# def find_index(point, group, index_closest, index_before_closest):
#     if index_closest==0:
#         return 0
#     dis1=airline_distance(group[index_closest], group[index_before_closest])
#     # dis2=airline_distance(point, group[index_closest])
#     dis3=airline_distance(point, group[index_before_closest])
#     if (dis3<dis1):
#         return index_closest
#     else:
#        return index_closest + 1

# # def sort(group):


# def group_it(temp):
#     groups, group = [], []
#     if len(temp) > 0:
#         # print('first:',len(temp),len(group))
#         group.append(temp[0])
#         temp.pop(0)
#         # print('second: ',len(temp),len(group))
#         while len(temp) > 0:  # each iteration doing several transfers from temp until it empty
#             for element in temp:
#                 # dis, ind = closest_point(element, group)
#                 dis=airline_distance(element,group[len(group)-1])
#                 if dis < 9e-4:
#                     # group.insert(find_index(element,temp,ind,ind-1), element)
#                     group.append(element)
#                     temp.remove(element)
#             groups.append(group)
#             # print('loop: ',len(temp),len(group))
#             if len(temp) > 0:
#                 group = [temp[0]]
#                 # print('afterloop: ', len(temp), len(group))
#     return groups
class MyApp(QWidget):
    def __init__(self, window_width, window_height, width, height, location, df):
        super().__init__()
        self.setWindowTitle('folium map')
        self.window_width, self.window_length = window_width, window_height
        self.setMaximumSize(self.window_width, self.window_length)
        m = folium.Map(width=width, height=height, location=location,tiles='cartodbpositron', zoom_start=13, min_zoom=3, max_zoom=19)

        roads =  {}
        for road, c_direction, subrub, point in zip(df['road_name'], df['cardinal_direction_name'], df['suburb'],
                                                    zip(df['wgs84_latitude'], df['wgs84_longitude'])):
            if (road, c_direction, subrub) not in roads:
                roads[road, c_direction, subrub] = [point]
            else:
                # dis=airline_distance(roads[road, c_direction, subrub][len(roads[road, c_direction, subrub])-1],point)
                if point not in roads[road, c_direction, subrub]:
                    roads[road, c_direction, subrub] += [point]

                # print(roads[road, c_direction, subrub][len(roads[road, c_direction, subrub])-1],point,roads[road, c_direction, subrub])
        # for road, subrub, point in zip(df['road_name'], df['suburb'],
        #                                             zip(df['wgs84_latitude'], df['wgs84_longitude'])):
        #     if (road, subrub) not in roads:
        #         roads[road,  subrub] = [point]
        #     else:
        #         roads[road, subrub] += [point]


        f = folium.FeatureGroup("")

        layout = QVBoxLayout()
        self.setLayout(layout)

        for road in (roads):
            set_traffic_jam(roads[road], f, str(road))
        f.add_to(m)

        folium.LayerControl().add_to(m)
        f.add_to(m)


        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # df = pd.read_csv('Traffic_Volume_Viewer_-_Station_Information.csv', error_bad_lines=False)
    df = pd.read_csv('Traffic_Volume_Viewer_2019.csv', error_bad_lines=False)
    myApp = MyApp(window_width=1600, window_height=1400, width=600, height=480,
                  location=[-33.8, 151.216721], df=df)
    myApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("closing window")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

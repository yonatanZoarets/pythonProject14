import requests
import csv
import pandas as pd
import random

def try_except_next(array, params, i, func):
    if i == len(array):
        return 0
    try:
        return func(array[i], params)
    except:
        return try_except_next(array, params, i + 1,func)

df = pd.read_csv("roads_points.csv", error_bad_lines=False)
from geopy.geocoders import Nominatim


def json_it(path):
    res = requests.get(path)
    return res.json()


def read_routing_point_api_data(key, point1, point2):
    path = "https://api.tomtom.com/routing/1/calculateRoute/" + point1 + ":" + point2 + "/json?key=" + key + "&traffic=true"
    return json_it(path)


if __name__ == '__main__':
    keys = ["JFF6W4ZnqWnNSJarr8RsiTP4GeqCkJND", "fN1GFcLNR2Jd0oYxrQrhpqOTpeGAq9YM",
            "CwMysQRumeK8JZ9JG9WVdGIaixZY5ohR",
            "19TxtGiVQdQhRqPlVGhc2fzVI3WB3AUc"]
    points_list = []
    geolocator = Nominatim(user_agent="name_of_your_app")
    for index, instance in df.iterrows():
        point = index
        points_list.append(instance['point'])
    with open("org_des_time.csv", 'w', encoding="utf-8") as s:
        csv_f1 = csv.writer(s)
        for index, instance in df.iterrows():
            if index % 6 == 0:
                point1, point2 = points_list[index], points_list[random.randint(0, len(points_list))]
                print(point1, point1.split(","))
                data = try_except_next(array=keys, params=[point1, point2], i = 0, func=read_routing_point_api_data)
                if data == 0:
                    flag = 4
                    print('breaked')
                    break

                # print(point, datetime_SDN.strftime("%H:%M"))  # traffic,

                # csv_f1 = csv.writer(f)
                # csv_f1.writerow([])

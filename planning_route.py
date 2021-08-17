import csv
import random
from datetime import datetime

import pandas as pd
import pytz
from geopy import Nominatim
from schedule import right_time

from org_des_time import json_it

def try_except_next(array, params, i, func):
    if i == len(array):
        return 0
    try:
        return func(array[i], params)
    except:
        return try_except_next(array, params, i + 1,func)

def read_routing_point_api_data(key, points):
    path = "https://api.tomtom.com/routing/1/calculateRoute/" + points[0] + ":" + points[
        1] + "/json?key=" + key + "&traffic=true"
    return json_it(path)


if __name__ == '__main__':
    # df = pd.read_csv("newy (1).csv", error_bad_lines=False)
    # f1 = open('routes.csv', 'w', encoding="utf-8", newline='')
    # csv_f1 = csv.writer(f1)
    # for index, instance in df.iterrows():
    #     csv_f1.writerow([instance['date_departure'],instance['date_arrive'],instance['travel_time'],
    #                      instance['start_point_lat'],instance['start_point_lon'],
    #                      instance['end_point_lat'],instance['end_point_lon'],"route"+str(index+1)])
    df = pd.read_csv("roads_points.csv", error_bad_lines=False)

    f1 = open('routes_1.csv', 'w', encoding="utf-8", newline='')
    csv_f1 = csv.writer(f1)
    csv_f1.writerow(["dep", "des", "route", "time"])
    print(["dep", "des", "route", "time"])
    f1.close()
    f2 = open('org_des_time.csv', 'w', encoding="utf-8", newline='')
    csv_f2 = csv.writer(f2)
    csv_f2.writerow(["route", "inter_point"])
    print(["route", "inter_point"])
    f2.close()

    keys = ["JFF6W4ZnqWnNSJarr8RsiTP4GeqCkJND", "fN1GFcLNR2Jd0oYxrQrhpqOTpeGAq9YM",
            "CwMysQRumeK8JZ9JG9WVdGIaixZY5ohR",
            "19TxtGiVQdQhRqPlVGhc2fzVI3WB3AUc"]
    points_list = []
    geolocator = Nominatim(user_agent="name_of_your_app")
    tz_SDN = pytz.timezone('Australia/Sydney')
    for index, instance in df.iterrows():
        points_list.append(instance["point"])
    flag = 1
    q = 15
    while flag == 1:
        if right_time(timeZone=tz_SDN, start_hour=4, end_hour=10, minutes=30):
            for index, instance in df.iterrows():
                if index % q == 0:
                    point1, point2 = instance['point'], points_list[random.randint(0, len(points_list))]
                    route = "route " + str(index / q + 1).replace(".0", "")
                    data = try_except_next(keys, params=[point1, point2], i=0, func=read_routing_point_api_data)
                    if data == 0:
                        flag = 4
                        print('breaked')
                        break
                    f1 = open('routes_1.csv', 'a', encoding="utf-8", newline='')
                    csv_f1 = csv.writer(f1)
                    csv_f1.writerow([point1, point2, route, data['routes'][0]['summary']["travelTimeInSeconds"],
                                     data['routes'][0]['summary']['departureTime'].split('T')[1].split('+')[0]])
                    print(data['routes'][0]['summary']['departureTime'].split('T')[1].split('+')[0])
                    # print([point1, point2])
                    i = 0
                    for point_js in data['routes'][0]['legs'][0]['points']:
                        point = str(point_js['latitude']) + "," + str(point_js['longitude'])
                        if i % 9 == 0:
                            f2 = open('org_des_time.csv', 'a', encoding="utf-8", newline='')
                            csv_f2 = csv.writer(f2)
                            try:
                                csv_f2.writerow([route, str(geolocator.reverse(point)).split(',')[0]])
                                print([route, str(geolocator.reverse(point)).split(',')[0]])
                            except:
                                csv_f2.writerow([])

                        i += 1

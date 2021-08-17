import os
import glob
import folium
import pandas as pd
import csv
from datetime import datetime as dt
import datetime
import requests as requests
from geopy.geocoders import Nominatim

# set working directory

if __name__ == '__main__':
    # os.chdir("/mydir")
    files = []
    directory = r'C:\Users\Ronit.Iconics\PycharmProjects\pythonProject10\mydir\done'  # taking all what we have' no need to match every time
    for filename in os.listdir(directory):
        if filename in ['02062 - Enmore Road.csv',
'02396 - King Street.csv',
'69087 - Prospect Highway.csv',
'24008 - King Georges Road.csv']:
            files.append(filename)
            print(filename)
        # else:
        #     continue

    hours = ["hour_00", "hour_01", "hour_02", "hour_03",
             "hour_04", "hour_05",
             "hour_06", "hour_07", "hour_08", "hour_09", "hour_10", "hour_11", "hour_12", "hour_13", "hour_14",
             "hour_15",
             "hour_16", "hour_17",
             "hour_18", "hour_19", "hour_20", "hour_21", "hour_22",
             "hour_23"]  # avoiding repeated rows and memory location
    new_files = []
    for filename in files:
        # name = "mydir/" + filename + ".csv"
        if "-" in filename:  # if it with number before the name - take only the name
            num = 8
        else:
            num = 0
        dir_name='mydir/done/'
        df = pd.read_csv(dir_name + filename, error_bad_lines=False)
        relevant = ["date", "cardinal_direction_seq", "public_holiday", "school_holiday"] + hours
        df = df[relevant]  # take only relevant columns
        df.duplicated().value_counts()
        df = df.drop_duplicates()
        df = df.dropna()
        df.isnull().sum()
        dir_name = 'mydir/'
        for index, instance in df.iterrows():
            name = filename.replace(".csv", "") + " " + instance["cardinal_direction_seq"] + '.csv'
            if name not in new_files:
                new_files.append(name)
                f = open(dir_name + name, 'w', encoding="utf-8", newline='')  #
                csv_f1 = csv.writer(f)
                csv_f1.writerow(["date", "month", "public_holiday", "school_holiday", "hour", "numVehicle"])
                f.close()

            f = open(dir_name + name, 'a', encoding="utf-8", newline='')  # "mydir/" +
            csv_f1 = csv.writer(f)
            try:
                date = dt.strptime(instance["date"], '%d/%m/%Y')
            except:
                date = dt.strptime(instance["date"], '%Y-%m-%d')
            print(date.strftime('%d/%m'))
            temp = [(date.strftime('%d/%m/%y')), date.strftime("%B")
                , instance["public_holiday"], instance["school_holiday"]]
            for hour in hours:  # taking each hour
                csv_f1.writerow(temp + [hour[5:7], instance[hour]])

# geolocator = Nominatim(user_agent="name_of_your_app")
# for i in range(1, moves):  # creating the coordinate for HeatMap
#     temp = []

#     point=instance['VehicleLocation.Latitude'], instance['VehicleLocation.Longitude']]
#     nameOfStreet = (location.address).split(",")
#     first_value = nameOfStreet[0]
#     if first_value.isnumeric() or first_value.split("-")[0].isnumeric():
#         nameOfStreet.remove(first_value)
#     if len(first_value.split("&")) > 1:
#         nameOfStreet.pop(0)
#         nameOfStreet.pop(1)
#         temp = nameOfStreet
#         nameOfStreet = first_value.split("&") + temp
#     road = nameOfStreet[0]
#     for part in (nameOfStreet[0], nameOfStreet[1], nameOfStreet[2]):
#         if ((bool([ele for ele in map_line_des if (ele in part)])
#              and part in [nameOfStreet[0], nameOfStreet[1]])
#                 or (part == nameOfStreet[2] and
#                     bool(ele for ele in ['Avenue', 'Boulevard', 'Street', 'Road', 'Tunnel', 'Expressway'
#                         , 'Parkway', 'Turnpike', 'Cross', 'Bridge'] if (ele in part)))):
#             road = part.strip()
#     csv_f1.writerow([road]+file[index])
# if len(file) < 30:
# points += str(instance['VehicleLocation.Latitude']) + "," + str(
#     instance['VehicleLocation.Longitude']) + "|"
# else:
# points += str(instance['VehicleLocation.Latitude']) + "," + str(instance['VehicleLocation.Longitude'])
# print(points,points[:-1:])
# path = "https://roads.googleapis.com/v1/snapToRoads?path=" + points[:-1:] + "&interpolate=false&key=AIzaSyAXjZkNImardcXuwga_WUqwk-TmAdW7hPU"
# response = requests.get(path)
# for item, row in zip(response.json()['snappedPoints'], file):
#     road = item['placeId']
#     csv_f1.writerow(row + [road])
# file, points = [], ""
# print(response.json())

# points += str(instance['VehicleLocation.Latitude']) + "," + str(instance['VehicleLocation.Longitude']) + "|"
# path = "https://roads.googleapis.com/v1/snapToRoads?path=" + points[
#                                                              :-1:] + "&interpolate=false&key=AIzaSyAXjZkNImardcXuwga_WUqwk-TmAdW7hPU"
# response = requests.get(path)
# for item in response.json()['snappedPoints']:
#     road = item['placeId']
#     road_keys.append(road)
# print(points[:-1:])
# response = requests.get(
#     "https://roads.googleapis.com/v1/snapToRoads?path=-35.27801,149.12958|-35.28032,149.12907|-35.28099,149.12929|-35.28144,149.12984|-35.28194,149.13003|-35.28282,149.12956|-35.28302,149.12881|-35.28473,149.12836&interpolate=true&key=AIzaSyAXjZkNImardcXuwga_WUqwk-TmAdW7hPU")
# print(response.json())
# file[0].append("RoadName")


# print(file[index])
# csv_f1.writerows(file)
# df3.to_csv('mta_1706_0_0_0.csv')
# geolocator = Nominatim(user_agent="name_of_your_app")
# for long,lat in zip(df['VehicleLocation.Longitude'],df['VehicleLocation.Latitude']):
#     location = geolocator.reverse(str(long)+", "+str(lat))
#     # df['address']=location.address
#     print(location,long,lat)
# Finded_URL = [
# 'mydir/02243 - Eastern Distributor.csv','mydir/03018 - Eastern Distributor.csv'
# ,'mydir/10052 - Syd Einfeld Drive.csv'
#           ,'mydir/19065 - Parramatta Road(1).csv','mydir/21032 - Strathallen Avenue.csv','mydir/22043 - Ourimbah Road.csv','mydir/28022 - Liverpool Road.csv'

# ]
# ,'mydir/30005 - Parramatta Road.csv','mydir/55028 - Pittwater Road.csv','mydir/74062 - Epping Road.csv','mydir/74453 - Epping Road.csv']
# find all csv files in the folder
# use glob pattern matching -> extension = 'csv'
# save result in list -> all_filenames

# combined_csv = pd.concat([pd.read_csv(f, header=None) for f in Finded_URL])
#
# combined_csv.head()
#
# combined_csv.to_csv("Eastern Distributor.csv", quotechar='"',
#                     quoting=csv.QUOTE_ALL, index=False, encoding='utf-8')

# extension = 'csv'
# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# # print(all_filenames)
#
# # combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
# # export to csv
# combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')

# geolocator = Nominatim(user_agent="name_of_your_app")
# print(str(55)+","+str(66))
# df['address'] = geolocator.reverse(str(df['VehicleLocation.Longitude'])+", "+str(df['VehicleLocation.Latitude'])) #lat, long
# df.to_csv(mta_1706_0_0.csv)

# print(location.address)
# coords, all_coords_list,strings = [] ,[],[]
# temp.append(point)

# break
# file[index].append(road)
# file[index].append(road)
# print([road]+temp)
# roads= {}
# vahicleRef = 'car 1'
# geolocator = Nominatim(user_agent="name_of_your_app")
# for point in zip(df['VehicleLocation.Latitude'], df['VehicleLocation.Longitude']):
#     location = geolocator.reverse(str(point))
#     nameOfStreet=(location.address).split(",")
#     first_value=nameOfStreet[0]
#     if first_value.isnumeric() :#or first_value.split("-")[0].isnumeric():
#       nameOfStreet.remove(first_value)
#     road=nameOfStreet[0],nameOfStreet[1],nameOfStreet[2]
#     if nameOfStreet[0].split("-")[0].isnumeric():
#       print(nameOfStreet)
#     if road not in roads:
#         roads[road] = [[point[0],point[1]]]
#     else:
#         roads[road]+=[[point[0],point[1]]]

# print(vehicles)

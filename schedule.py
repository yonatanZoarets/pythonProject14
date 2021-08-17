import csv
from datetime import datetime
import pytz
import requests
import pandas as pd
from org_des_time import json_it
import time


# def get_route_points(loc, des, key):
#     path = "https://api.tomtom.com/routing/1/calculateRoute/" + loc + ":" + des + "/json?&key=" + key
#     response = requests.get(path)
#     coords = []
#     print(response.json())
#     for item in response.json()["routes"][0]["legs"][0]["points"]:
#         coords.append([item["latitude"], item["longitude"]])
#     return coords


def read_traffic_point_api_data(key, point):
    path = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key=" + key + "&point=" + point
    return json_it(path)


# method of the coordinates

def right_time(timeZone, start_hour, end_hour, minutes):
    datetime_ABC = datetime.now(timeZone)
    return (end_hour > int(datetime_ABC.strftime("%H")) >= start_hour and int(
        datetime_ABC.strftime("%M")) % minutes == 0 and int(datetime_ABC.strftime("%S")) < 1)


def try_except_next(array, params, i, func):
    if i == len(array):
        return 0
    try:
        return func(array[i], params)
    except:
        return try_except_next(array, params, i + 1,func)


tz_SDN = pytz.timezone('Australia/Sydney')
datetime_SDN = datetime.now(tz_SDN)
df = pd.read_csv("roads_points.csv", error_bad_lines=False)
rec_file_name = "traffic_recordings" + datetime_SDN.strftime("%d_%m_%y") + ".csv"
f = open(rec_file_name, 'w', encoding="utf-8")
csv_f1 = csv.writer(f)
csv_f1.writerow(["road", "point", "traffic_percent", "hour", "currentSpeed", "freeFlowSpeed"])  # headline writing
f.close()
df = df.dropna()
if __name__ == '__main__':
    flag = 1
    keys = ["JFF6W4ZnqWnNSJarr8RsiTP4GeqCkJND", "fN1GFcLNR2Jd0oYxrQrhpqOTpeGAq9YM",
            "CwMysQRumeK8JZ9JG9WVdGIaixZY5ohR",
            "19TxtGiVQdQhRqPlVGhc2fzVI3WB3AUc"]

    while flag == 1:
        if right_time(timeZone=tz_SDN, start_hour=10, end_hour=4, minutes=30):
            for index, instance in df.iterrows():
                point = instance["point"]

                if index % 21 == 0:
                    data = try_except_next(keys, point, 0,func=read_traffic_point_api_data)
                    # data={'flowSegmentData': {'frc': 'FRC0', 'currentSpeed': 10, 'freeFlowSpeed': 59, 'currentTravelTime': 570, 'freeFlowTravelTime': 96, 'confidence': 1, 'roadClosure': False, 'coordinates': {'coordinate': [{'latitude': -33.872727730751926, 'longitude': 151.21079007114412}, {'latitude': -33.872695982967784, 'longitude': 151.21086614998643}, {'latitude': -33.87252104038269, 'longitude': 151.21135291884502}, {'latitude': -33.87248494506295, 'longitude': 151.21150197145766}, {'latitude': -33.87247158930629, 'longitude': 151.21155759973874}, {'latitude': -33.87244933967661, 'longitude': 151.2116337673492}, {'latitude': -33.87240663390553, 'longitude': 151.2117816054755}, {'latitude': -33.87237939577668, 'longitude': 151.2118858734977}, {'latitude': -33.87235169776127, 'longitude': 151.21197680984403}, {'latitude': -33.8722674247959, 'longitude': 151.21234560389422}, {'latitude': -33.8722674247959, 'longitude': 151.21276736680602}, {'latitude': -33.872270881074165, 'longitude': 151.21296376442774}, {'latitude': -33.872278329969454, 'longitude': 151.2131461854077}, {'latitude': -33.87228285191979, 'longitude': 151.21327238891666}, {'latitude': -33.87228787948754, 'longitude': 151.21336549826725}, {'latitude': -33.8722893193773, 'longitude': 151.21341369126844}, {'latitude': -33.87230008222368, 'longitude': 151.21359982496398}, {'latitude': -33.87232979520145, 'longitude': 151.21384718210237}, {'latitude': -33.87235941449953, 'longitude': 151.21403250057807}, {'latitude': -33.87241069900132, 'longitude': 151.21428039747792}, {'latitude': -33.87249496024069, 'longitude': 151.21468412036887}, {'latitude': -33.87254315711657, 'longitude': 151.21487910198783}, {'latitude': -33.872591138993165, 'longitude': 151.21504690716284}, {'latitude': -33.8726554439993, 'longitude': 151.21522264438818}, {'latitude': -33.87276398085769, 'longitude': 151.21572028055186}, {'latitude': -33.87278336135715, 'longitude': 151.21580564632256}, {'latitude': -33.87278721625854, 'longitude': 151.2158266596495}, {'latitude': -33.87291311245668, 'longitude': 151.21666763613314}, {'latitude': -33.87301538502339, 'longitude': 151.21715466731393}, {'latitude': -33.87306537517694, 'longitude': 151.21731993675212}, {'latitude': -33.87310779120327, 'longitude': 151.21747096149903}, {'latitude': -33.87315842511735, 'longitude': 151.2176395582427}, {'latitude': -33.87321489813423, 'longitude': 151.2177994844365}, {'latitude': -33.87326702556515, 'longitude': 151.21794381433853}, {'latitude': -33.87336870429911, 'longitude': 151.2181468640809}, {'latitude': -33.87351819052623, 'longitude': 151.2183838066358}, {'latitude': -33.873765455608826, 'longitude': 151.21864471511464}, {'latitude': -33.87385713580004, 'longitude': 151.21870593948364}, {'latitude': -33.873678856348874, 'longitude': 151.21855324593565}, {'latitude': -33.873491806336254, 'longitude': 151.2182913189887}, {'latitude': -33.87333480367917, 'longitude': 151.21795224655978}, {'latitude': -33.87327222233522, 'longitude': 151.2176403520686}, {'latitude': -33.87325107839433, 'longitude': 151.2174151766526}, {'latitude': -33.873249173891125, 'longitude': 151.21745378943842}, {'latitude': -33.873249173891125, 'longitude': 151.21749309295603}, {'latitude': -33.87326394398808, 'longitude': 151.21725954932276}, {'latitude': -33.873306252583355, 'longitude': 151.21710667683323}, {'latitude': -33.87331315022421, 'longitude': 151.21707905646775}, {'latitude': -33.873334046815046, 'longitude': 151.21701629897063}, {'latitude': -33.87330865393974, 'longitude': 151.21708641794226}, {'latitude': -33.87328812452931, 'longitude': 151.21714971681638}, {'latitude': -33.873320393183654, 'longitude': 151.2170575919992}, {'latitude': -33.87339154431845, 'longitude': 151.21690883629572}, {'latitude': -33.87353218971385, 'longitude': 151.21668151635652}, {'latitude': -33.873721518308315, 'longitude': 151.2164918652681}, {'latitude': -33.873865093225106, 'longitude': 151.21638939052156}, {'latitude': -33.87393611053878, 'longitude': 151.2163486358126}, {'latitude': -33.874071240280244, 'longitude': 151.21629610397088}, {'latitude': -33.87415251638997, 'longitude': 151.21627883800448}, {'latitude': -33.87419169213959, 'longitude': 151.2162724938416}, {'latitude': -33.87428679139681, 'longitude': 151.21626689793914}, {'latitude': -33.874307348828566, 'longitude': 151.21626848047947}, {'latitude': -33.874328996238475, 'longitude': 151.21626987568908}, {'latitude': -33.874435950623074, 'longitude': 151.21628969416696}, {'latitude': -33.87452054017463, 'longitude': 151.2163164176107}, {'latitude': -33.87463635890296, 'longitude': 151.21636144257712}, {'latitude': -33.87469295731385, 'longitude': 151.2163954388443}, {'latitude': -33.874832467729284, 'longitude': 151.21647509875828}, {'latitude': -33.875003329242, 'longitude': 151.2166458312924}, {'latitude': -33.87515877231727, 'longitude': 151.21682738120023}, {'latitude': -33.87528096455977, 'longitude': 151.21707045672065}, {'latitude': -33.87534358150693, 'longitude': 151.2172298330555}, {'latitude': -33.87536829333697, 'longitude': 151.2173292197637}, {'latitude': -33.87533241990706, 'longitude': 151.21718022709803}, {'latitude': -33.87548840185973, 'longitude': 151.21758903900388}, {'latitude': -33.87540028683983, 'longitude': 151.21797184514224}, {'latitude': -33.875404036953576, 'longitude': 151.21790328182936}, {'latitude': -33.87536440397833, 'longitude': 151.21809137626957}, {'latitude': -33.87532859852736, 'longitude': 151.21821157258728}, {'latitude': -33.87527236083689, 'longitude': 151.21835471204332}, {'latitude': -33.87515731669145, 'longitude': 151.2185675480169}, {'latitude': -33.875062370913895, 'longitude': 151.2186827525469}, {'latitude': -33.87497628147654, 'longitude': 151.2187828673289}, {'latitude': -33.87480661512966, 'longitude': 151.2189244112957}, {'latitude': -33.87468622332782, 'longitude': 151.21899471688772}, {'latitude': -33.874611451447244, 'longitude': 151.21903208050531}, {'latitude': -33.87451680560028, 'longitude': 151.2190605053467}, {'latitude': -33.87453268552753, 'longitude': 151.21905704093376}, {'latitude': -33.874614153907146, 'longitude': 151.21904102069374}, {'latitude': -33.87462857804768, 'longitude': 151.21903788334726}, {'latitude': -33.8746349911105, 'longitude': 151.21903715098153}, {'latitude': -33.87469967571818, 'longitude': 151.21902763538225}, {'latitude': -33.87474525811407, 'longitude': 151.2190209298597}, {'latitude': -33.874790840485616, 'longitude': 151.21901422433717}]}, '@version': 'traffic-service 4.1.022'}}
                    if data == 0:
                        flag = 4
                        print('breaked')
                        break
                    if data["flowSegmentData"]["freeFlowSpeed"] > 0:
                        traffic = 1 - data["flowSegmentData"]["currentSpeed"] / data["flowSegmentData"]["freeFlowSpeed"]
                    else:  # traffic calculated according to flow
                        traffic = 0
                    print(point, datetime_SDN.strftime("%H:%M"))  # traffic,
                    f = open(rec_file_name, 'a', encoding="utf-8", newline='')
                    csv_f1 = csv.writer(f)
                    csv_f1.writerow([instance["road"], point, 100 * traffic, datetime_SDN.strftime("%H:%M"),
                                     data["flowSegmentData"]["currentSpeed"], data["flowSegmentData"]["freeFlowSpeed"]])
            time.sleep(2)  # because the condition of second<1
        if datetime_SDN.strftime("%H") == '11':
            flag = 5

# str(instance["DestinationLat"]) + "," + str(instance["DestinationLong"])
# str(instance["VehicleLocation.Latitude"]) + "," + str(instance["VehicleLocation.Longitude"])
# if instance['road'] == 'Eastren distributor southbound':
#     loc = instance["origin"].replace(" ", "")
#     des = instance["destination"].replace(" ", "")
#     try:
#         coords = get_route_points(loc=loc, des=des, key="JFF6W4ZnqWnNSJarr8RsiTP4GeqCkJND")
#     except:
#         coords = get_route_points(loc=loc, des=des, key="fN1GFcLNR2Jd0oYxrQrhpqOTpeGAq9YM")
#     for coord in coords:
#         point = str(coord[0]) + "," + str(coord[1])

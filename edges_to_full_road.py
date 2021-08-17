import pandas as pd
import requests
import csv

# !pip install folium --upgrade

f = open('roads_length.csv', 'a', encoding="utf-8", newline='')
csv_f1 = csv.writer(f)
if __name__ == '__main__':
    df3 = pd.read_csv("edges.csv", error_bad_lines=False)
    df3 = df3.dropna()
    for index, instance in df3.iterrows():
        if instance['road'] + ".csv" in [
            '02396 - King Street Northbound.csv',
            '02396 - King Street Southbound.csv',
            '02062 - Enmore Road Northbound.csv',
            '02062 - Enmore Road Southbound.csv',
            '69087 - Prospect Highway Southbound.csv',
            '69087 - Prospect Highway Northbound.csv',
            '24008 - King Georges Road Northbound.csv',
            '24008 - King Georges Road Southbound.csv']:

            orig = instance['origin'].replace(" ", "")
            des = instance['destination'].replace(" ", "")
            print(instance['road'])

            path = "https://api.tomtom.com/routing/1/calculateRoute/" + orig + ":" + des + "/json?&key=CwMysQRumeK8JZ9JG9WVdGIaixZY5ohR"
            response = requests.get(path)
            coords1 = []
            for point in response.json()['routes'][0]['legs'][0]['points']:
                csv_f1.writerow([instance['road'], str(point['latitude']) + "," + str(point['longitude'])])

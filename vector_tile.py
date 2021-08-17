import requests
import csv
import pandas as pd
import random

from org_des_time import json_it

from schedule import read_traffic_point_api_data
keys = ["JFF6W4ZnqWnNSJarr8RsiTP4GeqCkJND", "fN1GFcLNR2Jd0oYxrQrhpqOTpeGAq9YM",
            "CwMysQRumeK8JZ9JG9WVdGIaixZY5ohR",
            "19TxtGiVQdQhRqPlVGhc2fzVI3WB3AUc"]
if __name__ == '__main__':
    data=res = requests.get("https://api.tomtom.com/map/4/tile/flow/absolute/17/64989/42178.pbf?key=JFF6W4ZnqWnNSJarr8RsiTP4GeqCkJND")
    print(data)
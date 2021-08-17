import os

import utm
import pandas as pd
import csv
from datetime import datetime as dt
import datetime
import requests as requests

# set working directory

if __name__ == '__main__':
    # os.chdir("/mydir")
    files = []
    directory = r'C:\Users\Ronit.Iconics\PycharmProjects\pythonProject10'  # taking all what we have' no need to match every time
    for filename in os.listdir(directory):

        if filename == "workbook.csv":
            files.append(filename)
            print(filename)
        # else:
        #     continue

    for filename in files:
        if "-" in filename:  # if it with number before the name - take only the name
            num = 8
        else:
            num = 0
        df = pd.read_csv(filename, error_bad_lines=False)
        df = df[
            ["Time",
             "VehicleID",
             "Speed",
             "Dist_front",
             "xCoord",
             "yCoord",
             "SectionID",
             "Avg_Sect_Speed",
             "Sect_Density"]]  # take only relevant columns
        new_files = []
        df.duplicated().value_counts()
        df = df.drop_duplicates()
        df = df.dropna()
        df.isnull().sum()
        for index, instance in df.iterrows():
            name = filename.replace(".csv", "1.csv")
            if name not in new_files:
                new_files.append(name)
                f = open(name, 'w', encoding="utf-8")  # "mydir/" +
                csv_f1 = csv.writer(f)
                csv_f1.writerow(
                    ["Time", "VehicleID", "Speed", "Dist_front", "xCoord", "yCoord", "SectionID", "Avg_Sect_Speed",
                     "Sect_Density"])
                f.close()

            f = open(name, 'a', encoding="utf-8")  # "mydir/" +
            csv_f1 = csv.writer(f)
            second_to_minute = instance["Time"] / 60
            second_to_minute = int(second_to_minute % 60)
            hour = int(instance["Time"] / 3600)
            hour=hour%24
            time=str(hour)+" : "+str(second_to_minute)
            latlon = utm.to_latlon(instance["xCoord"], instance["yCoord"], 31, 'U')
            csv_f1.writerow([time, instance["VehicleID"], instance["Speed"],  # taking the hour of the day
                             instance["Dist_front"], latlon[0], latlon[1],
                             instance["SectionID"], instance["Avg_Sect_Speed"], instance["Sect_Density"]])

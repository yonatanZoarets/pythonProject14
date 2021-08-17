import os
import glob
import pandas as pd
import csv
from datetime import datetime as dt

if __name__ == '__main__':
    # os.chdir("/mydir")
    files = []
    directory = r'C:\Users\Ronit.Iconics\PycharmProjects\pythonProject10'  # taking all what we have' no need to match every time

    for traffic_file_name in os.listdir(directory):
        if ('.csv' in traffic_file_name and 'traffic_recordings' in traffic_file_name
        and '_count' not in traffic_file_name):
            date = (traffic_file_name.replace('traffic_recordings', '').replace('.csv', '').replace('_', '/'))
            t=traffic_file_name.replace('.csv','')
            print(traffic_file_name,t)
            csvfile = open(t + '_count.csv', 'w', newline='')
            writer = csv.writer(csvfile)
            writer.writerow(['road','point','hour','traffic_percent','currentSpeed','freeFlowSpeed','num_Vehicles'])
            traffic_df = pd.read_csv(traffic_file_name, error_bad_lines=False)
            for count_file_name in os.listdir(directory + r'\mydir\recorded_dates'):
                if count_file_name != 'done':
                    count_df = pd.read_csv('mydir/recorded_dates/' + count_file_name, error_bad_lines=False)
                    for index, c_instance in count_df[11 > count_df['hour']][count_df['hour'] > 5].iterrows():
                        if (date == c_instance['date'] and 11 > c_instance['hour'] > 5):
                            # print("true",traffic_file_name,instance['date'],count_file_name)
                            for index, t_instance in traffic_df.iterrows():
                                hour = str(c_instance['hour'])
                                if len(hour) == 1:
                                    hour = '0' + hour
                                # print(t_instance['hour'][:2],hour,t_instance['hour'][:2]==hour)
                                if (t_instance['road'] == count_file_name[8:].replace('.csv', '') and t_instance[
                                                                                                          'hour'][
                                                                                                      :2] == hour):
                                    arr = [t_instance['road'], t_instance['point'],
                                           t_instance['hour'], t_instance['traffic_percent'], t_instance['currentSpeed']
                                        , t_instance['freeFlowSpeed'], c_instance['numVehicle']]
                                    writer.writerow(arr)

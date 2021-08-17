from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
import pandas as pd
import matplotlib as plt
import seaborn as sns


def monthsConvert(month):
    if month == 'January':
        return 1
    elif month == 'February':
        return 2
    elif month == 'March':
        return 3
    elif month == 'April':
        return 4
    elif month == 'May':
        return 5
    elif month == 'June':
        return 6
    elif month == 'July':
        return 7
    elif month == 'August':
        return 8
    elif month == 'September':
        return 9
    elif month == 'October':
        return 10
    elif month == 'November':
        return 11
    elif month == 'December':
        return 12
    else:
        return -1


def date_convert(date):
    date_splited = date.split("/")
    appended_parts_date = ""
    for part in date_splited:
        appended_parts_date = appended_parts_date + part
    return int(appended_parts_date)


if __name__ == '__main__':
    # vehicleDataSet=pd.read_csv("Western Distributor Westbound.csv")
    # vehicleDataSet=pd.read_csv("Eastern Distributor Southbound.csv")
    vehicleDataSet = pd.read_csv("mydir/Eastern Distributor Northbound.csv")
    vehicleDataSet.head()
    vehicleDataSet.dropna()
    f = open("hii.txt", 'w')
    f2 = open("hii2.txt", 'w')
    f5 = open("countVehError.txt", 'w')
    f6 = open("countVeh.txt", 'w')
    for i, row in vehicleDataSet.iterrows():
        value_month = row['month']
        value_date = row['date']
        print(value_date,value_month)
        conv_month = monthsConvert(value_month)
        conv_date = date_convert(value_date)
        vehicleDataSet.at[i, 'month'] = conv_month
        vehicleDataSet.at[i, 'date'] = conv_date
        f.write(str(conv_month) + '\n')
        f2.write(str(conv_date) + '\n')
        if math.isnan(row['numVehicle']):
            f5.write(str(row['numVehicle']) + str(i) + '\n')
        f6.write(str(row['numVehicle']) + '\n')
    f.close()
    f2.close()
    f5.close()
    f6.close()
    print(vehicleDataSet.isnull().any())

    vehicleDataSet = vehicleDataSet[vehicleDataSet['numVehicle'].notna()]
    X = vehicleDataSet.drop(['numVehicle'], axis=1)
    X = X.values
    y = vehicleDataSet["numVehicle"]
    y = y.values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=12345)

f3 = open("hd.txt", 'w')
f4 = open("he.txt", 'w')
for k in X_train:
    f3.write(str(k) + '\n')
for n in y_train:
    f4.write(str(n) + '\n')
# X_train=np.array(X_train,dtype=float)
# y_train=np.array(y_train,dtype=float)
f3.close()
f4.close()
# print(np.any(np.isnan(X_train))) #and gets False
# print(np.all(np.isfinite(X_train))) #and gets True
# print(X_train) #and gets False

knn_model = KNeighborsRegressor(n_neighbors=7)
knn_model.fit(X_train, y_train)
train_preds = knn_model.predict(X_train)
mse = mean_squared_error(y_train, train_preds)
rmse = sqrt(mse)
print(rmse)
test_preds = knn_model.predict(X_test)
mse = mean_squared_error(y_test, test_preds)
rmse = sqrt(mse)
print(rmse)

cmap = sns.cubehelix_palette(as_cmap=True)
f, ax = plt.subplots()
points = ax.scatter(X_test[:, 3], X_test[:, 4], c=test_preds, s=50, cmap=cmap)
f.colorbar(points)
plt.show()

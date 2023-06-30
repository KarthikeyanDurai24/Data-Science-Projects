# -*- coding: utf-8 -*-
"""Store Sales Analysis and Predictive Models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l4dhwGBpx4VvwDbbnkgCbdY8rKBMCi-O

Importing required libraries
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

"""Reading CSV file"""

stores_df = pd.read_csv("sample_data/Stores.csv")
stores_df = stores_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

stores_df.columns

"""Removing spaces from column names"""

stores_df.columns = stores_df.columns.str.strip()
stores_df.columns

"""Checking for null values and duplicates"""

stores_df.info()

stores_df.isnull().sum()

stores_df.duplicated().sum()

"""Getting details about store with maximum sales"""

stores_df.iloc[stores_df["Store_Sales"].idxmax()]

"""Getting details about store with minimum sales"""

stores_df.iloc[stores_df["Store_Sales"].idxmin()]

"""Removing StoreID column from the dataframe"""

stores_df.drop("Store ID", inplace = True, axis = "columns")

"""Descriptive stats for each variable"""

stores_df.describe()

"""Correlation of store sales with other variables"""

stores_df.corr()["Store_Sales"].sort_values()

"""Paired plot"""

sns.pairplot(stores_df)
plt.show()

"""Distribution of store sales"""

sns.displot(data = stores_df, x = "Store_Sales", bins = 50)
plt.show()

"""Identifying and removing outliers"""

IQR_Daily_Customer_Count = 970 - 600
upper_limit = 970 + 1.5 * IQR_Daily_Customer_Count
lower_limit = 600 - 1.5 * IQR_Daily_Customer_Count
stores_df.loc[stores_df["Daily_Customer_Count"] > upper_limit] = np.nan
stores_df.loc[stores_df["Daily_Customer_Count"] < lower_limit] = np.nan

stores_df.isnull().sum()

stores_df.dropna(inplace = True)

"""Creating x and y variables for creating machine learning models"""

x = stores_df[["Store_Area", "Items_Available", "Daily_Customer_Count"]]
y = stores_df["Store_Sales"]

"""Splitting dataset for training and testing the machine learning models"""

from sklearn.model_selection import train_test_split as tts
x_train, x_test, y_train, y_test = tts(x, y, random_state = 42, test_size = 0.3)

"""Standardizing x varibles in both training and testing datasets"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_x_train = scaler.fit_transform(x_train)
scaled_x_test = scaler.fit_transform(x_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error

"""Creating function to calculate errors of machine learning models"""

def model_metrics(predictions):
  mae = mean_absolute_error(y_test, predictions)
  mse = mean_squared_error(y_test, predictions)
  rmse = np.sqrt(mse)
  print(f"Mean absolute error of model: {mae}")
  print(f"Mean squared error of model: {mse}")
  print(f"Root mean squared error of model: {rmse}")

"""Creating linear regression model"""

from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(scaled_x_train, y_train)
y_predictionlr = lr.predict(scaled_x_test)
model_metrics(y_predictionlr)

"""Creating support vector regression model"""

from sklearn.svm import SVR
svr = SVR()
svr.fit(scaled_x_train, y_train)
y_predictionsvr = svr.predict(scaled_x_test)
model_metrics(y_predictionsvr)

"""Using GridSearchCV to find the best params for SVR model"""

from sklearn.model_selection import GridSearchCV
svrmodel = SVR()
param_gridsvr = {"C":[0.001, 0.01, 0.1, 0.5], "kernel":["linear", "rbf", "poly"], "gamma":["auto", "scale"], "degree":[2, 3, 4, 5]}
gridsvr = GridSearchCV(svrmodel, param_gridsvr)
gridsvr.fit(scaled_x_train, y_train)

print(f"Best parameters of SVR model is {gridsvr.best_params_}")

preds_gridsvr = gridsvr.predict(scaled_x_test)
model_metrics(preds_gridsvr)

"""Creating random forest regression model"""

from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor()
rfr.fit(scaled_x_train, y_train)
pred_rfr = rfr.predict(scaled_x_test)
model_metrics(pred_rfr)

"""Using GridSearchCV to find the best params for random forest regression model"""

rfrmodel = RandomForestRegressor(max_features = 1.0)
params_gridrfr = {"bootstrap":[True], "max_depth":[5, 10, 15], "n_estimators":[2, 3, 4, 5, 6]}
gridrfr = GridSearchCV(rfrmodel, params_gridrfr)
gridrfr.fit(scaled_x_train, y_train)

print(f"Best parameters of random forest regression model is {gridrfr.best_params_}")

preds_gridrfr = gridrfr.predict(scaled_x_test)
model_metrics(preds_gridrfr)
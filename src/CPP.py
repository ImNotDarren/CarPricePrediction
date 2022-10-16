#!/usr/bin/python3
import sys
import pandas as pd
import pickle
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from get_df import get_df
from set_x import set_X
from copy import deepcopy
import datetime

def main():
    # get web url
    url = sys.argv[1]
    year = int(sys.argv[2])
    curr_year = datetime.datetime.now().year

    if year < curr_year:
        print('Please input a future year!')
        exit()

    # load the model from pickle file
    with open('../models/ridge_model.pkl', 'rb') as f:
        lr = pickle.load(f)

    # test_df = pd.read_csv('data/test_df.csv', index_col=0)
    df = get_df(url, year)

    if year == curr_year:
        print('$' + str(round(df.price, 2)))

    df_train = get_df(url, curr_year)

    X = set_X(df)
    X_curr = set_X(df_train)
    y_curr = df.price
    # X = X.iloc[0].values.flatten().tolist()

    # lr.fit(X_curr, y_curr)

    y = lr.predict(X)
    print('$' + str(round(y[0], 2)))

if __name__ == '__main__':
    main()
#!/usr/bin/python3
import sys
import pandas as pd
import pickle
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from get_df import get_df
from set_x import set_X

def main():
    # get web url
    url = sys.argv[1]
    year = sys.argv[2]

    # load the model from pickle file
    with open('models/lasso_model.pkl', 'rb') as f:
        lasso = pickle.load(f)

    # test_df = pd.read_csv('data/test_df.csv', index_col=0)
    df = get_df(url, year)
    X = set_X(df)
    # X = X.iloc[0].values.flatten().tolist()
    y = lasso.predict(X)
    print('$' + str(round(y[0], 2)))

if __name__ == '__main__':
    main()
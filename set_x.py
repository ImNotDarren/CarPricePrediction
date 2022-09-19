import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import pickle

def set_X(df):
    test_df = pd.read_csv('data/test_df.csv', index_col=0)
    train_df = pd.read_csv('data/train_df.csv', index_col=0)

    # scaler = StandardScaler()
    # train_X = train_df.drop(columns=['price'])
    # scaler.fit(train_X)
    with open('models/scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)

    X = df.drop(columns=['price'], axis=1)
    X_scaled = scaler.transform(X)
    poly = PolynomialFeatures(degree=2)
    X_scaled_poly = poly.fit_transform(X_scaled)
    return X_scaled_poly
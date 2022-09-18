import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

def set_X(df):
    test_df = pd.read_csv('data/test_df.csv', index_col=0)

    X = df.drop(columns=['price'], axis=1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    poly = PolynomialFeatures(degree=2)
    X_scaled_poly = poly.fit_transform(X_scaled)
    return X_scaled_poly
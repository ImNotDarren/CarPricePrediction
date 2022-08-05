# Car Price Prediction (in progress)

## Table of Contents
- [Abstract](#link-part-1)
- [Design](#link-part-2)
- [Data](#link-part-3)
- [Algorithm](#link-part-4)
- [Tools](#link-part-5)
- [Communication](#link-part-6)
- [**How to run**](#link-part-7)

## <a name="link-part-1">Abstract</a>

The goal of this project was to build a model using used car
infomation on [cars.com](https://www.cars.com) to predict used
car prices. Based on the prices we have, we may be able to predict
car prices in a few years to make a better choice when to get a
used car.

## <a name="link-part-2">Design</a>

Nowadays, because of the COVID situation, used cars are getting more and more expensive.
People are usually confused if they should get a car now or if they should wait. Hence,
more and more people need a car price predicting tool to predict the price of used cars
to avoid spending too much money.

## <a name="link-part-3">Data</a>

The dataset I used is scraped from [cars.com](https://www.cars.com)
containing 1193 rows of data.

Each row will represent one used car that is on sale on [cars.com](https://www.cars.com).
The information includes year, module, make, price, mileage, color,
drivetrain, mpg, fuel type, transmission type, and engine. 

## <a name="link-part-4">Algorithm</a>



## <a name="link-part-5">Tools</a>

* **Pandas** for exploratory data analysis
* **Matplotlib** and **Seaborn** for plotting
* **Beautifulsoup** and **Requests** for web scraping
* **Scikit Learn** and **Statsmodels** for building regression model

## <a name="link-part-6">Communication</a>

* [Linear regression model](/models/linear_model_pkl) test:

<img src="images/linear_regression_test.png" alt="drawing" width="500"/>

**Train $R^2$ score: 0.940**

**Test $R^2$ score: 0.918**

* [Lasso regression model](/models/lasso_model_pkl) test: (Solved overfitting)

<img src="images/lasso_regression_test.png" alt="drawing" width="500"/>

**Train $R^2$ score: 0.935**

**Test $R^2$ score: 0.934**

The project proposal is shown [here](/documents/proposal.md).

MVP documentation is shown [here](/documents/MVP.md).

The slides to the project are not here yet.

## <a name="link-part-7">How to run</a>

**To get data:**

* Use [this dataset](/data/car_info.csv) or scrape [cars.com](https://www.cars.com) by running [web_scraping](/web_scraping.ipynb)

**To train the model:**

* Run [car_price_prediction](/car_price_prediction.ipynb) in Jupyter Notebook

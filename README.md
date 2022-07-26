# Used Car Price Predicting Tool
## Table of Contents
- [Abstract](#link-part-1)
- [Design](#link-part-2)
- [Data](#link-part-3)
- [Algorithm](#link-part-4)
- [Tools](#link-part-5)
- [Communication](#link-part-6)
- [**How to run**](#link-part-7)

## <a name="link-part-1">Abstract</a>

The goal of this project was to build a regression model to predict used
car prices. I worked with data scraped from [cars.com](https://www.cars.com)
to achieve training the model. Based on the prices we have, we are able to
predict car prices in a few years to make a better choice on when to get which
used cars.

## <a name="link-part-2">Design</a>

Nowadays, because of the COVID situation, used cars are getting more and more expensive.
People are usually confused if they should get a car now or if they should wait. Hence,
more and more people need a car price predicting tool to predict the price of used cars
to avoid spending too much money.

For car owners, they are also able to predict their cars' prices in a few years using
this model, which can help them decide when to sell their car and get a car at the same
time with the best deal.

## <a name="link-part-3">Data</a>

The dataset I used is scraped from [cars.com](https://www.cars.com)
containing 4161 rows of data.

<div align="center">
    <img width="999" alt="Screen Shot 2022-12-17 at 15 26 54" src="https://user-images.githubusercontent.com/80400820/208264920-f4fa3a06-6c7e-4efc-8568-46dfca3c6143.png">
</div>


Each row will represent one used car that is on sale on [cars.com](https://www.cars.com).
Features includes year, module, make, price, mileage, drivetrain, mpg, fuel type, transmission
type, engine and zip code. Oneowner and personal_use don't have a big influence on the
result, hence they're not used for model building.

## <a name="link-part-4">Algorithm</a>

**Web Scraping**

1. Getting used car list url 120 pages.
3. Scraping name, price, mileage information from every page.
4. Scraping every used car's individual page link from every page.
5. Scraping each used car's page to get drivetrain, mpg, fuel type, transmission and engine information.
6. Saving the information in a dataframe and then saving into a csv file for modeling.

**Feature Engineering**

1. Converting fuel type, car make and model, transmission into dummies.
2. Converting MPG into int type by add lowest mpg to highest mpg.
3. Breaking down car engines into liters and volts.
4. Breaking down drivetrain into 2-wheel-drive and 4-wheel-drive.
5. Get population by zip code.

**Models**

Firstly, I built a baseline model with linear regression. It has a 0.847
accuracy on validation set and only 0.435 accuracy on test set which shows
a huge overfitting problem. 

In order to solve this problem, ridge regression is used here and massively
reduced overfitting and increased accuracy on test set.

<div align="center">
    <img src="imgs/ridge.png" style="width: 400px;" />
</div>

Ridge regression is a model tuning method that is used to analyse any data
that suffers from multicollinearity. This method performs L2 regularization.

The cost function for ridge regression:

```
Min(||Y – X(theta)||^2 + λ||theta||^2)
```

Lambda is the penalty term. λ given here is denoted by an alpha parameter
in the ridge function. So, by changing the values of alpha, we are controlling
the penalty term. The higher the values of alpha, the bigger is the penalty
and therefore the magnitude of coefficients is reduced.

Ploynomial features are also included in training which massively increased
the performance.

Now the train $R^2$ value and test $R^2$ value are both around 0.80.

**Model Evaluation**

The entire training dataset of 4161 records was split into 80/20 train vs. holdout, and all
scores reported below were validated from both train dataset and holdout dataset.

**Final Score: 0.784**

## <a name="link-part-5">Tools</a>

* **Pandas** for exploratory data analysis
* **Matplotlib** and **Seaborn** for plotting
* **Beautifulsoup** and **Requests** for web scraping
* **Scikit Learn** and **Statsmodels** for building regression model
* **Pickle** for saving regression models in a pickle file

## <a name="link-part-6">Communication</a>

* **Linear regression model** test:

    Train $R^2$ score: 0.847

    Test $R^2$ score: 0.435

* **[Ridge regression model](/models/ridge_model.pkl)** test:

    Train $R^2$ score: 0.823

    Test $R^2$ score: **0.784**
    
* **Predicting tool:**

I also built a tool that takes a cars.com webpage and year as input, and it will output
the predicted price of the vehicle in that year.

Here are some examples:

For this 2021 Cadillac XT6 Sport AWD, in 2022, its price is $53,852.

<div align="center">
    <img width="519" alt="Screen Shot 2022-12-16 at 23 08 53" src="https://user-images.githubusercontent.com/80400820/208224181-be3a5a9e-4d4b-4d99-ba61-0e0fdd2b6111.png" style="width: 400px;">
</div>

However, if you wait till 2025, this vehicle's price should only be $39,607.

<div align="center">
    <img width="568" alt="example1" src="https://user-images.githubusercontent.com/80400820/208223970-882b7c80-9a71-4d01-bd6b-4963e0d0f4ef.png">
</div>

And for this 2017 Cadillac XT5 Premium Luxury, in 2022, its price is $25,950.

<div align="center">
    <img width="532" alt="Screen Shot 2022-12-16 at 23 17 23" src="https://user-images.githubusercontent.com/80400820/208224435-73ce6a15-7f71-49f4-9fc9-a92f69b07fa5.png" style="width: 400px;">
</div>

However, in 2026, the price would likely drop to $11,450.

<div align="center">
    <img width="596" alt="example2" src="https://user-images.githubusercontent.com/80400820/208224409-74c37c80-1699-48c6-8c12-004d094923db.png">
</div>


The project proposal is shown [here](/documents/proposal.md).

## <a name="link-part-7">How to run</a>

**To get predicted price:**

cd into [src](/src):
```
cd src
```

Run the predictor by:
```
python3 CPP.py $(car_webpage_link) $(year)
```

For example:
```
python3 CPP.py https://www.cars.com/vehicledetail/ff495aa2-9589-498a-8894-553fcde8f321/ 2026
```

**To get data:**

* Fine the data [here](/data) or scrape [cars.com](https://www.cars.com)
by running [web_scraping](/web_scraping.ipynb).

**To train the model:**

* Run [car_price_prediction](/car_price_prediction.ipynb) in Jupyter Notebook.

* The saved model is [here](/models/ridge_model.pkl).

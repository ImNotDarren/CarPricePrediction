import sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import pickle
import re
from uszipcode import SearchEngine

def is_gas(row):
    regex1 = re.compile('.*Gas.*')
    regex2 = re.compile('.*Flex.*')
    if regex1.match(row.fuel_type) or \
            regex2.match(row.fuel_type) or \
            row.fuel_type == 'Hybrid ':
        return 1
    else:
        return 0

def is_diesel(row):
    regex1 = re.compile('Diesel.*')
    regex2 = re.compile('.*Flex Fuel.*')
    if regex1.match(row.fuel_type) or \
            regex2.match(row.fuel_type):
        return 1
    else:
        return 0

def is_electric(row):
    regex = re.compile('.*Electric.*')
    if regex.match(row.fuel_type) or \
            row.fuel_type == 'Hybrid ':
        return 1
    else:
        return 0

def get_year_make_model(row):
    i = row['name']
    w = i.split()
    return w

def get_low_mpg(row):
    if row.mpg == '–' or row.mpg == 'None':
        return 25.4
    else:
        i = row.mpg.find('–')
        if i != -1:
            return row.mpg[0:i]
        else:
            return row.mpg

def get_high_mpg(row):
    if row.mpg == '–' or row.mpg == 'None':
        return 25.4
    else:
        i = row.mpg.find('–')
        if i != -1:
            return row.mpg[i+1:]
        else:
            return row.mpg

def is_auto(row):
    regex = re.compile('.*([A|a]uto|A/T|Dual Shift).*')
    if regex.match(row.transmission):
        return 1
    else:
        return 0

def is_cvt(row):
    regex = re.compile('.*(CVT|Variable).*')
    if regex.match(row.transmission):
        return 1
    else:
        return 0

def is_manual(row):
    regex = re.compile('.*(Manual|M/T).*')
    if regex.match(row.transmission):
        return 1
    else:
        return 0

def get_speed(row):
    tmp = row.transmission
    tmp = re.sub('[^0-9]', '', tmp)
    if tmp == '':
        return 6
    else:
        return int(tmp)

def get_L(row):
    i = row.engine.find('L')
    if i == -1:
        return 0
    else:
        return float(row.engine[i-3:i])

def get_V(row):
    i = row.engine
    a = re.compile('.*16V.*')
    b = re.compile('.*24V.*')
    c = re.compile('.*32V.*')
    d = re.compile('.*48V.*')
    e = re.compile('.*12V.*')
    if a.match(i):
        return 16
    elif b.match(i):
        return 24
    elif c.match(i):
        return 32
    elif d.match(i):
        return 48
    elif e.match(i):
        return 12
    else:
        return 24

def get_drivetrain(row):
    i = row.drivetrain
    four = re.compile('.*(Front|Rear|FWD).*')
    two = re.compile('.*(All|Four|4WD|AWD).*')
    if four.match(i):
        return 4
    elif two.match(i):
        return 2
    else:
        return 3

def get_major_city(row):
    engine = SearchEngine()
    zipcode = engine.by_zipcode(row.zipcode)
    return zipcode.major_city

def get_population(row):
    engine = SearchEngine()
    zipcode = engine.by_zipcode(row.zipcode)
    return zipcode.population



def get_df(url, year):
    column_names = ['name', 'price', 'mileage', 'drivetrain', \
                    'mpg', 'fuel_type', 'transmission', 'engine', 'zipcode', 'oneowner', 'personal_use']
    df = pd.DataFrame(columns=column_names)
    res = requests.get(url).text
    soup = bs(res, features="html.parser")

    # get name
    name = soup.find(name='h1', attrs={'class': 'listing-title'}).text
    df['name'] = [name]

    # get price
    price = soup.find(name='span', attrs={'class': 'primary-price'}).text
    pr_list = re.findall(r'\d+', price)
    price = ''.join(pr_list)
    df['price'] = [price]

    # get mileage
    mileage = soup.find(name='div', attrs={'class': 'listing-mileage'}).text
    mi_list = re.findall(r'\d+', mileage)
    mileage = ''.join(mi_list)
    df['mileage'] = [mileage]

    # get drivetrain
    dt = soup.find(name='dt', text='Drivetrain')
    if dt == None:
        df['drivetrain'] = ['']
    else:
        dt = dt.next.next.next.text
        df['drivetrain'] = [dt]

    # get mpg
    mpg = soup.find(name='a', attrs={'class': 'sds-tooltip__trigger'})
    if mpg != None:
        mpg = mpg.previous_sibling.previous_sibling.text
        df['mpg'] = [mpg]
    else:
        df['mpg'] = ['None']

    # get fuel type
    fuel_type = soup.find(name='dt', text='Fuel type')
    if fuel_type == None:
        df['fuel_type'] = ['']
    else:
        fuel_type = fuel_type.next.next.next.text
        df['fuel_type'] = [fuel_type]

    # get transmission
    transmission = soup.find(name='dt', text='Transmission')
    if transmission == None:
        df['transmission'] = ['']
    else:
        transmission = transmission.next.next.next.text
        df['transmission'] = [transmission]

    # get engine
    engine = soup.find(name='dt', text='Engine')
    if engine == None:
        df['engine'] = ['']
    else:
        engine = engine.next.next.next.text
        df['engine'] = [engine]

    # get zip code
    zipcode = soup.find(name='div', attrs={'class': 'dealer-address'})
    if zipcode == None:
        df['zipcode'] = [0]
    else:
        zipcode = zipcode.text
        df['zipcode'] = [zipcode[-5:]]

    # get one_owner
    oneowner = soup.find(name='dd', attrs={'data-qa': 'one-owner-value'})
    if oneowner == None:
        oneowner = 3
    else:
        if oneowner.text == 'Yes':
            oneowner = 1
        else:
            oneowner = 0
    df['oneowner'] = [oneowner]

    # adding personal use
    personal_use = soup.find(name='dd', attrs={'data-qa': 'personal-use-value'})
    if personal_use == None:
        personal_use = 3
    else:
        if personal_use.text == 'Yes':
            personal_use = 1
        else:
            personal_use = 0
    df['personal_use'] = [personal_use]

    # convert df to standerd format
    df['age'] = df.apply(lambda row: int(year) - int(get_year_make_model(row)[0]), axis=1) \
        .astype('int')
    df['make_model'] = df.apply(lambda row: get_year_make_model(row)[1] + get_year_make_model(row)[2], axis=1)
    df['mpg'] = df.apply(lambda row: int(get_low_mpg(row)) + int(get_high_mpg(row)), axis=1).astype('int')
    df['is_auto'] = df.apply(lambda row: is_auto(row), axis=1)
    df['is_cvt'] = df.apply(lambda row: is_cvt(row), axis=1)
    df['is_manual'] = df.apply(lambda row: is_manual(row), axis=1)
    df['speed'] = df.apply(lambda row: get_speed(row), axis=1)
    df['engine_L'] = df.apply(lambda row: get_L(row), axis=1).astype('float')
    df['engine_V'] = df.apply(lambda row: get_V(row), axis=1).astype('float')
    df['drivetrain'] = df.apply(lambda row: get_drivetrain(row), axis=1)
    df['major_city'] = df.apply(lambda row: get_major_city(row), axis=1)
    df['population'] = df.apply(lambda row: get_population(row), axis=1)
    df = pd.get_dummies(df, columns=['make_model'], \
                        prefix='mm', prefix_sep='_')
    df = pd.get_dummies(df, columns=['drivetrain'], \
                        prefix='dt', prefix_sep='_')
    df = pd.get_dummies(df, columns=['major_city'], \
                        prefix='is_in', prefix_sep='_')
    df = df.drop(columns= \
                     ['name', 'mpg', 'fuel_type', 'transmission', 'engine', 'personal_use'])

    train_df = pd.read_csv('data/train_df.csv', index_col=0)

    new_df = pd.DataFrame(columns=train_df.columns)
    for c in train_df.columns:
        if c in df.columns:
            new_df[c] = df[c]
        else:
            new_df[c] = [0]
    return new_df


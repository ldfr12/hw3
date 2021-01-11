import json
import requests

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2, linregress
from scipy.optimize import minimize
from numpy import linalg as LA

import stream_functions
importlib.reload(stream_functions)
import stream_classes
importlib.reload(stream_classes)


'''
HOMEWORK 3.

Here you will need to create 2 tables.

### Table 1 ###

The first table is df_top_correlations. Given a portfolio (it will be a single 
ric, for example SAN.MC) and a benchmark (^STOXX as default), you will compute a 
table for correlations and betas of all names in the universe vs that portfolio. 

The output will be a table with fixed columns:
[ric, correlation, abs_correlation, beta].

The size of the table is equal to the size of the universe MINUS one:
    - we need to exclude the portfolio (say SAN.MC) from the universe of rics
    - we do not want a correlation of 1 of the portfolio vs itself
    
The correlation will that of SAN.MC vs each element of the universe.
The abs_correlation is the absolute value of the correlation.
The beta is vs the given benchmark (here ^STOXX)

### Table 2 ###

The second table df_hedges will compute the best hedges for different parameters. 

The columns are fixed:
[number_hedges, epsilon, portfolio_delta, portfolio_beta, hedge_delta, hedge_beta]

number_hedges is a list of the number of hedges we want to have 
    e.g. number_hedges = [1, 2, 3, 4, 5]
epsilon is the regularisation parameter in hedge_manager.compute_numerical 
    e.g. epsilons = [0, 0.001, 0.01, 0.1]
portfolio_delta is the input given, in mn USD
portfolio_beta will be in mn USD, computed using the given benchmark
hedge_delta will be the delta of the optimal hedge in mn USD
hedge_beta will be the beta vs benchmark of the optimal hedge in mn USD

The size of the second table is len(number_hedges) * len(epsilons)


'''
def create_dataframe_top_correlations(portfolio, benchmark, universe):
    df = pd.DataFrame()
    # columns = security + list of metrics
    # number of rows = nb_rows

    # your code comes here
    columns = ['ric','correlation','abs_correlation','beta']
    
    for i in universe:
        if portfolio == i:
            universe.remove(i)
    
    index = list(range(len(universe)))
    df = pd.DataFrame(index = index, columns = columns)

    for i in universe:
        n = universe.index(i)
        df.iloc[n, df.columns.get_loc('ric')] = i
        
        capm = stream_classes.capm_manager(portfolio, i)
        b = stream_classes.capm_manager(benchmark, i)
        capm.load_timeseries()
        capm.compute()
        corr = capm.correlation
        b.load_timeseries()
        b.compute()
        beta = b.beta
        
        df.iloc[n, df.columns.get_loc('correlation')] = corr
        df.iloc[n, df.columns.get_loc('abs_correlation')] = abs(corr)
        df.iloc[n, df.columns.get_loc('beta')] = beta
    
    df.sort_values(by = 'abs_correlation', ascending= False, inplace= True, ignore_index = True)

    return df


def create_dataframe_hedges(portfolio, benchmark, delta, df_top_correlations, numbers_hedges, epsilons):
    df = pd.DataFrame()
    # columns = security + list of metrics
    # number of rows = nb_rows

    # your code comes here
    n_hedges = []
    n_epsilon = []
    n_port_delta = []
    n_port_beta = []
    n_hed_delta = []
    n_hed_beta = []
    
    for epsilon in epsilons:
        for number_hedge in numbers_hedges:
            universe = df.iloc[:,0]
            hedge_rics = universe.iloc[0:number_hedge]
            hedger = stream_classes.hedge_manager(benchmark, portfolio, hedge_rics, delta)
            hedger.load_inputs()
            hedger.compute_numerical(epsilon)
            n_hedges.append(number_hedge)
            n_epsilon.append(epsilon)
            n_port_delta.append(hedger.delta)
            n_port_beta.append(hedger.beta_usd)
            n_hed_delta.append(hedger.hedge_delta)
            n_hed_beta.append(hedger.hedge_beta_usd)
        
        dictionary = {'number_hedges': n_hedges,\
                      'epsilon': n_epsilon,\
                      'portfolio_delta':n_port_delta,\
                      'portfolio_beta': n_port_beta,\
                      'hedge_delta': n_hed_delta,\
                      'hedge_beta': n_hed_beta}
        
        df_hedges = pd.DataFrame(dictionary)
    df_hedges = df_hedges.round(8)

    return df_hedges


# NO MODIFICAR
def settings(numero_cuenta):

    r = requests.post('http://meva1.sytes.net/ulmo/dataHW3.php',  {'numero_cuenta':numero_cuenta} )

    data = json.loads(r.text)
    portfolio = data['portfolio']
    benchmark = data['benchmark']
    delta = data['delta']
    epsilons = data['epsilons']
    numbers_hedges = data['numbers_hedges']
    universe = data['universe']


    df_top_correlations_student = create_dataframe_top_correlations(
        portfolio, benchmark, universe)
    df_hedges_student = create_dataframe_hedges(
        portfolio, benchmark, delta, df_top_correlations_student, numbers_hedges, epsilons)

    print('--------------------------------------------------------')

    data_json = df_top_correlations_student.to_json() 
    data_json2 = df_hedges_student.to_json() 
    payload = {'json_data': data_json, 'json_data2':data_json2 ,'numero_cuenta': numero_cuenta}
    r = requests.post('http://meva.sytes.net/ulmo/evaluateHW3.php', json=payload)
    print(r.text)
    return r.text

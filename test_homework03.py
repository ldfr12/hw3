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
import time

import stream_functions
importlib.reload(stream_functions)
import stream_classes
importlib.reload(stream_classes)


import homework_03 as hw;

'''
NO OLVIDES PONER TU NUMERO DE CUENTA!
'''
numero_cuenta = 313198799

def test_1():
    time.sleep(2)
    print(".-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    result = hw.settings(numero_cuenta)[0:4]
    if result == "Data":
        print("Tu dataframe esta mal construido")
        result = "Dataframe Invalido!"
    if result == "El s":
        print("El servidor no esta respondiendo, contacta al ayudante")
        result = "El servidor no responde"
    else:
        print("En el primer test obtuviste", result)
    time.sleep(2)
    assert float(result) == 10.0


def test_2():
    time.sleep(2)
    print(".-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    result = hw.settings(numero_cuenta)[0:4]
    if result == "Data":
        print("Tu dataframe esta mal construido")
        result = "Dataframe Invalido!"
    if result == "El s":
        print("El servidor no esta respondiendo, contacta al ayudante")
        result = "El servidor no responde"
    else:
        print("En el segundo test obtuviste", result)
    time.sleep(2)
    assert float(result) == 10.0


def test_3():
    time.sleep(2)
    print(".-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    result = hw.settings(numero_cuenta)[0:4]
    if result == "Data":
        print("Tu dataframe esta mal construido")
        result = "Dataframe Invalido!"
    if result == "El s":
        print("El servidor no esta respondiendo, contacta al ayudante")
        result = "El servidor no responde"
    else:
        print("En el tercer test obtuviste", result)
    time.sleep(2)
    assert float(result) == 10.0

import tensorflow as tf
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def predict(w, b, t):
        
    return w * t + b

def change_time(time, term):    # term은 몇 시간 간격으로 측정했는지. 1시간이면 term = 1, 30분이면 term = 0.5 / time은 예측하고 싶은 시간

    return int(time / term)

dfParm = pd.read_csv("result.csv", header = 0)
w_am = dfParm['w'][0]
b_am = dfParm['b'][0]
w_pm = dfParm['w'][1]
b_pm = dfParm['b'][1]

pre_time = int(input("예측할 시간을 입력하세요 (0 ~ 23): "))
t = change_time(pre_time, 2)
print("t: " + str(t))

if 0 <= pre_time < 12:
    predic_result = predict(w_am,b_am,t)
elif 12 <= pre_time < 24:
    predic_result = predict(w_pm,b_pm,t)

print("예측 습도: " + str(predic_result))

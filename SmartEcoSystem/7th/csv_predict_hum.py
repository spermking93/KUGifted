import tensorflow as tf
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# predict 함수를 정의합니다.
def predict(w, b, t):
# 예측하고 싶은 시간의 값을 return합니다.        
    return w * t + b

# change_time 함수를 정의합니다.
# term은 몇 시간 간격으로 측정했는지. 1시간이면 term = 1, 30분이면 term = 0.5 / time은 예측하고 싶은 시간
def change_time(time, term):    
    # 예측하고 싶은 시간을 x축 위의 값으로 바꿔줍니다.
    return int(time / term)

# result.csv 파일을 읽어 데이터프레임 형태로 dfParm에 저장합니다.
dfParm = pd.read_csv("result.csv", header = 0)
# 읽어서 각 w와 b를 저장합니다.
w_am = dfParm['w'][0]
b_am = dfParm['b'][0]
w_pm = dfParm['w'][1]
b_pm = dfParm['b'][1]

pre_time = int(input("예측할 시간대를 입력하세요 (0 ~ 23): "))
t = change_time(pre_time, 2)
print("t: " + str(t))

# 원하는 시간대에서 습도의 값을 예측합니다.
if 0 <= pre_time < 12:
    predic_result = predict(w_am,b_am,t)
elif 12 <= pre_time < 24:
    predic_result = predict(w_pm,b_pm,t)

print("예측 습도: " + str(predic_result))


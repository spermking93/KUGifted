import tensorflow as tf
import time
import csv
import pandas as pd
import numpy as np

def LinearRegression(step, lr, df):     # setp: 몇 번 학습 반복할지 / lr: alpha / dadta: csv 파일을 읽은 데이터프레임
    
    time = np.arange(0, len(df), 1)
    data = df
    
    x_data = time
    y_data = data

    b_initial = data[0]
    w_initial = (data[1] - data[0])

    b = tf.Variable(b_initial)
    w = tf.Variable(w_initial)

    b_result = 0
    w_result = 0

    learnig_rate = lr

    for i in range(0, step):
        with tf.GradientTape() as tape:

            hypothesis = w * x_data + b
            
            cost = tf.reduce_mean(tf.square(hypothesis - y_data))

        w_grad, b_grad = tape.gradient(cost, [w, b])
        
        w.assign_sub(learnig_rate * w_grad)
        b.assign_sub(learnig_rate * b_grad)

        w_result = w.numpy()
        b_result = b.numpy()
    
    
    return w_result, b_result


dfData = pd.read_csv("humTime.csv", header = None)

# 데이터프레임 형식인 dfData의 첫번째 열의 0행부터 5번째 행까지를 list 형식으로 바꿔서 LinearRegression 함수에 넘겨준다.
w_am, b_am = LinearRegression(30,0.01,dfData.iloc[:6, 1].tolist())

# 데이터프레임 형식인 dfData의 첫번째 열의 6번째 행부터 마지막 행까지를 list형식으로 바꿔서 LinearRegression 함수에 넘겨준다.
w_pm, b_pm = LinearRegression(30,0.01,dfData.iloc[6:, 1].tolist())

print(w_am, b_am)
print(w_pm, b_pm)

# result.csv파일에 w, b를 저장합니다.
result = {'w': [w_am, w_pm], 'b': [b_am, b_pm]}
result_pd = pd.DataFrame(result)
result_pd.to_csv('result.csv', index = False)

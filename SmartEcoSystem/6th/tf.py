import tensorflow as tf
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def LinearRegression(step, lr, data):     # hum 에 관해서 setp: 몇 번 학습 반복할지 / lr: alpha / dadta: csv 파일을 읽은 데이터프레임
    
    time = np.arange(0, len(data[0]), 1)
    hum = data[1]
        
    x_data = time
    y_data = hum

    b_initial = hum[1]
    w_initial = (hum[2] - hum[1])

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

        if i % 30 == 0 or i == step-1:
            plt.scatter(x_data, y_data, label = 'hum')
            
            x = np.arange(0, len(data[0]), 1)
            y = [(w * num + b) for num in x]

            plt.plot(x, y, c = 'r', label = 'w = ' + str(w.numpy()) + ', b = ' + str(b.numpy()))
            
            plt.title('i = ' + str(i))
            plt.legend()
            plt.show()
        
    return w_result, b_result


df = pd.read_csv("humtempTime.csv", header = None)
w, b = LinearRegression(100, 0.001, df)
print(w, b)

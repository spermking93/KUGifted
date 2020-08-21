import tensorflow as tf
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def LinearRegression(step, lr, df):     # setp: 몇 번 학습 반복할지 / lr: alpha / dadta: csv 파일을 읽은 데이터프레임
    
    time = np.arange(0, len(df[0]), 1)
    data = df[1]
    
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



###################################################################
#   csv 를 판다스 dataframe 형식으로 읽은 후 dfData로 저장합니다.   #
#           위의 함수를 이용해서 w, b 값을 학습합니다.              #
###################################################################


dfData = pd.read_csv("humtempTime.csv", header = None)
w, b = LinearRegression(30, 0.001, dfData)
x = np.arange(0, len(dfData[0]), 1)
y = [(w * num + b) for num in x] 


##############################################################
#   측정 데이터를 앞서배운 plt.scatter 메소드를 이용해서 그려라 #
##############################################################

x_data = x
y_data = dfData[1]
plt.scatter(x_data, y_data, label = 'hum')

plt.plot(x, y, c = 'r', label = 'w = ' + str(w) + ', b = ' + str(b))

#plt.title('i = ' + str(30))         # 타이틀이 i 인데, 이것도 직접 입력하게??
plt.legend()

plt.show()
        

print(w, b)

###########################################
#   120번 째 이후 예측 값을 출력해봅니다.   #
###########################################

print("38번째: "  + str(37*w + b))
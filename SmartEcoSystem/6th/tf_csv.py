# 저장한 습도 csv 파일을 가지고 다음 습도를 예측해봅니다.

import tensorflow as tf
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# LinearRegression이라는 함수를 정의합니다.
def LinearRegression(step, lr, df):     # setp: 몇 번 학습 반복할지 / lr: alpha / dadta: csv 파일을 읽은 데이터프레임
    
    # 시간에 데이터프레임 크기 만큼의 정수를 저장합니다. 0, 1, 3... 이런 식으로
    time = np.arange(0, len(df[0]), 1)
    
    # data에 df[1]을 저장합니다.
    data = df[1]
    
    # x_data에 time을 넣습니다.
    x_data = time
    # y_data에 data를 넣습니다.
    y_data = data

    # 일차함수의 초기 y절편은 data[0]으로 정합니다.
    b_initial = data[0]
    # 일차함수의 초기 기울기를 data[1] - data[0] 으로 정합니다.
    w_initial = (data[1] - data[0])

    # 텐서플로우에 활용 되게끔 형식에 맞게 변수로 초기화합니다.
    b = tf.Variable(b_initial)
    w = tf.Variable(w_initial)

    # 학습 전 초기 기울기 값과 y절편 값을 0으로 설정합니다.
    b_result = 0
    w_result = 0

    # 텐서플로우의 학습률을 나타냅니다. 기울기 값을 얼마나 반영할지를 결정합니다.
    learnig_rate = lr

    # step 만큼 학습을 반복시킵니다.
    for i in range(0, step):
        # 텐서플로우에서 제공하는 기울기를 구하는 API
        with tf.GradientTape() as tape:
            # 가설 변수를 설정합니다. (추세선)
            hypothesis = w * x_data + b
            # 오차 제곱의 평균을 cost에 저장합니다.
            cost = tf.reduce_mean(tf.square(hypothesis - y_data))

        # cost의 x, b에 대한 미분 값을 순서대로 할당하며 이를 지속적으로 갱신합니다. 즉, 기울기를 업데이트 합니다.
        w_grad, b_grad = tape.gradient(cost, [w, b])
        
        # 업데이트된 순간 기울기가 양이면 왼쪽으로 이동하고, 음이면 오른쪽으로 이동합니다.
        w.assign_sub(learnig_rate * w_grad)
        b.assign_sub(learnig_rate * b_grad)

        w_result = w.numpy()
        b_result = b.numpy()
    
    # 학습을 통해 최종으로 구한 예측 기울기 w와 예측 y절편 b를 return합니다.
    return w_result, b_result



###################################################################
#   csv 를 판다스 dataframe 형식으로 읽은 후 dfData로 저장합니다.   #
#           위의 함수를 이용해서 w, b 값을 학습합니다.              #
###################################################################



##################################################################
#   측정 데이터를 앞서배운 plt.scatter 메소드를 이용해서 그립니다.  #
##################################################################


# 학습을 통해 얻은 일차함수를 그립니다.
plt.plot(x, y, c = 'r', label = 'w = ' + str(w) + ', b = ' + str(b))
plt.title('i = ' + str(30))
plt.legend()
plt.show()



###########################################
#   120번 째 이후 예측 값을 출력해봅니다.   #
###########################################




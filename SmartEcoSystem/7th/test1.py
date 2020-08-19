import tftest
import RPi.GPIO as GPIO
import datetime
import time
import spidev
import Adafruit_DHT as dht



# 시간에 대한 리스트
timelist = []
# 습도에 대한 리스트
humilist = []
# 온도에 대한 리스트
templist = []

dataMag=10

i = 0
# i가 step값 보다 작은 범위 한에서 아래 과정을  무한반복합니다. 
try:
     while True:
          # 센서값을 읽어서 저장합니다.
          h,t = dht.read_retry(dht.DHT22, 4)

          # 현재 시각에 대한 값을 저장합니다.  
          now = datetime.datetime.now()

          # 시각을 시,분,초로 나타냅니다. 
          nowTime = now.strftime('%H:%M:%S')
        
          # 시,분,초로 나타낸 현재 시각을 출력합니다.
          print(nowTime)
        
          # 온도 습도를  형식에 맞게 값을 출력합니다..
          print('Temp={0:0.01f}*C Humidity={1:0.01f}%'.format(t, h))
    
          # i를 시간의 리스트 값으로 추가합니다.
          timelist.append(i)
        
          # 측정된 습도값을 리스트값에 추가합니다.
          humilist.append(h)
        
          # 측정된 온도값을 리스트값에 추가합니다.
          templist.append(t)
        
          # 실제 시간간격을 0.01초로 설정합니다.
          time.sleep(.01)
         
          if i % dataMag == 0 and i != 0:
             
             W_h, b_h = tftest.LinearRegression(101 , 0.001, humilist, timelist, dataMag)
             W_t, b_t = tftest.LinearRegression(101 , 0.001, templist, timelist, dataMag)     
             
             
             timeNext = 11.

             print(W_h,b_h)
             hum = W_h * timeNext + b_h
             print(hum)

             print(W_t,b_t)
             temp = W_t * timeNext + b_t 
             print(temp)

             i = 0

             timelist.clear()
             humilist.clear()
             templist.clear()

             
       
          else:
              i = i + 1

          

except KeyboardInterrupt:
     print("finish")



import learn
import RPi.GPIO as GPIO
import datetime
import time
import spidev
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D4)

# 시간에 대한 리스트
timelist = []
# 습도에 대한 리스트
humilist = []
# 온도에 대한 리스트
templist = []

def panpump(hum, temp):
    if (60. > hum) :
        #GPIO.output(w1,GPIO.HIGH)
        #GPIO.output(w2,GPIO.LOW)
        print("humhumhum")
    else :
        #GPIO.output(w1,GPIO.LOW)
        #GPIO.output(w2,GPIO.LOW)
        print("not hum")
    time.sleep(0.5)


    if (25. < temp) :
        #GPIO.output(w3,GPIO.HIGH)
        #GPIO.output(w4,GPIO.LOW)
        print("temptemptemp")
    else :
        #GPIO.output(w3,GPIO.LOW)
        #GPIO.output(w4,GPIO.LOW)
        print("not temp")
    time.sleep(5.0)



#dataMag=10
dataMag = int(input("학습할 데이터의 갯수를 정하세요: "))
step = int(input("학습할 횟수를 정하세요: "))

i = 0
# i가 step값 보다 작은 범위 한에서 아래 과정을  무한반복합니다. 
try:
     while True:
        # 센서값을 읽어서 저장합니다.
        h = float(dhtDevice.humidity)
        t = float(dhtDevice.temperature)

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
             
            W_h, b_h = learn.LinearRegression(step , 0.001, humilist, timelist, dataMag)
            W_t, b_t = learn.LinearRegression(step , 0.001, templist, timelist, dataMag)     
             
             
            timeNext = dataMag

            print(W_h,b_h)
            next_hum = W_h * timeNext + b_h
            print(hum)

            print(W_t,b_t)
            next_temp = W_t * timeNext + b_t 
            print(temp)

            i = 0

            timelist.clear()
            humilist.clear()
            templist.clear()

            panpump(next_hum, next_temp)

        else:
            i = i + 1

          

except KeyboardInterrupt:
    print("finish")
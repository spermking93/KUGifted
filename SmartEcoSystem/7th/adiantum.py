import learn
import RPi.GPIO as GPIO
import datetime
import time
import spidev
import adafruit_dht
import board
import smbus   # i2c 라이브러리

# 사용할 i2c 채널 번호
I2C_CH = 1
# BH1750 주소
BH1750_DEV_ADDR = 0x23

# 조도의 측정 모드
# 값이 1lx 단위로 측정되며 샘플링 시간은 120ms이고 계속 측정하는 모드
CONT_H_RES_MODE     = 0x10

i2c = smbus.SMBus(I2C_CH)

dhtDevice = adafruit_dht.DHT11(board.D4)

# 시간에 대한 리스트
timelist = []
# 습도에 대한 리스트
humilist = []
# 온도에 대한 리스트
templist = []

# GPIO의 핀모드를 BCM으로 설정합니다.
GPIO.setmode(GPIO.BCM)

# 5번 6번 핀을 팬의 출력 핀으로 설정하고 LOW로 설정합니다.
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)

# 23번 24번 핀을 펌프의 출력 핀으로 설정하고 LOW로 설정합니다.
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, GPIO.LOW)


# panpump 함수를 정의합니다.
def panpump(hum, temp):
    if (50. > hum) :
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(24,GPIO.LOW)
    else :
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)

    time.sleep(0.5)


    if (26. < temp) :
        GPIO.output(5,GPIO.HIGH)
        GPIO.output(6,GPIO.LOW)
    else :
        GPIO.output(5,GPIO.LOW)
        GPIO.output(6,GPIO.LOW)

    time.sleep(5.0)


# luxledcontrol 함수를 정의합니다.
def luxledcontrol():
    luxBytes = i2c.read_i2c_block_data(BH1750_DEV_ADDR, CONT_H_RES_MODE, 2)
    lux = int.from_bytes(luxBytes, byteorder='big')

    if lux >= 800:
        print('{0}lux RED LED ON. ITS TOO BRIGHT NOW !'.format(lux))
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)



# 100개의 데이터를 수집해서 100번 학습 시켜 예측하도록 합니다.
dataMag = 100
step = 100

i = 0
# i가 step값 보다 작은 범위 한에서 아래 과정을  무한반복합니다. 
try:
     while True:
        # 센서값을 읽어서 저장합니다.
        t = float(dhtDevice.temperature)
        h = float(dhtDevice.humidity)
    
        # 현재 시각에 대한 값을 저장합니다.  
        now = datetime.datetime.now()

        # 시각을 시,분,초로 나타냅니다. 
        nowTime = now.strftime('%H:%M:%S')
        
        # 시,분,초로 나타낸 현재 시각을 출력합니다.
        print(nowTime)
        
        # 습도를  형식에 맞게 값을 출력합니다..
        print('Temp={1:0.01f}*C Humidity={1:0.01f}%'.format(t, h))
    
        # i를 시간의 리스트 값으로 추가합니다.
        timelist.append(i)
        
        # 측정된 습도값을 리스트값에 추가합니다.
        humilist.append(h)
        
        # 측정된 온도값을 리스트값에 추가합니다.
        templist.append(t)
        
        # 실제 시간간격을 108초로 설정합니다. 3시간동안 100개의 데이터를 수집해 예측하기 위함입니다.
        time.sleep(108)
         
        if i == dataMag - 1 and i != 0:
             
            W_h, b_h = learn.LinearRegression(step , 0.001, humilist, timelist, dataMag)
            W_t, b_t = learn.LinearRegression(step , 0.001, templist, timelist, dataMag)     
            
            timeNext = dataMag

            next_hum = W_h * timeNext + b_h
            next_temp = W_t * timeNext + b_t 
            
            i = 0

            timelist.clear()
            humilist.clear()
            templist.clear()

            panpump(next_hum, next_temp)
            luxledcontrol()
            

        else:
            i = i + 1

          

except KeyboardInterrupt:
    GPIO.cleanup()
    print("finish")
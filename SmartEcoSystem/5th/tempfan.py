# 온습도 센서로 온도 정보를 추출하고 온도에 따라 팬을 제어해봅니다.

import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import time

# GPIO 사용을 위해 기본 설정을 합니다.
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)

# 1초간의 텀을 줍니다.
time.sleep(1)

# 아래 코드를 시도합니다.
try:
    # while문 안의 코드를 반복합니다.
    while True:
        # 온습도 센서로 온도와 습도 정보를 알아내어 각각 t, h에 저장합니다.
        h,t = dht.read_retry(dht.DHT22, 4)

        # 온도가 25도 이상이면 팬을 작동합니다.
        if t>= 25:
            print("Temp: {0:0.1f}*C FAN ON".format(t))
            GPIO.output(5, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(5, GPIO.LOW)
        
        time.sleep(1.0)

except KeyboardInterrupt:
    GPIO.cleanup()

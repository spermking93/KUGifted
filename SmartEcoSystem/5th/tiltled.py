# 기울기 센서를 통해 기울기를 측정하고, 기울기에 따라 LED를 제어해봅니다.

import Adafruit_ADXL345
import time
import RPi.GPIO as GPIO

accel = Adafruit_ADXL345.ADXL345()

# GPIO 사용을 위한 설정을 해줍니다.
GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)     # R
GPIO.output(19, GPIO.HIGH)
GPIO.setup(20,GPIO.OUT)     # G
GPIO.output(20, GPIO.HIGH)
GPIO.setup(21,GPIO.OUT)     # B
GPIO.output(21, GPIO.HIGH)

# 1초간의 텀을 줍니다.
time.sleep(1)

# 기울기 센서로부터 기울기 정보를 initx, inity, initz에 저장합니다.
initx, inity, initz = accel.read()
print("initial x, y, z: {0}, {1}, {2}".format(initx, inity, initz))

time.sleep(3)       # 3초 쉬고

# 아래 코드를 시도합니다.
try:
    # while문 안의 코드를 반복합니다.
    while True:
        # 기울기 센서로부터 기울기 정보를 받아옵니다.
        x, y, z = accel.read()

        # 처음에 측정했던 기울기에서, 최근 측정한 기울기의 차이를 구합니다.
        subx = abs(x - initx)
        suby = abs(y - inity)
        subz = abs(z - initz)        # x, y, z 기울기 차이 구하기 (절댓값)

        '''
        이 코드 처음 실행했을 때와 비교해서 x, y, z 중 어디로 가장 치우쳤는지!
        기준은 가장 처음 코드를 실행했을 때의 기울기.
        x쪽으로 가장 치우쳤으면 빨간색, y쪽으로 가장 치우쳤으면 초록색, z축으로 가장 치우쳤으면 파란색
        '''

        # x축으로 가장 많이 기울었다면 LED는 빨간색 빛을 냅니다.
        if max(subx, suby, subz) == subx:
            print("x, y, z: {0}, {1}, {2} RED LED ON".format(x, y, z))
            GPIO.output(19, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.HIGH)

        # y축으로 가장 많이 기울었다면 LED는 초록색 빛을 냅니다. 
        elif max(subx, suby, subz) == suby:
            print("x, y, z: {0}, {1}, {2} GREEN LED ON".format(x, y, z))
            GPIO.output(19, GPIO.HIGH)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)

        # z축으로 가장 많이 기울었다면 LED는 파란색 빛을 냅니다.
        else:
            print("x, y, z: {0}, {1}, {2} BLUE LED ON".format(x, y, z))
            GPIO.output(19, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)

        time.sleep(1)
        

except KeyboardInterrupt:
    GPIO.cleanup()

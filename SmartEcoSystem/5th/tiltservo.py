import Adafruit_ADXL345
import time
import RPi.GPIO as GPIO

accel = Adafruit_ADXL345.ADXL345()

# GPIO 사용을 위해 기본 설정을 합니다.
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

# 13번 핀으로 PWM제어를 시작합니다.
p = GPIO.PWM(13, 50)
p.start(0)

# 1초간의 텀을 줍니다.
time.sleep(1)

try:
    while True:
        x, y, z = accel.read()
        # y축으로의 기울기가 -100 미만이면 서보모터가 회전합니다.
        if y < -100:
            print("x, y, z: {0}, {1}, {2} SERVO ROtATED".format(x, y, z))
            p.ChangeDutyCycle(10)
            print("angle : 90")

        # y축으로의 기울기가 100 이상이면 서보모터가 회전합니다.
        elif y > 100:
            print("x, y, z: {0}, {1}, {2} SERVO ROtATED".format(x, y, z))
            p.ChangeDutyCycle(5)
            print("angle : 0")
        
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

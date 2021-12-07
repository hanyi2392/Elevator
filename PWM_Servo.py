#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

# 핀 번호
SERVO_PIN = 18
BUZZER_PIN = 23

# 불필요한 warning 제거
GPIO.setwarnings(False)

# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)

# 출력 설정 
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# PWM 인스턴스 servo 생성, 주파수 50으로 설정 
servo = GPIO.PWM(SERVO_PIN,50)
buzzer = GPIO.PWM(BUZZER_PIN, 440)

def open_door():
        servo.start(0)
        servo.ChangeDutyCycle(12.5) # 180도 
        time.sleep(1)
        servo.stop()

def close_door() :
        servo.start(0)
        servo.ChangeDutyCycle(2.5)  # 0도 
        time.sleep(1)
        servo.stop()

def make_sound() :
        buzzer.start(10)
        buzzer.ChangeFrequency(329)
        time.sleep(0.5)
        buzzer.ChangeFrequency(261)
        time.sleep(0.5)
        buzzer.stop()
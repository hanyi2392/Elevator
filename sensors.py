#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

# 핀 번호
SERVO_PIN = 18
BUZZER_PIN = 23
TRIG = 3
ECHO = 4
        
# 불필요한 warning 제거
GPIO.setwarnings(False)

# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)

# 출력 설정 
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM 인스턴스 servo 생성, 주파수 55으로 설정 
buzzer = GPIO.PWM(BUZZER_PIN, 440)

distance=11

def open_door():
        try :
                servo = GPIO.PWM(SERVO_PIN,55)
                servo.start(0)
        except RuntimeError :
                time.sleep(1)
                servo = GPIO.PWM(SERVO_PIN,55)
                servo.start(0)
        print("-----------------------------------------")
        print("문이 열립니다.")
        print("-----------------------------------------")
        servo.ChangeDutyCycle(12.5) # 180도 
        time.sleep(1)
        servo.stop()

def close_door() :
        try :
                servo = GPIO.PWM(SERVO_PIN,55)
                servo.start(0)
        except RuntimeError:
                time.sleep(1)
                servo = GPIO.PWM(SERVO_PIN,55)
                servo.start(0)
        print("-----------------------------------------")
        print("문이 닫힙니다.")
        print("-----------------------------------------")
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

def person_detect() :
        global distance
        
        #Trig핀의 신호를 0으로 출력 
        GPIO.output(TRIG, False)
        print("Waiting for sensor to settle")
        time.sleep(2)

        while True: 			     
                GPIO.output(TRIG, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
                time.sleep(0.00001)       # 10µs 딜레이 
                GPIO.output(TRIG, False)
                
                while GPIO.input(ECHO)==0:
                        start = time.time()	 # Echo 핀 상승 시간 
                while GPIO.input(ECHO)==1:
                        stop= time.time()	 # Echo 핀 하강 시간 
                        
                check_time = stop - start
                distance = check_time * 34300 / 2
                #print("Distance : %.1f cm" % distance)
                time.sleep(0.4)	# 0.4초 간격으로 센서 측정 
                       
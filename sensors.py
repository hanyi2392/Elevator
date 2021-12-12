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

buzzer = GPIO.PWM(BUZZER_PIN, 440)

distance=11
cdc = 2.5

def open_door():
        global cdc
        pwmready=False
        while(not pwmready) :
                try :
                        servo = GPIO.PWM(SERVO_PIN,55)
                        servo.start(0)
                        pwmready=True
                except RuntimeError :
                        pwmready=False
                        time.sleep(1)
                print("=======runtime_error_loop=======")
        print("-----------------------------------------")
        print("문이 열립니다.")
        print("-----------------------------------------")
        while(cdc<12.5) :
                cdc = cdc + 0.5
                servo.ChangeDutyCycle(cdc) # 180도 
                time.sleep(0.1)
        servo.stop()

def close_door() :
        global cdc
        pwmready=False
        while(not pwmready) :
                try :
                        servo = GPIO.PWM(SERVO_PIN,55)
                        servo.start(0)
                        pwmready=True
                except RuntimeError :
                        pwmready=False
                        time.sleep(1)
                print("=======runtime_error_loop=======")
        print("-----------------------------------------")
        print("문이 닫힙니다.")
        print("-----------------------------------------")
        while(cdc>2.5) :
                cdc = cdc-0.5
                servo.ChangeDutyCycle(cdc)  # 0도 
                time.sleep(0.1)
                if(distance<10) : 
                        servo.stop()
                        return 1
        servo.stop()
        return 0

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
                if(distance<10) : print("-------사람 감지됨-------")
                time.sleep(0.4)	# 0.4초 간격으로 센서 측정 
                       
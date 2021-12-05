# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/로 접속하면 
# index.html을 실행하고 버튼을 이용하여 LED 작동시킴

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
import time
import threading
import PWM_Servo

app = Flask(__name__)

STOP = 0
UP = 1
DOWN = 2

story = 5           # 전체 층수
btnum = story*3-2   # 전체 버튼수

class button:
    def __init__(self, floor, move, pushed):
        self.floor = floor
        self.move = move
        self.pushed = pushed

btn_list = [button(1, STOP, False),
            button(1, UP, False),
            button(2, STOP, False),
            button(2, UP, False),
            button(2, DOWN, False),
            button(3, STOP, False),
            button(3, UP, False),
            button(3, DOWN, False),
            button(4, STOP, False),
            button(4, UP, False),
            button(4, DOWN, False),
            button(5, STOP, False),
            button(5, DOWN, False), ]

class elevator:
    def __init__(self, floor_state, move, next_dst):
        self.floor_state = floor_state
        self.move = move
        self.next_dst = next_dst

    def seek_upper_stop(self):
        global btn_list
        dst_floor = 0
        i = self.floor_state*3-2  # 1=2, 2=5, 3=8, 4=11
        while (i < btnum):
            if btn_list[i].pushed == True:
                dst_floor = btn_list[i].floor
                if btn_list[i].move is not DOWN:
                    break
            i = i+1
        return dst_floor

    def seek_lower_stop(self):
        global btn_list
        dst_floor = 0
        i = self.floor_state*3-5  # 5=10, 4=7, 3=4, 2=1
        while (i >= 0):
            if btn_list[i].pushed == True:
                dst_floor = btn_list[i].floor
                if btn_list[i].move is not UP:
                    break
            i = i-1
        return dst_floor

    def set_next_dst(self):
        global btn_list
        if(self.move == UP):
            dst_floor = self.seek_upper_stop()
            if(dst_floor):
                self.next_dst = dst_floor
            else:
                dst_floor = self.seek_lower_stop()
                if(dst_floor == 0):
                    self.move = STOP
                    self.next_dst = 0
                    return
                else:
                    self.move = DOWN
        else:
            dst_floor = self.seek_lower_stop()
            if(dst_floor):
                self.next_dst = dst_floor
                self.move = DOWN
            else:
                dst_floor = self.seek_upper_stop()
                if(dst_floor == 0):
                    self.move = STOP
                    self.next_dst = 0
                    return
                else:
                    self.move = UP
                    self.next_dst = dst_floor

    def go(self):
        global btn_list
        if self.move == UP:
            self.floor_state = self.floor_state + 1
        elif self.move == DOWN:
            self.floor_state = self.floor_state - 1
        print(self.floor_state, self.next_dst)
        if(self.floor_state == self.next_dst):
            print("")
            print(self.floor_state, "층입니다. 문이 열립니다.")
            print("")
            PWM_Servo.open_door()
            PWM_Servo.close_door()
        for bl in btn_list:
            if (bl.floor == self.floor_state) and ((bl.move == self.move) or (bl.move == STOP)):
                bl.pushed = False
            self.set_next_dst()


e = elevator(1, STOP, 0)

def system_reset():
    global btn_list, e
    btn_list = [button(1, STOP, False),
                button(1, UP, False),
                button(2, STOP, False),
                button(2, UP, False),
                button(2, DOWN, False),
                button(3, STOP, False),
                button(3, UP, False),
                button(3, DOWN, False),
                button(4, STOP, False),
                button(4, UP, False),
                button(4, DOWN, False),
                button(5, STOP, False),
                button(5, DOWN, False), ]
    e = elevator(1, STOP, 0)

mp = False

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/led/on")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def btn_interrupt():
    floor = request.args.get('floor', default = 1, type=int)
    move = request.args.get('move', default=0, type=int)
    global btn_list, e
    if floor == e.floor_state and e.move == STOP:
        print("문이 열립니다.")
        PWM_Servo.open_door()
        PWM_Servo.close_door()
        pushed = False
    else:
        for bl in btn_list:
            if (bl.floor == floor) and (bl.move == move):
                print("----------------------------")
                print(bl.floor, bl.move, "번 버튼 누름")
                print("----------------------------")
                bl.pushed = not bl.pushed
                pushed = bl.pushed
                break
        e.set_next_dst()
    print("----------------------------")
    print("pushed : ", pushed)
    print("----------------------------")
    return pushed

if __name__ == "__main__":
    app.run(host="0.0.0.0")
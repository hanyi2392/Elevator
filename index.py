# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/로 접속하면 
# index.html을 실행하고 버튼을 이용하여 LED 작동시킴

from flask import Flask, request
from flask import render_template
import time
import threading
import sensors
#from flask import Response, make_response
#import requests
#import json

app = Flask(__name__)

STOP = 0
UP = 1
DOWN = 2
term = 2

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
    def __init__(self, floor_state, move):
        self.floor_state = floor_state
        self.move = move

    def seek_upper_stop(self):
        global btn_list
        i = self.floor_state*3-1  # 1=2, 2=5, 3=8, 4=11
        while (i < btnum):
            if btn_list[i].pushed == True:
                return True
            i = i+1
        return False

    def seek_lower_stop(self):
        global btn_list
        i = self.floor_state*3-5  # 5=10, 4=7, 3=4, 2=1
        while (i >= 0):
            if btn_list[i].pushed == True:
                return True
            i = i-1
        return False

    def move_floor(self):
        global btn_list
        if self.move == UP:
            self.floor_state = self.floor_state + 1
        elif self.move == DOWN:
            self.floor_state = self.floor_state - 1

        # 버튼 눌림 여부를 검사해서 멈출지 말지 결정
        is_open = False
        for bl in btn_list:
            if (bl.pushed==True and bl.floor == e.floor_state):   # 눌린 버튼일 경우
                if(bl.move==STOP) :     # 엘리베이터 안에서 누른 버튼일 경우
                    bl.pushed=False         # 버튼 꺼짐
                    is_open=True            # 문열림
                if(bl.move==UP) :       # 위로 가는 버튼일 경우      # 아래로 가는 버튼일 경우
                    if(self.move!=DOWN) :     # 아래로 가고 있었다면 버튼 끄고 문열림
                        bl.pushed=False
                        is_open=True
                if(bl.move==DOWN) :       # 아래로 가는 버튼일 경우
                    if(self.move!=UP) :     # 아래로 가고 있었다면 버튼 끄고 문열림
                        bl.pushed=False
                        is_open=True

                # 다음에 갈 방향 결정
                if(self.move==UP) :  
                    is_up = self.seek_upper_stop()  # 위로 목적지가 더 있나 검사
                    if(not is_up) :
                        bl.pushed=False
                        is_open=True
                        is_down = self.seek_lower_stop()
                        if(is_down) : self.move=DOWN
                        else : self.move=STOP      # 아래로 가는 버튼일 경우
                if(self.move==DOWN) :     # 아래로 가고 있었다면 버튼 끄고 문열림
                    # 엘리베이터가 내려가는 중이라면 아래로 목적지가 더 있나 검사한다.
                    is_down = self.seek_lower_stop()  # 아래로 목적지가 더 있나 검사
                    if(not is_down) :                
                        bl.pushed=False
                        is_open=True
                        is_up = self.seek_upper_stop()
                        if(is_up) : 
                            self.move=UP
                        else : 
                            self.move=STOP
        
        if(is_open) :
            sensors.make_sound()
            sensors.open_door()
            sensors.close_door()

e = elevator(1, STOP)



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


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/btn")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def btn_interrupt():
    floor = request.args.get('floor', default = 1, type=int)
    move = request.args.get('move', default=0, type=int)
    global btn_list, e
    if e.move == STOP:
        if(floor>e.floor_state):
            e.move=UP
        if(floor<e.floor_state):
            e.move=DOWN
    for bl in btn_list:
        if bl.floor == floor and bl.move == move:
            bl.pushed = not bl.pushed
            return str(bl.pushed)


@app.route("/send_status")
def send_status():
    return str(e.floor_state)+str(e.move)

def go():
    while(True) :
        time.sleep(term)
        e.move_floor()

t1 = threading.Thread(target=go)     # Thread t1 생성
t1.start()
t2 = threading.Thread(target=sensors.person_detect)
t2.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
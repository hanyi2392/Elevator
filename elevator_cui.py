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


def see():
    global btn_list
    for bl in btn_list:
        if(bl.pushed):
            print(bl.floor, "층,  눌림 : ", bl.pushed)


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

    def go(self):
        print("======현재 방향======")
        print(self.move)
        print("===================")
        global btn_list
        is_open=False
        if self.move == UP:
            self.floor_state = self.floor_state + 1
        elif self.move == DOWN:
            self.floor_state = self.floor_state - 1

        # 버튼 눌림 여부를 검사해서 멈출지 말지 결정
        for bl in btn_list:
            if (bl.pushed==True and bl.floor == e.floor_state):   # 눌린 버튼일 경우
                if(bl.move==STOP) :     # 엘리베이터 안에서 누른 버튼일 경우
                    bl.pushed=False         # 버튼 꺼짐
                    is_open=True            # 문열림
                if(bl.move==UP) :       # 위로 가는 버튼일 경우      # 아래로 가는 버튼일 경우
                    if(self.move==UP) :     # 아래로 가고 있었다면 버튼 끄고 문열림
                        bl.pushed=False
                        is_open=True
                if(bl.move==DOWN) :       # 아래로 가는 버튼일 경우
                    if(self.move==DOWN) :     # 아래로 가고 있었다면 버튼 끄고 문열림
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
                            print("올라값니다.")
                        else : 
                            self.move=STOP
                            print("정지합니다.")
        print("======현재 방향======")
        print(self.move)
        print("===================")


        if(is_open) : 
            print("")
            print(self.floor_state, "층입니다. 문이 열립니다.")
            print("")


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
    e = elevator(1, STOP)


def btn_interrupt(floor, move):
    global btn_list
    if(e.move == STOP): # 아무 버튼도 눌려 있지 않았던 경우
        if(floor>e.floor_state):
            e.move=UP
        if(floor<e.floor_state):
            e.move=DOWN
    for bl in btn_list:
        if bl.floor == floor and bl.move == move:
            bl.pushed = not bl.pushed


print("현재 엘리베이터의 위치를 입력하세요 : ")
e.floor_state = int(input())

while(True):
    print("누를 버튼의 숫자를 입력하세요 : ")
    print("5층(50) :        ▽(52)")
    print("4층(40) : △(41) ▽(42)")
    print("3층(30) : △(31) ▽(32)")
    print("2층(20) : △(21) ▽(22)")
    print("1층(10) : △(11)       ")
    print("엘리베이터 움직이기 : 1")
    print("종료 : 0")
    try :
        btn_status = int(input())
    except :
        print("유효하지 않은 입력입니다.")
        continue
    if btn_status == 1:
        e.go()
    if btn_status == 0:
        break
    if btn_status != 1: btn_interrupt(btn_status//10, btn_status % 10)
    print("")
    print(e.floor_state, "층")
    print("")
    see()
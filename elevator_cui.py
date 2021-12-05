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

# 딕셔너리 사용해보기
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


def btn_interrupt(floor, move):
    global btn_list
    if(floor == e.floor_state and e.move == STOP):
        print("문이 열립니다.")
    else:
        for bl in btn_list:
            if bl.floor == floor and bl.move == move:
                bl.pushed = not bl.pushed
                break
        e.set_next_dst()


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
    btn_status = int(input())
    if btn_status == 1:
        e.go()
    if btn_status == 0:
        break
    btn_interrupt(btn_status//10, btn_status % 10)
    print("")
    print(e.floor_state, "층")
    print("")
    see()

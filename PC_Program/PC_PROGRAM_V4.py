import tkinter as tk
from tkinter import ttk
import tkinter.font
import serial
import time
import struct
import random

import serial.tools.list_ports

def find_available_ports(keyword):
    available_ports = list(serial.tools.list_ports.comports())
    filtered_ports = [port for port in available_ports if keyword in port.description]
    
    if not filtered_ports:
        print(f"{keyword}를 포함하는 사용 가능한 시리얼 포트가 없습니다.")
    else:
        print(f"{keyword}를 포함하는 사용 가능한 시리얼 포트 목록:")
        for port in filtered_ports:
            print(port.device, port.description)
    
    return filtered_ports

def select_serial_port(available_ports):
    if not available_ports:
        return None
    
    selected_port = available_ports[0].device  
    
    return selected_port


keyword = "Serial"
available_ports = find_available_ports(keyword)
selected_port = select_serial_port(available_ports)

if selected_port:
    try:
        py_serial = serial.Serial(port=selected_port, baudrate=9600, timeout=1)
        print(f"선택한 시리얼 포트: {selected_port}")
    except Exception as e:
        print(f"시리얼 포트를 열 수 없습니다: {e}")
else:
    print(f"{keyword}를 포함하는 시리얼 포트를 찾지 못했습니다.")




def send_yes_data_to_student(py_serial, addr, cmd, senddata): 
    preamble = 0x66
    sendsum = addr
    cmd
    sendsum += cmd
    sendsum += senddata
    if sendsum > 255:
        sendsum=sendsum-256        
    tail = 0x0D

    packed_data = struct.pack("BBBBBB", preamble, addr, cmd, senddata, sendsum, tail)
    py_serial.write(packed_data)
    
def send_no_data_to_student(py_serial, addr, cmd):  
    preamble = 0x66
    sendsum = addr
    cmd

    sendsum += cmd

    if sendsum > 255:
        sendsum=sendsum-256        
    tail = 0x0D

    packed_data = struct.pack("BBBBB", preamble, addr, cmd,sendsum,tail)
    py_serial.write(packed_data)

def get_no_data():
    rf_com_ok=0


    header = py_serial.read() 
    header = hex(ord(header))
    time.sleep(0.2)
    adr = py_serial.read()
    adr = hex(ord(adr))

    cmmd=py_serial.read()
    cmmd=hex(ord(cmmd))
    c_sum=py_serial.read()
    c_sum=hex(ord(c_sum))

    post=py_serial.read()
    post=hex(ord(post))
    if post == '0xd':
        r_sum = int(adr, 16) + int(cmmd, 16) 
        c_sum = int(c_sum,16)
        if r_sum >255:
            r_sum=r_sum-256

        if c_sum == r_sum:
            rf_com_ok=1
    return adr ,cmmd,rf_com_ok

def get_data1():
    r_sum=0
    rf_com_ok=0
    header = py_serial.read()  
    if not header:
        return None, None, None, 0 
    
    header = hex(ord(header))
    
    adr = py_serial.read()
    adr = hex(ord(adr))
    
    cmmd=py_serial.read()
    cmmd=hex(ord(cmmd))
        
    data=py_serial.read()
    data=hex(ord(data))

    c_sum=py_serial.read()
    c_sum=hex(ord(c_sum))

    post=py_serial.read()
    post=hex(ord(post))
    if post == '0xd':
        r_sum = int(adr, 16) + int(cmmd, 16) + int(data, 16) 
        c_sum = int(c_sum,16)
        if r_sum >255:
            r_sum=r_sum-256

        if c_sum == r_sum:
            rf_com_ok=1
    return adr ,cmmd,data,rf_com_ok


chosung_to_number = {
    'ㄱ': 1,
    'ㄲ': 2,
    'ㄴ': 3,
    'ㄷ': 4,
    'ㄸ': 5,
    'ㄹ': 6,
    'ㅁ': 7,
    'ㅂ': 8,
    'ㅃ': 9,
    'ㅅ': 10,
    'ㅆ': 11,
    'ㅇ': 12,
    'ㅈ': 13,
    'ㅉ': 14,
    'ㅊ': 15,
    'ㅋ': 16,
    'ㅌ': 17,
    'ㅍ': 18,
    'ㅎ': 19
}
def read_O_answers(py_serial, how_many_student,student_attend, MAX_ATTEND, CMD_XO_REQ):
            if how_many_student == 0:
                how_many_student = MAX_ATTEND
            ox_data='0xfb'
            o_correct_answer = []
            ucpass = 0
            expected_addr = 1


            while ucpass < how_many_student:
                if expected_addr > how_many_student:
                    break
                send_no_data_to_student(py_serial, int(student_attend[ucpass], 16), CMD_XO_REQ)
                student_att_exit = 1

                while student_att_exit:
                    adr, cmmd, data, rf_com_ok = get_data1()

                    if rf_com_ok == 1:
                        rf_com_ok = 0
                        student_att_exit = 0
                        if ox_data == data:

                            o_correct_answer.append(adr)
                    else:
                        student_att_exit = 0
                expected_addr += 1
                ucpass += 1

            return o_correct_answer

def read_X_answers(py_serial, how_many_student, student_attend, MAX_ATTEND, CMD_XO_REQ):
    if how_many_student == 0:
        how_many_student = MAX_ATTEND
    ox_data='0xf'
    x_correct_answer = []
    ucpass = 0
    expected_addr = 1

    while ucpass < how_many_student:
        if expected_addr > how_many_student:
            break
        send_no_data_to_student(py_serial, int(student_attend[ucpass], 16), CMD_XO_REQ)
        student_att_exit = 1

        while student_att_exit:
            adr, cmmd, data, rf_com_ok = get_data1()

            if rf_com_ok == 1:
                rf_com_ok = 0
                student_att_exit = 0
                if ox_data == data:

                    x_correct_answer.append(adr)
            else:
                student_att_exit = 0
        expected_addr += 1
        ucpass += 1

    return x_correct_answer
MAX_ATTEND = 8
RF_ALLSTUDENT=0xA1 


CMD_PING = 0x71
CMD_XO_REQ=0x72
CMD_GAMEMODE=0x73
CMD_RANDOM_CHOSUNG =0x76
CMD_CHOSUNG_FONT =0x77
CMD_TIME_OVER = 0x7c

GM_XOGAME=0x01
GM_CHOSUNG=0x03
GM_RANDOM_CHOSUNG=0x05

how_many_student = 0
student_attend = []
random_addr=[] 


current_time = int(time.time())
random.seed(current_time)

XO_problem = [                                      
    "미국의 수도는 뉴욕이다.",
    "6.25전쟁은 1950년에 일어났다.",
    "문어의 다리개수는 8개이다.",
    "대한민국의 국화는 장미이다.",
    "중력을 발견한 사람은 뉴턴이다.",
    "세계에서 가장 큰 강은 아마존강이다.",
    "지구의 자전 주기는 24시간이다.",
    "지구에서 가장 높은 산은 백두산이다.",
    "빛의 속도는 300,000 km/s이다.",
    "프랑스의 수도는 런던이다.",
    "달팽이는 이빨이 있다.",
    "바닷물 속에도 금이 들어 있다.",
    "고기를 많이 먹으면 방귀 냄새가 더 독하다.",
    "광화문역에 있는 이순신장군동상은 왼손에 칼을 들고 있다.",
    "문어의 다리는 문어의 머리에서 나온다.",
    "여왕개미는 개미중에 가장 오래 산다다.",
    "기린은 누워서 잠을 잘 수 없다.",
    "낙타는 선인장을 먹을 수 없다.",
    "인구가 가장 많은 대륙은 유럽이다.",
    "원숭이는 지문이 있다."

]
XO_answer = ["X", "O", "O", "X", "O", "O", "O", "X", "O", "X", "O", "O", "O", "X", "O", "O", "X", "X", "X", "O"]
num = random.randrange(0, 20)

def XO_attend(): 
    root.destroy() 

    global A1_window
    A1_window = tk.Tk()   
    A1_window.geometry("1280x960")
    # K_window.resizable(False, False)
    A1_window.title("쪼끼쪼끼(3355놀이)-OX게임")
    
    def attend_check(): # 시리얼 출석 명령어 넣기
            # =======================출석 ==================================   
        progress_bar['maximum'] = 7
        def attendance(MAX_ATTEND, CMD_PING):
            ucpass = 0
            expected_addr = 1
            global student_attend 
            global how_many_student 
            student_attend =[]
            how_many_student=0

            while ucpass < MAX_ATTEND:
                if expected_addr > MAX_ATTEND:
                    break
                progress_bar['value'] = ucpass
                root.update_idletasks()  # GUI 업데이트 
                send_no_data_to_student(py_serial, ucpass + 1, CMD_PING)
                student_att_exit = 1

                while student_att_exit:
                    adr, cmmd, data, rf_com_ok = get_data1()

                    if rf_com_ok == 1:
                        rf_com_ok = 0
                        student_attend.append(adr)
                        how_many_student += 1
                        student_att_exit = 0

                    else:
                        # 응답이 없는 경우 다음 주소로 이동
                        student_att_exit = 0

            
                expected_addr += 1
                ucpass += 1
            return how_many_student
        #======================출석===============================  
        label_attend.configure(text="현재 출석 인원 수 :" + str(attendance(MAX_ATTEND,CMD_PING)) , font=("맑은 고딕", 30)) 
        
    label_attend = tk.Label(
        A1_window, text="현재 출석 인원 수", font=("맑은 고딕", 30), height=3 #height는 폰트크기 기준으로 예를들어 height=3이면 
    )       
    label_attendging = tk.Label(A1_window,text="출석정보 체크는 약 7초정도 소요됩니다",font=("맑은 고딕", 10), height=4)
                                                               
    label_comment = tk.Label(A1_window,text="출석진행 후 다음을 눌러주세요",font=("맑은 고딕", 10), height=4)
   
    label_comment.pack()
    label_attendging.pack()            # 위에서 폰트크기 만한 글자 3개정도가 들어가는 위치에 생성합니다
    label_attend.pack()
    


    button_label = tk.Label(A1_window)
    button_label.pack()
    
    attend_button = tk.Button(
        button_label, 
        text = "출석 체크", 
        font=("맑은 고딕", 20),
        bg="orange",
        width=8,
        command = attend_check)
    attend_button.pack()
    other_game_button = tk.Button(
        button_label,           
        text="다음",
        font=("맑은 고딕", 20),
        height=1,
        bg="green", #버튼 색깔
        width=8,
        command=XO_Go #다른게임하기 버튼 클릭시 XO_Go()함수 실행
    )
    other_game_button.pack(side="left", anchor="s") #왼쪽 정렬
    progress_bar = ttk.Progressbar(A1_window, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack()
    

def XO_Go():
    send_yes_data_to_student(py_serial,RF_ALLSTUDENT,CMD_GAMEMODE,GM_XOGAME)  # XO게임모드전송
    def Root_go():     
        window.destroy()   #XO게임 윈도우창 종료
        
        global root
        root = tk.Tk()     #기본화면 다시 실행
        root.geometry("1280x960") #프로그램해상도
        root.resizable(False, False) #프로그램 크기 조정 불가
        root.title("쪼끼쪼끼(3355놀이)") #프로그램의 제목
        
        label_1 = tk.Label(root, text="쪼끼쪼끼(3355놀이)", font=("맑은 고딕", 30), height=3) #쪼끼쪼끼(3355)놀이 출력  #height는 폰트크기 기준으로 예를들어 height=3이면 
                                                                                             # 위에서 폰트크기 만한 글자 3개정도가 들어가는 위치에 생성합니다
        label_1.pack() #쪼끼쪼끼(3355)놀이 출력
        label_2 = tk.Label(root, text="원하는 게임의 버튼을 누르세요", font=("맑은 고딕", 20)) #원하는 게임의 버튼을 누르세요 출력, font는 맑은고딕에 글자 크기는 20입니다
        label_2.pack() #원하는 게임의 버튼을 누르세요 출력

        XO_button = tk.Button(
            root, text="1. XO게임", font=("맑은 고딕", 20), height=1, command=XO_attend #XO게임 버튼   command=XO_Go --> 1. XO게임 버튼을 누르면
        )                                                                                             # XO_Go함수 실행
        XO_button.pack() 
        Korean_button = tk.Button(
            root, text="2. 초성게임", font=("맑은 고딕", 20), height=1, command=Kor_attend #초성게임 버튼  command=Korean_go --> 2.초성게임 버튼을 누르면
        )                                                                                             # Korean_go함수 실행
        Korean_button.pack()

        root.mainloop()

    def check_answer():
        global XO
        XO=XO_answer[num]
        adr_to_number = {
            '0x1': 1,
            '0x2': 2,
            '0x3': 3,
            '0x4': 4,
            '0x5': 5,
            '0x6': 6,
            '0x7': 7,
            '0x8': 8,
            '0x9': 9,
            '0x10': 10,
        }   
        mapped_adrs=[] 
        if XO=='X':
            x_student=read_X_answers(py_serial, how_many_student, student_attend, MAX_ATTEND, CMD_XO_REQ)
            for i in x_student:
                if i in adr_to_number:
                    mapped_adr = adr_to_number[i]
                    mapped_adrs.append(mapped_adr)
                else :
                    mapped_adrs.append(None)


            label_check.configure(text="정답자:" +str(mapped_adrs), font=("맑은 고딕", 30))
        if XO=='O':
            o_student=read_O_answers(py_serial, how_many_student, student_attend, MAX_ATTEND, CMD_XO_REQ)
            for i in o_student:
                if i in adr_to_number:
                    mapped_adr = adr_to_number[i]
                    mapped_adrs.append(mapped_adr)
                else :
                    mapped_adrs.append(None)
            label_check.configure(text="정답자:" +str(mapped_adrs), font=("맑은 고딕", 30))
        
        send_yes_data_to_student(py_serial,RF_ALLSTUDENT,CMD_TIME_OVER,1) # 바로 OX선택 멈춰라
        answer_label.config(text=XO_answer[num], font=("맑은 고딕", 150)) #answer_label의 텍스트 값을 바꿔주는 함수
        
    def next_problem(): #ox에서 시간초 보내기만 넣으면될듯
        send_yes_data_to_student(py_serial,RF_ALLSTUDENT,CMD_GAMEMODE,GM_XOGAME)
        global num
        num = (num + 1) % len(XO_problem)  # 문제 개수에 따라 순환하도록 수정
        label_1.config(text="[문제] " + XO_problem[num])
        answer_label.config(text="?")

    def startTimer(): #타이머 동작함수 : 0이면 자동으로 중지
        def stop():
            global running 
            running = False
        if running == True:
            global timer
            timer -= 1
            timeText.configure(text= f'{timer:.2f} s')
            if timer == 0: #0으로 바꾸고 
                stop()
                #여기에 그만 명령어 보내면 될듯?
        window.after(1000, startTimer)

    def start(): #타이머 실행 
        global running
        
        if timer == 20:
            send_yes_data_to_student(py_serial,RF_ALLSTUDENT,CMD_TIME_OVER,20)
            time.sleep(1)
            running = True
        if timer == 10:
            send_yes_data_to_student(py_serial,RF_ALLSTUDENT,CMD_TIME_OVER,10)
            time.sleep(1)
            running = True
        if timer <= 0:
            running = False
        

    def timer_10(): #10초 타이머
        global running, timer
        running = False
        timer = 10
        timeText.configure(text= f'{timer:.2f} s')
        

    def timer_20(): #20초 타이머
        global running, timer
        running = False
        timer = 20
        timeText.configure(text= f'{timer:.2f} s')
        
          
#=======================================================================지금까지 XO_Go()의 내부함수 정의 였고  이제부터 XO_Go()의 내용입니다===============
    A1_window.destroy()     #출석화면 종료후 OX게임실행
    window = tk.Tk()  #window라는 프로그램창 생성
    window.geometry("1280x960") #window의 해상도 설정
    #window.resizable(False, False) #프로그램의 창 크기를 사용자가 임의로 조절가능하게 할것인지 False시 조정 불가
    window.title("쪼끼쪼끼(3355놀이)-XO게임") #프로그램 제목

    label_1 = tk.Label(
        window, text="[문제] " + XO_problem[num], font=("맑은 고딕", 30), height=3 # 문제를 띄워준다
    )
    label_1.pack()

    answer_label = tk.Label(window, text="?", font=("맑은 고딕", 150))   #정답을 띄워준다 정답보기 버튼을 누르기전에는 ? 가 출력 
    answer_label.place(x=600, y=410)

    next_problem_button = tk.Button(
        window,
        text="다음문제",
        font=("맑은 고딕", 20),
        height=1,
        bg="yellow", #버튼 색깔
        command=next_problem,  #다음문제 버튼을 누르면 next_problem()함수가 실행된다
    ) 
    next_problem_button.pack(side="right", anchor="s")  #오른쪽 정렬  anchor='s'는 south남쪽에 위치시키겠다는 의미로 N,W,E,S등 존재합니다

    answer_button = tk.Button(
        window,
        text="정답보기",
        font=("맑은 고딕", 20),
        height=1,
        bg="lightblue", #버튼 색깔
        command=check_answer,  #정답보기 버튼을 누르면 check_answer()함수가 실행
    )
    answer_button.pack(side="right", anchor="s") #오른쪽 정렬  
    
    global running, timer
    running = False
    timer = 0

    timeText = tk.Label(window, text = '0', font=("맑은 고딕", 20)) #남은시간 출력
    timeText.pack(side="top", anchor="w")

    startButton = tk.Button(window, text = 'Start', bg='yellow', command=start, width=10)   #Start 버튼을 누르면 start()함수가 실행된다
    startButton.pack(side="top", anchor="w")

    t_10_Button = tk.Button(window, text = '10초 타이머', bg='green', command=timer_10, width=10)   #10초 타이머 버튼을 누르면 timer_10()함수가 실행된다
    t_10_Button.pack(side="top", anchor="w")

    t_20_Button = tk.Button(window, text = '20초 타이머', bg='blue', command=timer_20, width=10)    #20초 타이머 버튼을 누르면 timer_20()함수가 실행된다
    t_20_Button.pack(side="top", anchor="w")

    startTimer()

    
    
    global label_check
    label_check = tk.Label(
        window, text="정답자", font=("맑은 고딕", 30)
    )                                                                       
    label_check.pack(side="left" ,anchor="s")

    other_game_button = tk.Button(
        window,
        text="다른 게임 하기",
        font=("맑은 고딕", 20),
        height=1,
        bg="green", #버튼 색깔
        command=Root_go,  #정답보기 버튼을 누르면 Root_go()함수가 실행
    )
    other_game_button.pack(side="right", anchor="s") #왼쪽 정렬

    window.mainloop()

#-------------------------------------------------------------------------------------------------------------------------------------------------
def Kor_attend(): # 초성게임 실행시 출석
    root.destroy() #메인화면 종료

    global A2_window
    A2_window = tk.Tk()   #출석프로그램 생성
    A2_window.geometry("1280x960")
    # K_window.resizable(False, False)
    A2_window.title("쪼끼쪼끼(3355놀이)-OX게임")
       
    def attend_check():
        progress_bar['maximum'] = 7
        def attendance(MAX_ATTEND, CMD_PING):
            ucpass = 0
            expected_addr = 1
            global student_attend 
            global how_many_student 
            how_many_student=0
            student_attend =[]

            while ucpass < MAX_ATTEND:
                if expected_addr > MAX_ATTEND:
                    break
                progress_bar['value'] = ucpass
                root.update_idletasks()  # GUI 업데이트 
                send_no_data_to_student(py_serial, ucpass + 1, CMD_PING)
                student_att_exit = 1

                while student_att_exit:
                    adr, cmmd, data, rf_com_ok = get_data1()

                    if rf_com_ok == 1:
                        rf_com_ok = 0
                        student_attend.append(adr)
                        how_many_student += 1
                        student_att_exit = 0

                    else:
                        # 응답이 없는 경우 다음 주소로 이동
                        student_att_exit = 0

            
                expected_addr += 1
                ucpass += 1
            return how_many_student
        
        label_attend.configure(text="현재 출석 인원 수:"+str(attendance(MAX_ATTEND,CMD_PING)), font=("맑은 고딕", 30)) 

        

    label_attend = tk.Label(
        A2_window, text="현재 출석 인원 수", font=("맑은 고딕", 30), height=3 #height는 폰트크기 기준으로 예를들어 height=3이면 
    )                                                                              # 위에서 폰트크기 만한 글자 3개정도가 들어가는 위치에 생성합니다
    label_attendging = tk.Label(A2_window,text="출석정보 체크는 약 7초정도 소요됩니다",font=("맑은 고딕", 10), height=4)
    label_attendging.pack()    
    label_comment2 = tk.Label(A2_window,text="출석진행 후 다음을 눌러주세요",font=("맑은 고딕", 10), height=4)
    label_comment2.pack()
    label_attend.pack()
       
    button_label = tk.Label(A2_window)
    button_label.pack()
     
    attend_button = tk.Button(
        button_label, 
        text = "출석 체크", 
        font=("맑은 고딕", 20),
        bg="orange",
        width=8,
        command = attend_check)
    attend_button.pack()
    other_game_button = tk.Button(
        button_label,           
        text="다음",
        font=("맑은 고딕", 20),
        height=1,
        bg="green", #버튼 색깔
        width=8,
        command=Korean_go #다른게임하기 버튼 클릭시 XO_Go()함수 실행
    )
    other_game_button.pack(side="left", anchor="s") #왼쪽 정렬
    progress_bar = ttk.Progressbar(A2_window, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack()

def Korean_go():   
    def KorToRoot(): #초성게임 페이지를 종료하고 다시 메인화면을 생성하는 함수
        G_window.destroy() #초성게임 종료
        global root
        root = tk.Tk()  #메인화면 생성
        root.geometry("1280x960") #메인화면 프로그램 사이즈 설정
        # root.resizable(False, False) #메인화면 프로그램의 창 크기를 사용자가 임의로 조절가능하게 할것인지 False시 조정 불가

        root.title("쪼끼쪼끼(3355놀이)")

        label_1 = tk.Label(root, text="쪼끼쪼끼(3355놀이)", font=("맑은 고딕", 30), height=3)
        label_1.pack()
        label_2 = tk.Label(root, text="원하는 게임의 버튼을 누르세요", font=("맑은 고딕", 20))
        label_2.pack()

        XO_button = tk.Button(
            root, text="1. XO게임", font=("맑은 고딕", 20), height=1, command=XO_attend #1. XO게임 버튼을 누르면 XO_Go() 함수 실행
        )
        XO_button.pack()
        
        Korean_button = tk.Button(
            root, text="2. 초성게임", font=("맑은 고딕", 20), height=1, command=Kor_attend #2. 초성게임 버튼을 누르면 Korean_go() 함수 실행
        )
        Korean_button.pack()

        root.mainloop()
    
    def origin_game():
        K_window.destroy() #메인화면 종료
        send_yes_data_to_student(py_serial,RF_ALLSTUDENT,CMD_GAMEMODE,GM_RANDOM_CHOSUNG)
        global G_window
        G_window = tk.Tk()   #초성게임프로그램 생성
        G_window.geometry("1280x960")
        # K_window.resizable(False, False)
        G_window.title("쪼끼쪼끼(3355놀이)-초성게임")
        label_korean = tk.Label(
            G_window, text="원하는 글자수를 선택하세요.", font=("맑은 고딕", 30), height=3 #height는 폰트크기 기준으로 예를들어 height=3이면 
        )                                                                               # 위에서 폰트크기 만한 글자 3개정도가 들어가는 위치에 생성합니다
        label_korean.pack()
        button_label = tk.Label(G_window)
        button_label.pack()
        two_word_button = tk.Button(
            button_label,
            text="2글자",
            font=("맑은 고딕", 20),
            height=1,
            bg="yellow", #버튼 색깔
            command=two_word, #2글자 버튼 클릭시 two_word()함수 실행
        )
        two_word_button.pack(side="left") #왼쪽 정렬
        three_word_button = tk.Button(
            button_label,
            text="3글자",
            font=("맑은 고딕", 20),
            height=1,
            bg="orange", #버튼 색깔
            command=three_word, #3글자 버튼 클릭시 three_word()함수 실행
        )
        three_word_button.pack(side="left")   #왼쪽 정렬

        global word_label
        word_label = tk.Label(G_window)
        word_label.pack()

        other_game_button = tk.Button(
            button_label,           
            text="다른 게임 하기",
            font=("맑은 고딕", 20),
            height=1,
            bg="green", #버튼 색깔
            command=KorToRoot, #다른게임하기 버튼 클릭시 KorToRoot()함수 실행
        )
        other_game_button.pack(side="right")    #오른쪽 정렬
    
    
    def sequence_game(): 
        K_window.destroy() #메인화면 종료
        #send_yes_data_to_student(py_serial, RF_ALLSTUDENT, CMD_GAMEMODE, GM_CHOSUNG)
        global G_window
        G_window = tk.Tk()   #초성게임프로그램 생성
        G_window.geometry("1280x960")
        # K_window.resizable(False, False)
        G_window.title("쪼끼쪼끼(3355놀이)-초성게임")
       
        label_korean = tk.Label(
            G_window, text="초성을 입력하세요.", font=("맑은 고딕", 30), height=3 #height는 폰트크기 기준으로 예를들어 height=3이면 
        )                                                                              # 위에서 폰트크기 만한 글자 3개정도가 들어가는 위치에 생성합니다
        label_korean.pack()

        global Ko_input
        Ko_input=tk.Entry(font=('맑은 고딕',30),bg='white',width=8)
        Ko_input.pack()

        button_label = tk.Label(G_window)
        button_label.pack()
               
        Korean_output_button = tk.Button(
            button_label,           
            text="입력",
            font=("맑은 고딕", 20),
            height=1,
            bg="orange", #버튼 색깔
            command=kor_output,#다른게임하기 버튼 클릭시 KorToRoot()함수 실행
        )
        Korean_output_button.pack(side="top", anchor="s") #왼쪽 정렬

        global kor_label
        kor_label = tk.Label(G_window)
        kor_label.pack()
        
        other_game_button = tk.Button(
            button_label,           
            text="다른 게임 하기",
            font=("맑은 고딕", 20),
            height=1,
            bg="green", #버튼 색깔
            command=KorToRoot #다른게임하기 버튼 클릭시 KorToRoot()함수 실행
        )
        other_game_button.pack(side="right", anchor="s") #왼쪽 정렬
        
    def two_word():
        random_font_list=[]
        ucpass = 0
        expected_addr = 1
        while ucpass < how_many_student:
            if expected_addr > how_many_student:
                break
            random_font = random.randrange(0, 14)
            random_font_list.append(random_font)
            send_yes_data_to_student(py_serial, int(student_attend[ucpass], 16), CMD_CHOSUNG_FONT, random_font_list[ucpass])
            time.sleep(0.2)
            expected_addr += 1
            ucpass += 1
        word_label.config(text="2명씩 짝지어 단어를 만드세요!", font=("맑은 고딕", 50), height=9) #"2명씩 짝지어 단어를 만드세요!"라는 문장 출력

    def three_word():
        random_font_list=[]
        ucpass = 0
        expected_addr = 1

        while ucpass < how_many_student:
            if expected_addr > how_many_student:
                break
            random_font = random.randrange(0, 14)
            random_font_list.append(random_font)
            send_yes_data_to_student(py_serial, int(student_attend[ucpass], 16), CMD_CHOSUNG_FONT, random_font_list[ucpass])
            time.sleep(0.2)
            expected_addr += 1
            ucpass += 1
        word_label.config(text="3명씩 짝지어 단어를 만드세요!", font=("맑은 고딕", 50), height=9) #"3명씩 짝지어 단어를 만드세요!"라는 문장 출력
    
    def kor_output():
        send_yes_data_to_student(py_serial, RF_ALLSTUDENT, CMD_GAMEMODE, GM_CHOSUNG)
        time.sleep(3)
        a = Ko_input.get()
        random_addr=[]
        chosung=list(a)
        chosung_font = [chosung_to_number[i] for i in chosung if i in chosung_to_number]
        random_addr = random.sample(student_attend, len(student_attend))
        ucpass = 0
        expected_addr = 1
        while ucpass < how_many_student:
            if expected_addr > how_many_student:
                break
            send_yes_data_to_student(py_serial, int(random_addr[ucpass], 16), CMD_CHOSUNG_FONT, chosung_font[ucpass])
            expected_addr += 1
            ucpass += 1
        kor_label.config(text="초성대로 줄을 서세요!", font=("맑은 고딕", 50), height=9) #"초성대로 줄을 서세요!"라는 문장 출력

#==========================================================지금까지 Korean_go()의 내부함수 정의였습니다===========================================
    A2_window.destroy() #출석체크화면 종료
    
    K_window = tk.Tk()   #초성게임선택 프로그램 생성
    K_window.geometry("1280x960")
    # K_window.resizable(False, False)
    K_window.title("쪼끼쪼끼(3355놀이)-초성게임")
    label_korean = tk.Label(
        K_window, text="원하는 게임을 선택하세요.", font=("맑은 고딕", 30), height=3 #height는 폰트크기 기준으로 예를들어 height=3이면 
    )                                                                               # 위에서 폰트크기 만한 글자 3개정도가 들어가는 위치에 생성합니다
    label_korean.pack()
    button_label = tk.Label(K_window)
    button_label.pack()
    two_word_button = tk.Button(
        button_label,
        text="그룹 게임",
        font=("맑은 고딕", 20),
        height=1,
        bg="yellow", #버튼 색깔
        command=origin_game, #버튼 클릭시 origin_game()함수 실행
    )
    two_word_button.pack(side="left") #왼쪽 정렬
    three_word_button = tk.Button(
        button_label,
        text="순서 게임",
        font=("맑은 고딕", 20),
        height=1,
        bg="orange", #버튼 색깔
        command=sequence_game, #버튼 클릭시 sequence_game()함수 실행
    )
    three_word_button.pack(side="left")   #왼쪽 정렬

    K_window.mainloop()

#======================================프로그램 실행 시키면 처음 나타나는 메인화면 부분
root = tk.Tk() #root라는 메인화면 생성
root.geometry("1280x960") #메인화면의 크기설정
#root.resizable(False, False)

root.title("쪼끼쪼끼(3355놀이)")

label_1 = tk.Label(root, text="쪼끼쪼끼(3355놀이)", font=("맑은 고딕", 30), height=3) #font 맑은고딕으로 크기는30으로 설정후 글자크기만큼의 3칸 아래에 위치
label_1.pack()
label_2 = tk.Label(root, text="원하는 게임의 버튼을 누르세요", font=("맑은 고딕", 20))
label_2.pack()

XO_button = tk.Button(
    root, text="1. XO게임", font=("맑은 고딕", 20), height=1, command=XO_attend #XO게임 버튼 클릭시 XO_Go함수 실행
)
XO_button.pack()
Korean_button = tk.Button(
    root, text="2. 초성게임", font=("맑은 고딕", 20), height=1, command=Kor_attend #초성게임 버튼 클릭시 Korean_go함수 실행
)
Korean_button.pack()


root.mainloop()

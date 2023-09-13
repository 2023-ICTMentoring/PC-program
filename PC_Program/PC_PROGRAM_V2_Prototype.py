import tkinter as tk
import tkinter.font
import random
import serial
# PC프로그램 GUI라이브러리로 tkinter라이브러리를 사용하였으며 
# https://m.blog.naver.com/sisosw/221408280038 이 사이트를 참고하시면 됩니다!
# 프로그램실행할때 반드시 마스터보드와 연결하여 장치관리자의 포트번호와 py_serial의 포트번호 일치 시켜야 프로그램이 실행됩니다!


def send_yes_data_to_student(py_serial, addr, cmd, datalen, senddata): #데이터가 있는 ex) cccc ttt9 8765 4321 명령어를 보낼때 사용
    preamble = 0x71                                                    #PC에서의 헤더PREAMBLE은 0X71
    py_serial.write(chr(preamble).encode())
    
    py_serial.write(chr(addr).encode())
    sendsum = addr
    
    py_serial.write(chr(cmd).encode())
    sendsum += cmd
    
    for i in range(datalen):
        sendsum += senddata[i]
        py_serial.write(chr(senddata[i]).encode())

    py_serial.write(chr(sendsum).encode())
    
    tail = 0x0D
    py_serial.write(chr(tail).encode())
    
def send_no_data_to_student(py_serial, addr, cmd):  #데이터가 없는 ex)#0x71 명령어를 보낼때 사용
    preamble = 0x71                                 #PC에서의 헤더PREAMBLE은 0X71
    py_serial.write(chr(preamble).encode())
    
    py_serial.write(chr(addr).encode())
    sendsum = addr
    
    py_serial.write(chr(cmd).encode())
    sendsum += cmd
    
    py_serial.write(chr(sendsum).encode())
    
    tail = 0x0D
    py_serial.write(chr(tail).encode())

    
py_serial = serial.Serial(
    # Window
    port="COM3",
    # 보드 레이트 (통신 속도)
    baudrate=9600,
)

XO_problem = [                                          #OX문제 추가할때 XO_answer의 답 순서와 맞춰주고 num = random.randrange(0, 10) 값 업데이트해야함
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
]
XO_answer = ["X", "O", "O", "X", "O", "O", "O", "X", "O", "X"]
num = random.randrange(0, 10)


def XO_Go():  #XO_Go함수 --> XO게임 버튼을 누르면 실행되는 함수로 이 함수안에는 다시 메인화면으로 돌아가는 Root_go()함수와 정답을 확인하는 check_answer()함수
              #다음 문제로 넘어가는 next_problem()함수가 있다 
              #이 함수는 메인화면에서 XO버튼을 누르면 메인화면을 종료하고 XO게임 페이지를 생성한다.
    addr = 0x01   #0xA1 모든학생  0x01 1번조끼
    cmd = 0x73    #ox게임 명령어
    datalen = 1
    senddata = [0x11]  #부저1초간 한번 울림
    send_yes_data_to_student(py_serial, addr, cmd, datalen, senddata) #학생보드로 OX게임 전송
    
    def Root_go():      #Root_go()함수 
        addr = 0x01   #0xA1 모든학생
        cmd = 0x71    #ox게임 결과확인 명령어
        send_no_data_to_student(py_serial, addr, cmd) #학생보드로 ox게임탈출 전송
        
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
            root, text="1. XO게임", font=("맑은 고딕", 20), height=1, command=XO_Go #XO게임 버튼   command=XO_Go --> 1. XO게임 버튼을 누르면
        )                                                                                             # XO_Go함수 실행
        XO_button.pack() 
        Korean_button = tk.Button(
            root, text="2. 초성게임", font=("맑은 고딕", 20), height=1, command=Korean_go #초성게임 버튼  command=Korean_go --> 2.초성게임 버튼을 누르면
        )                                                                                             # Korean_go함수 실행
        Korean_button.pack()

        root.mainloop()

    def check_answer():
        addr = 0x01   #0xA1 모든학생
        cmd = 0x71      
        send_no_data_to_student(py_serial, addr, cmd) #학생보드로 OX게임결과 요구를 전송
        
        answer_label.config(text=XO_answer[num], font=("맑은 고딕", 150)) #answer_label의 텍스트 값을 바꿔주는 함수
        
    def next_problem():
        addr = 0x01   #0xA1 모든학생
        cmd = 0x73
        datalen = 1
        senddata = [0x11]
        send_yes_data_to_student(py_serial, addr, cmd, datalen, senddata) #학생보드로 OX게임 전송
        
        global num
        num = (num + 1) % len(XO_problem)  # 문제 개수에 따라 순환하도록 수정
        label_1.config(text="[문제] " + XO_problem[num])
        answer_label.config(text="?")

#=======================================================================지금까지 XO_Go()의 내부함수 정의 였고  이제부터 XO_Go()의 내용입니다===============
    root.destroy()     #기본화면 종료후 OX게임실행
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

    other_game_button = tk.Button(
        window,
        text="다른 게임 하기",
        font=("맑은 고딕", 20),
        height=1,
        bg="green", #버튼 색깔
        command=Root_go,  #정답보기 버튼을 누르면 Root_go()함수가 실행
    )
    other_game_button.pack(side="left", anchor="s") #왼쪽 정렬

    window.mainloop()


def Korean_go():   #2. 초성게임 버튼을 누르면 실행 되는 함수로 Korean_go()의 내부함수로는 메인화면으로 돌아가는 함수인 KorToRoot(),
    # 2글자 단어 문제를 출제하는 two_word()함수, 3글자 단어 문제를 출제하는 three_word()함수가 존재하며
    # 이 함수를 실행하면 메인화면을 종료후 초성게임페이지를 생성시킨다.
    
    # addr = 0x01   #0xA1 모든학생
    # cmd = 0x74
    # datalen = 1
    # senddata = [0x11]
    # send_yes_data_to_student(py_serial, addr, cmd, datalen, senddata) #학생보드로 초성게임 전송
    
    def KorToRoot(): #초성게임 페이지를 종료하고 다시 메인화면을 생성하는 함수
        addr = 0x01   #0xA1 모든학생
        cmd = 0x71      
        send_no_data_to_student(py_serial, addr, cmd) #학생보드로 초성게임탈출 전송
        
        
        K_window.destroy() #초성게임 종료
        
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
            root, text="1. XO게임", font=("맑은 고딕", 20), height=1, command=XO_Go #1. XO게임 버튼을 누르면 XO_Go() 함수 실행
        )
        XO_button.pack()
        
        Korean_button = tk.Button(
            root, text="2. 초성게임", font=("맑은 고딕", 20), height=1, command=Korean_go #2. 초성게임 버튼을 누르면 Korean_go() 함수 실행
        )
        Korean_button.pack()

        root.mainloop()

    def two_word():
        addr = 0x01   #0xA1 모든학생
        cmd = 0x74
        datalen = 1
        senddata = [0x11]
        send_yes_data_to_student(py_serial, addr, cmd, datalen, senddata) #학생보드로 초성게임 전송
        
        word_label.config(text="2명씩 짝지어 단어를 만드세요!", font=("맑은 고딕", 50), height=9) #"2명씩 짝지어 단어를 만드세요!"라는 문장 출력

    def three_word():
        addr = 0x01   #0xA1 모든학생
        cmd = 0x74
        datalen = 1
        senddata = [0x11]
        send_yes_data_to_student(py_serial, addr, cmd, datalen, senddata) #학생보드로 초성게임 전송
        
        word_label.config(text="3명씩 짝지어 단어를 만드세요!", font=("맑은 고딕", 50), height=9) #"3명씩 짝지어 단어를 만드세요!"라는 문장 출력

#==========================================================지금까지 Korean_go()의 내부함수 정의였습니다===========================================
    
    root.destroy() #메인화면 종료
    
    K_window = tk.Tk()   #초성게임프로그램 생성
    K_window.geometry("1280x960")
   # K_window.resizable(False, False)
    K_window.title("쪼끼쪼끼(3355놀이)-초성게임")
    label_korean = tk.Label(
        K_window, text="원하는 글자수를 선택하세요.", font=("맑은 고딕", 30), height=3 #height는 폰트크기 기준으로 예를들어 height=3이면 
    )                                                                               # 위에서 폰트크기 만한 글자 3개정도가 들어가는 위치에 생성합니다
    label_korean.pack()
    button_label = tk.Label(K_window)
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
    word_label = tk.Label(K_window)
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
    
    # other_game_button = tk.Button(
    #     K_window,           
    #     text="다른 게임 하기",
    #     font=("맑은 고딕", 20),
    #     height=1,
    #     bg="green",
    #     command=KorToRoot,
    # )
    # other_game_button.pack(side="left", anchor="s")

    K_window.mainloop()

#======================================프로그램 실행 시키면 처음 나타나는 메인화면 부분
root = tk.Tk() #root라는 메인화면 생성
root.geometry("1280x960") #메인화면의 크기설정
#root.resizable(False, False)

root.title("쪼끼쪼끼(3355놀이)")

# print(tk.font.families())
label_1 = tk.Label(root, text="쪼끼쪼끼(3355놀이)", font=("맑은 고딕", 30), height=3) #font 맑은고딕으로 크기는30으로 설정후 글자크기만큼의 3칸 아래에 위치
label_1.pack()
label_2 = tk.Label(root, text="원하는 게임의 버튼을 누르세요", font=("맑은 고딕", 20))
label_2.pack()


XO_button = tk.Button(
    root, text="1. XO게임", font=("맑은 고딕", 20), height=1, command=XO_Go #XO게임 버튼 클릭시 XO_Go함수 실행
)
XO_button.pack()
Korean_button = tk.Button(
    root, text="2. 초성게임", font=("맑은 고딕", 20), height=1, command=Korean_go #초성게임 버튼 클릭시 Korean_go함수 실행
)
Korean_button.pack()


root.mainloop()

import tkinter as tk
import tkinter.font
import random

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
]
XO_answer = ["X", "O", "O", "X", "O", "O", "O", "X", "O", "X"]
num = random.randrange(0, 10)


def XO_Go():
    def Root_go():
        window.destroy()
        global root
        root = tk.Tk()
        root.geometry("1280x960")
        #root.resizable(False, False)

        root.title("쪼끼쪼끼(3355놀이)")

        # print(tk.font.families())
        label_1 = tk.Label(root, text="쪼끼쪼끼(3355놀이)", font=("08서울남산체 B", 30), height=3)
        label_1.pack()
        label_2 = tk.Label(root, text="원하는 게임의 버튼을 누르세요", font=("08서울남산체 B", 20))
        label_2.pack()

        XO_button = tk.Button(
            root, text="1. XO게임", font=("08서울남산체 B", 20), height=1, command=XO_Go
        )
        XO_button.pack()
        Korean_button = tk.Button(
            root, text="2. 초성게임", font=("08서울남산체 B", 20), height=1
        )
        Korean_button.pack()

        root.mainloop()

    def check_answer():
        answer_label.config(text=XO_answer[num], font=("08서울남산체 B", 150))

    def next_problem():
        global num
        num = (num + 1) % len(XO_problem)  # 문제 개수에 따라 순환하도록 수정
        label_1.config(text="[문제] " + XO_problem[num])
        answer_label.config(text="?")

    root.destroy()

    window = tk.Tk()
    window.geometry("1280x960")
    #window.resizable(False, False)
    window.title("쪼끼쪼끼(3355놀이)-XO게임")

    label_1 = tk.Label(
        window, text="[문제] " + XO_problem[num], font=("08서울남산체 B", 30), height=3
    )
    label_1.pack()

    answer_label = tk.Label(window, text="?", font=("08서울남산체 B", 150))
    answer_label.place(x=600, y=410)

    next_problem_button = tk.Button(
        window,
        text="다음문제",
        font=("08서울남산체 B", 20),
        height=1,
        bg="yellow",
        command=next_problem,
    )
    next_problem_button.pack(side="right", anchor="s")

    answer_button = tk.Button(
        window,
        text="정답보기",
        font=("08서울남산체 B", 20),
        height=1,
        bg="lightblue",
        command=check_answer,
    )
    answer_button.pack(side="right", anchor="s")

    other_game_button = tk.Button(
        window,
        text="다른 게임 하기",
        font=("08서울남산체 B", 20),
        height=1,
        bg="green",
        command=Root_go,
    )
    other_game_button.pack(side="left", anchor="s")

    window.mainloop()


root = tk.Tk()
root.geometry("1280x960")
#root.resizable(False, False)

root.title("쪼끼쪼끼(3355놀이)")

# print(tk.font.families())
label_1 = tk.Label(root, text="쪼끼쪼끼(3355놀이)", font=("08서울남산체 B", 30), height=3)
label_1.pack()
label_2 = tk.Label(root, text="원하는 게임의 버튼을 누르세요", font=("08서울남산체 B", 20))
label_2.pack()


XO_button = tk.Button(
    root, text="1. XO게임", font=("08서울남산체 B", 20), height=1, command=XO_Go
)
XO_button.pack()
Korean_button = tk.Button(root, text="2. 초성게임", font=("08서울남산체 B", 20), height=1)
Korean_button.pack()


root.mainloop()

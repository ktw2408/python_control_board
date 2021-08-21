# --------------------------------------
# import 영역
# --------------------------------------

import threading
from typing import get_args
import serial
import time 
from tkinter import *
import tkinter.ttk as ttk
from threading import *
import signal

# --------------------------------------
# 프로그램 기본 설정
# --------------------------------------

window = Tk()
window.title('Control Board')
window.geometry("550x380")
window.resizable(False, False)

window_frame = Frame(window)
window_frame.pack(fill="x", padx=5, pady=5)

ser = serial.Serial("COM4", 9600, timeout=5)

#스레드 구간
textEntry = StringVar()
#txt_dest_path = 'txt_dest_path'
exitThread = False   # 쓰레드 종료용 변수
line = []

# --------------------------------------
# 프로그램 동작 영역
# --------------------------------------

#연결 버튼 
def connect_button(): 
      
      if not ser.isOpen():
            ser.open()
      print('COM4 is open', ser.isOpen())
      ser.write(b'connect')

#on, off 버튼 
def button_on(): 
     ser.write(b'a') #버튼을 누르면 LED가 켜짐, 테라텀의 경우 창에 a가 출력
     
def button_off():
      ser.write(b'b') #버튼을 누르면 LED가 꺼짐, 테라텀의 경우 창에 b가 출력

#연결 해제하기
def disconnect_button():
      ser.write(b'disconnect')
      if ser.isOpen():
            ser.close()
      print('COM4 is close')

# --------------------------------------
# 스레드 영역
# --------------------------------------

#데이터 처리할 함수
def parsing_data(data):
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    #print("hello")
    tmp = ''.join(data)
    print(tmp)
    
def readThread():
     global line
     global exitThread

    # 쓰레드 종료될때까지 계속 돌림
     while not exitThread:
        #데이터가 있있다면
        for c in ser.read():
            #line 변수에 차곡차곡 추가하여 넣는다.
            line.append(chr(c))
            
#10
            if c == 13: #라인의 끝을 만나면..
                #데이터 처리 함수로 호출
                parsing_data(line)
                #line 변수 초기화
                del line[:]    
                break
                  
           
#시작 
def start():
      #시리얼 읽을 쓰레드 생성
      thread = threading.Thread(target=readThread, args=(ser,))
      
      #시작!
      thread.start()

#쓰레드 종료용 시그널 함수
def handler(signum, frame):
     exitThread = True

#정지
def stop():
      signal.signal(signal.SIGINT, handler)


# --------------------------------------
# 프레임 영역
# --------------------------------------

#상단 프레임
com_frame = Frame(window)
com_frame.pack(fill="x", padx=5, pady=5, ipady=5)

com_view = Label(com_frame)
com_view.pack(fill="both", side="left", ipadx=30)

#컴포넌트 프레임
con_area = Label(com_frame, text="컴포넌트 선택", width=10)
con_area.pack(side="left")

#컴포넌트 콤보박스
com_values = ["COM"+str(i) for i in range(1, 15)] #COM1~14 까지 나타냄
com_combobox = ttk.Combobox(com_frame, height=5, values=com_values, state="readonly")
com_combobox.pack(side="left", padx=5, pady=5)
com_combobox.set("COM1")

#connect 영역
btn_conn_button = Button(com_frame, padx=5, pady=5, text="Connect", width=8, command=connect_button)
btn_conn_button.pack(side="left", padx=5, pady=5)

#disconnect 버튼
btn_dis_con_button = Button(com_frame, padx=5, pady=5, text="Disconnect", width=8, command=disconnect_button)
btn_dis_con_button.pack(side="left", padx=5, pady=5)

#옵션 프레임 1번 라인
opt_frame = Frame(window)
opt_frame.pack(fill="x", padx=5, pady=5, ipady=5)

opt_view = Label(opt_frame)
opt_view.pack(fill="both", side="left", ipadx=36, ipady=25)

#LED 영역
led_area = Label(opt_frame, text="LED")
led_area.pack(side="left")

#LED 영역 버튼
btn_led_on = Button(opt_frame, text="ON", width=3, command=button_on)
btn_led_on.pack(side="left", fill="x", padx=5, pady=5)

btn_led_off = Button(opt_frame, text="OFF", width=3, command=button_off)
btn_led_off.pack(side="left", fill="x", padx=5, pady=5)

#Valve 영역
valve_area = Label(opt_frame, text="Valve")
valve_area.pack(fill="x", side="left", padx=7)

#Valve 영역 버튼
btn_valve_on = Button(opt_frame, padx=3, pady=3, text="ON", width=3, command=button_on)
btn_valve_on.pack(side="left", padx=5, pady=5)

btn_valve_off = Button(opt_frame, padx=3, pady=3, text="OFF", width=3, command=button_off)
btn_valve_off.pack(side="left", padx=5, pady=5)

#Vent 영역
vent_area = Label(opt_frame, text="Vent")
vent_area.pack(fill="x", side="left", padx=7)

#Vent 영역 버튼
btn_vent_on = Button(opt_frame, padx=3, pady=3, text="ON", width=3, command=button_on)
btn_vent_on.pack(side="left", padx=5, pady=5)

btn_vent_off = Button(opt_frame, padx=3, pady=3, text="OFF", width=3, command=button_off)
btn_vent_off.pack(side="left", padx=5, pady=5)

#옵션 프레임 2번 라인
opt_frame_l2 = Frame(window)
opt_frame_l2.pack(fill="x", padx=5, pady=5, ipady=5)

opt_view_l2 = Label(opt_frame_l2)
opt_view_l2.pack(fill="both", side="left", ipadx=25, ipady=25)

#Comp 영역
comp_area = Label(opt_frame_l2, text="Comp")
comp_area.pack(side="left")

#Comp 영역 버튼
btn_comp_on = Button(opt_frame_l2, text="ON", width=3, command=button_on)
btn_comp_on.pack(side="left", fill="x", padx=5, pady=5)

btn_comp_off = Button(opt_frame_l2, text="OFF", width=3, command=button_off)
btn_comp_off.pack(side="left", fill="x", padx=5, pady=5)

#HVPS 영역
hvps_area = Label(opt_frame_l2, text="HVPS")
hvps_area.pack(fill="x", side="left", padx=7)

#HVPS 영역 버튼
btn_hvps_on = Button(opt_frame_l2, padx=3, pady=3, text="ON", width=3, command=button_on)
btn_hvps_on.pack(side="left", padx=5, pady=5)

btn_hvps_off = Button(opt_frame_l2, padx=3, pady=3, text="OFF", width=3, command=button_off)
btn_hvps_off.pack(side="left", padx=5, pady=5)

#Dac_Vref 영역
dac_vref_area = Label(opt_frame_l2, text="Dac_Vref")
dac_vref_area.pack(fill="x", side="left", padx=7)

#Dac_Vref 영역 버튼
btn_dac_vref_on = Button(opt_frame_l2, padx=3, pady=3, text="ON", width=3, command=button_on)
btn_dac_vref_on.pack(side="left", padx=5, pady=5)

btn_dac_vref_off = Button(opt_frame_l2, padx=3, pady=3, text="OFF", width=3, command=button_off)
btn_dac_vref_off.pack(side="left", padx=5, pady=5)

#하위 영역(센서, Read, Start, Stop)
bottom_frame = Frame(window)
bottom_frame.pack(fill="x", padx=5, pady=5, ipady=5)

bottom_view = Label(bottom_frame)
bottom_view.pack(fill="both", side="left", ipadx=10)

#센서
sensor_area = Label(bottom_frame, text="Sensor", width=10)
sensor_area.pack(side="left")

txt_dest_path = Entry(bottom_frame, textvariable= textEntry)
txt_dest_path.pack(side="left", fill="x", padx=5, pady=5)

#Read
btn_read = Button(bottom_frame, text="Read", width=10, command=readThread)
btn_read.pack(side="left", padx=3)

#Start
btn_start = Button(bottom_frame, text="Start", width=10, command=start)
btn_start.pack(side="left", padx=3)

#Stop
btn_stop = Button(bottom_frame, text="Stop", width=10, command=stop)
btn_stop.pack(side="left", padx=3)


window.mainloop()


        
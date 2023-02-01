import cv2
import os
import time
import pyautogui
import numpy as np
import socket  # 소켓 프로그래밍에 필요한 API를 제공하는 모듈
import pickle  # ﻿객체의 직렬화 및 역직렬화 지원 모듈﻿
import struct  # 바이트(bytes) 형식의 데이터 처리 모듈
import threading
from PIL import ImageGrab
import mss

s_x = 0
s_y = 0
e_x = 1920
e_y = 1080
p_x = 0
p_y = 0

count = 0
flag = 0

def send(sock):
    while True:
        senddata = input('')
        sock.send(senddata.encode('utf-8'))
        if senddata == 'q':
            client_socket.close()

def receive(sock):
    global flag,p_x,p_y,s_x,s_y,e_x,e_y
    while True:
        recvdata = sock.recv(1024)
        pos = recvdata.decode('utf-8')
        #print('pos >> ', pos)#recvdata.decode('utf-8'))
        temp = pos.count('a')

        if temp == 1:   # mouse click
            pos = pos.split('a')
            p_x = int(pos[0])
            p_y = int(pos[1])
            s_x = 0
            s_y = 0
            e_x = 1920
            e_y = 1080
            flag = 1

        elif temp == 3:   # mouse drag
            pos = pos.split('a')
            s_x = int(pos[0])
            s_y = int(pos[1])
            e_x = int(pos[2])
            e_y = int(pos[3])
            flag = 2

        #print(pos)
        #print('x >> ', s_x, e_x)
        #print('y >> ', s_y, e_y)

def panorama(sock):
    os.chdir('/home/ypelec2022/Desktop/pano')
    os.system('/home/ypelec2022/Desktop/pano/PANORAMA/pano_exe_showFull /home/ypelec2022/Desktop/pano/pano_param.yaml')
    print('end panorama program')

ip = '192.168.211.61'
port = 50001

ESC_KEY = 115
FRAME_RATE = 120
SLEEP_TIME = 1/FRAME_RATE




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # 서버와 연결
    client_socket.connect((ip, port))

    print("연결 성공")

    sender = threading.Thread(target=send, args=(client_socket,))
    receiver = threading.Thread(target=receive, args=(client_socket,))
    pano_program = threading.Thread(target=panorama, args=(client_socket,))
    sender.start()
    receiver.start()
    pano_program.start()

    while True:
        #print("flag >> ", flag)
        #start = time.time()
        frame = pyautogui.screenshot(region=(s_x,s_y,e_x,e_y))
        #frame = ImageGrab.grab()
        #with mss.mss() as sct:
            #frame = sct.shot()
        frame = np.array(frame)
        #frame = cv2.resize(frame, dsize=(720, 480), interpolation=cv2.INTER_AREA)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if flag == 3:
            cv2.putText(frame, str(p_x)+', '+str(p_y), (100,80), cv2.FONT_HERSHEY_PLAIN, 3, (150,50,100), 4)
        #mid = time.time()-start
        #print('mid = ')
        #print(mid)
        retval, frame1 = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        #frame = np.array(frame)
        # dumps : 데이터를 직렬화
        # - 직렬화(serialization) : 효율적으로 저장하거나 스트림으로 전송할 때 데이터를 줄로 세워 저장하는 것
        frame2 = pickle.dumps(frame1)

        #print("전송 프레임 크기 : {} bytes".format(len(frame2)))

        client_socket.sendall(struct.pack(">L", len(frame2)) + frame2)

        #end = time.time() - start
        #print('end = ')
        #print(end)

        if flag == 0:
            count = 0
            s_x = 0
            s_y = 0
            e_x = 1920
            e_y = 1080
            p_x = -1
            p_y = -1

        elif flag == 1:
            flag = 3
            count = 0

        elif flag == 2:
            flag = 4
            count = 0

        elif flag == 3 or flag == 4:
            count = count + 1

        if count > 10:
            flag = 0

        '''
        if end < SLEEP_TIME:
            time.sleep(SLEEP_TIME-end)
        key = cv2.waitKey(1) & 0xFF
        if key == ESC_KEY:
            break
        '''
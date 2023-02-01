import cv2
import os
import time
import pyautogui
import numpy as np
import socket
import pickle
import struct
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

def panorama(sock):
    os.chdir('/home/ypelec2022/Desktop/pano')
    os.system('/home/ypelec2022/Desktop/pano/PANORAMA/pano_exe_showFull /home/ypelec2022/Desktop/pano/pano_param.yaml')
    print('end panorama program')

ip = '192.168.211.61'
port = 50001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    client_socket.connect((ip, port))

    print("연결 성공")

    sender = threading.Thread(target=send, args=(client_socket,))
    receiver = threading.Thread(target=receive, args=(client_socket,))
    pano_program = threading.Thread(target=panorama, args=(client_socket,))
    sender.start()
    receiver.start()
    pano_program.start()

    while True:

        frame = pyautogui.screenshot(region=(s_x,s_y,e_x,e_y))
        frame = np.array(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if flag == 3:
            cv2.putText(frame, str(p_x)+', '+str(p_y), (100,80), cv2.FONT_HERSHEY_PLAIN, 3, (150,50,100), 4)

        retval, frame1 = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        frame2 = pickle.dumps(frame1)

        client_socket.sendall(struct.pack(">L", len(frame2)) + frame2)

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
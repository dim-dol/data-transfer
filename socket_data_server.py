import socket
import struct
import pickle
import threading

import cv2


mouse_pressed = False
s_x = s_y = e_x = e_y = p_x = p_y = -1
drag_status = -1

def mouse_click(event,x,y,flags,param):
    global s_x,s_y,e_x,e_y,p_x,p_y,mouse_pressed, drag_status

    if event==cv2.EVENT_LBUTTONDOWN:
        mouse_pressed = True
        s_x, s_y = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_pressed: #drag
            drag_status = 1
        else:
            p_x, p_y = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        mouse_pressed = False
        e_x,e_y = x,y

        pos = str(s_x) + 'a' + str(s_y)

        if drag_status == 1:
            print("드래그 x: ", s_x, " ~ ", e_x, " y: ", s_y, " ~ ", e_y)
            drag_status = 0
            pos = pos + 'a' + str(e_x) + 'a' + str(e_y)

        client_socket.send(pos.encode('utf-8'))


# 서버 ip 주소 및 port 번호
ip = '192.168.211.61'
port = 50001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, port))
server_socket.listen(10)

print('Client 연결 대기')

client_socket, address = server_socket.accept()
print('Client ip address :', address[0])

data_buffer = b""

data_size = struct.calcsize("L")

while True:

    while len(data_buffer) < data_size:
        # 데이터 수신
        data_buffer += client_socket.recv(4096)

    packed_data_size = data_buffer[:data_size]
    data_buffer = data_buffer[data_size:]

    frame_size = struct.unpack(">L", packed_data_size)[0]

    while len(data_buffer) < frame_size:
        data_buffer += client_socket.recv(4096)


    frame_data = data_buffer[:frame_size]
    data_buffer = data_buffer[frame_size:]

    frame = pickle.loads(frame_data)

    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame = cv2.resize(frame,(1920,1080), interpolation=cv2.INTER_NEAREST)

    # 프레임 출력
    cv2.namedWindow('Frame', cv2.WND_PROP_FULLSCREEN)
    cv2.setMouseCallback('Frame', mouse_click)
    cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    key = cv2.waitKey(1)
    cv2.imshow('Frame', frame)

    # 'q' 키를 입력하면 종료
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

client_socket.close()
server_socket.close()
print('연결 종료')

cv2.destroyAllWindows()
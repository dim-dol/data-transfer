import cv2  # OpenCV(실시간 이미지 프로세싱) 모듈
import socket  # 소켓 프로그래밍에 필요한 API를 제공하는 모듈
import pickle  # ﻿객체의 직렬화 및 역직렬화 지원 모듈﻿
import struct  # 바이트(bytes) 형식의 데이터 처리 모듈

# 서버 ip 주소 및 port 번호
ip = '192.168.0.10'
port = 50001

# 카메라 또는 동영상
capture = cv2.VideoCapture(0)

# 프레임 크기 지정
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 가로
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 세로

# 소켓 객체 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # 서버와 연결
    client_socket.connect((ip, port))

    print("연결 성공")

    # 메시지 수신
    while True:
        # 프레임 읽기
        retval, frame = capture.read()

        retval, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

        # dumps : 데이터를 직렬화
        # - 직렬화(serialization) : 효율적으로 저장하거나 스트림으로 전송할 때 데이터를 줄로 세워 저장하는 것
        frame = pickle.dumps(frame)

        #print("전송 프레임 크기 : {} bytes".format(len(frame)))

        client_socket.sendall(struct.pack(">L", len(frame)) + frame)

# 메모리를 해제
capture.release()
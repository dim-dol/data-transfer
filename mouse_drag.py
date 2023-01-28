import cv2
import time
import pyautogui

mouse_pressed = False
s_x = s_y = e_x = e_y = p_x = p_y = -1
drag_status = -1

def mouse_click(event,x,y,flags,param):
    global s_x,s_y,e_x,e_y,mouse_pressed, drag_status

    if event==cv2.EVENT_LBUTTONDOWN:
        mouse_pressed = True
        s_x, s_y = x,y


    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_pressed: #drag
            drag_status = 1
        else:
            p_x, p_y = x,y
            print("마우스 위치  x: ", p_x, " y: ", p_y)

    elif event == cv2.EVENT_LBUTTONUP:
        mouse_pressed = False
        e_x,e_y = x,y
        print("마우스 클릭  x: ", s_x, " ~ ", e_x, " y: ", s_y, " ~ ", e_y)


cap = cv2.VideoCapture(0)

cv2.namedWindow('test')
cv2.setMouseCallback('test',mouse_click)

if cap.isOpened():
    # 만약 카메라가 실행되고 있다면,
    ret, a = cap.read()

    while ret:
        # 제대로 카메라를 불러왔다면~ 반복문을 실행합니다.
        ret, a = cap.read()
        cv2.imshow("test", a)
        # 이미지를 보여주는 방식과 같습니다.

        if cv2.waitKey(1) & 0xFF == 27:
            break
        # 종료 커맨드.

cap.release()


cv2.destroyAllWindows()




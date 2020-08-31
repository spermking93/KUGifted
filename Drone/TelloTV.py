from djitellopy import Tello
import cv2
import numpy as np
import time
import datetime
import os
import argparse

# 표준 argparse 관련 코드
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='** = required')
parser.add_argument('-d', '--distance', type=int, default=3,
    help='use -d to change the distance of the drone. Range 0-6')
parser.add_argument('-sx', '--saftey_x', type=int, default=100,
    help='use -sx to change the saftey bound on the x axis . Range 0-480')
parser.add_argument('-sy', '--saftey_y', type=int, default=55,
    help='use -sy to change the saftey bound on the y axis . Range 0-360')
parser.add_argument('-os', '--override_speed', type=int, default=1,
    help='use -os to change override speed. Range 0-3')
parser.add_argument('-ss', "--save_session", action='store_true',
    help='add the -ss flag to save your session as an image sequence in the Sessions folder')
parser.add_argument('-D', "--debug", action='store_true',
    help='add the -D flag to enable debug mode. Everything works the same, but no commands will be sent to the drone')

args = parser.parse_args()

# 드론의 속도
S = 20
S2 = 5
UDOffset = 150

# openCV가 생성하는 얼굴 인식 상자의 크기
faceSizes = [1026, 684, 456, 304, 202, 136, 90]

# 가속 시키는 값입니다. 다만 이 값들은 최종화되지 않았기에 주의 바람.
acc = [500,250,250,150,110,70,50]

# pygame 창의 fps 지정
FPS = 25
dimensions = (960, 720)

# 얼굴 인식 데이터
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_tellotv.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# 세션을 저장한다면, 디렉토리가 있는지 확인.
if args.save_session:
    ddir = "Sessions"

    if not os.path.isdir(ddir):
        os.mkdir(ddir)

    ddir = "Sessions/Session {}".format(str(datetime.datetime.now()).replace(':','-').replace('.','_'))
    os.mkdir(ddir)

#object 클래스를 상속받은 FrontEnd 클래스
class FrontEnd(object):
    
    def __init__(self):
       
        # 드론과 상호작용하는 Tello 객체
        self.tello = Tello()

        # 드론의 속도 (-100~100)
        #수직, 수평 속도
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False
        # 실행 함수
    def run(self):
        #드론이 연결이 되지 않으면 함수 종료
        if not self.tello.connect():
            print("Tello not connected")
            return
        #drone의 제한속도가 적절하지 않은 경우
        if not self.tello.set_speed(self.speed):
            print("Not set speed to lowest possible")
            return

        # 프로그램을 비정상적인 방법으로 종료를 시도하여 비디오 화면이 꺼지지 않은 경우 종료.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        # 비디오가 켜지지않는 경우 종료.
        if not self.tello.streamon():
            print("Could not start video stream")
            return

        #프레임 단위로 인식
        frame_read = self.tello.get_frame_read()

        should_stop = False
        imgCount = 0
        OVERRIDE = False
        oSpeed = args.override_speed
        tDistance = args.distance
        self.tello.get_battery()
        
        # X축 안전 범위
        szX = args.saftey_x

        # Y축 안전 범위
        szY = args.saftey_y
        
        #디버깅 모드
        if args.debug:
            print("DEBUG MODE ENABLED!")

        #비행을 멈취야할 상황이 주어지지 않은 경우
        while not should_stop:
            self.update()
            #프레임 입력이 멈췄을 경우 while문 탈출
            if frame_read.stopped:
                frame_read.stop()
                break

            theTime = str(datetime.datetime.now()).replace(':','-').replace('.','_')

            frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
            frameRet = frame_read.frame

            vid = self.tello.get_video_capture()
            #저장할 경우
            if args.save_session:
                cv2.imwrite("{}/tellocap{}.jpg".format(ddir,imgCount),frameRet)
            
            frame = np.rot90(frame)
            imgCount+=1

            time.sleep(1 / FPS)

            # 키보드 입력을 기다림
            k = cv2.waitKey(20)

            # 0을 눌러서 거리를 0으로 설정
            if k == ord('0'):
                if not OVERRIDE:
                    print("Distance = 0")
                    tDistance = 0

            # 1을 눌러서 거리를 1으로 설정
            if k == ord('1'):
                if OVERRIDE:
                    oSpeed = 1
                else:
                    print("Distance = 1")
                    tDistance = 1

            # 2을 눌러서 거리를 2으로 설정
            if k == ord('2'):
                if OVERRIDE:
                    oSpeed = 2
                else:
                    print("Distance = 2")
                    tDistance = 2
                    
            # 3을 눌러서 거리를 3으로 설정
            if k == ord('3'):
                if OVERRIDE:
                    oSpeed = 3
                else:
                    print("Distance = 3")
                    tDistance = 3
            
            # 4을 눌러서 거리를 4으로 설정
            if k == ord('4'):
                if not OVERRIDE:
                    print("Distance = 4")
                    tDistance = 4
                    
            # 5을 눌러서 거리를 5으로 설정
            if k == ord('5'):
                if not OVERRIDE:
                    print("Distance = 5")
                    tDistance = 5
                    
            # 6을 눌러서 거리를 6으로 설정
            if k == ord('6'):
                if not OVERRIDE:
                    print("Distance = 6")
                    tDistance = 6

            # T를 눌러서 이륙
            if k == ord('t'):
                if not args.debug:
                    print("Taking Off")
                    self.tello.takeoff()
                    self.tello.get_battery()
                self.send_rc_control = True

            # L을 눌러서 착륙
            if k == ord('l'):
                if not args.debug:
                    print("Landing")
                    self.tello.land()
                self.send_rc_control = False

            # Backspace를 눌러서 명령을 덮어씀
            if k == 8:
                if not OVERRIDE:
                    OVERRIDE = True
                    print("OVERRIDE ENABLED")
                else:
                    OVERRIDE = False
                    print("OVERRIDE DISABLED")

            if OVERRIDE:
                # S & W 눌러서 앞 & 뒤로 비행
                if k == ord('w'):
                    self.for_back_velocity = int(S * oSpeed)
                elif k == ord('s'):
                    self.for_back_velocity = -int(S * oSpeed)
                else:
                    self.for_back_velocity = 0

                # a & d 를 눌러서 왼쪽 & 오른쪽으로 회전
                if k == ord('d'):
                    self.yaw_velocity = int(S * oSpeed)
                elif k == ord('a'):
                    self.yaw_velocity = -int(S * oSpeed)
                else:
                    self.yaw_velocity = 0

                # Q & E 를 눌러서 위 & 아래로 비행
                if k == ord('e'):
                    self.up_down_velocity = int(S * oSpeed)
                elif k == ord('q'):
                    self.up_down_velocity = -int(S * oSpeed)
                else:
                    self.up_down_velocity = 0

                # c & z 를 눌러서 왼쪽 & 오른쪽으로 비행
                if k == ord('c'):
                    self.left_right_velocity = int(S * oSpeed)
                elif k == ord('z'):
                    self.left_right_velocity = -int(S * oSpeed)
                else:
                    self.left_right_velocity = 0

            # 프로그램 종료
            if k == 27:
                should_stop = True
                break

            gray  = cv2.cvtColor(frameRet, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=2)

            # 대상 크기
            tSize = faceSizes[tDistance]

            # 중심 차원들
            cWidth = int(dimensions[0]/2)
            cHeight = int(dimensions[1]/2)

            noFaces = len(faces) == 0

            # 컨트롤을 얻고, 얼굴 좌표 등을 얻으면
            if self.send_rc_control and not OVERRIDE:
                for (x, y, w, h) in faces:

                    # 
                    roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
                    roi_color = frameRet[y:y+h, x:x+w]

                    # 얼굴 상자 특성 설정
                    fbCol = (255, 0, 0) #BGR 0-255 
                    fbStroke = 2
                    
                    # 끝 좌표들은 x와 y를 제한하는 박스의 끝에 존재
                    end_cord_x = x + w
                    end_cord_y = y + h
                    end_size = w*2

                    # 목표 좌표들
                    targ_cord_x = int((end_cord_x + x)/2)
                    targ_cord_y = int((end_cord_y + y)/2) + UDOffset

                    # 얼굴에서 화면 중심까지의 벡터를 계산
                    vTrue = np.array((cWidth,cHeight,tSize))
                    vTarget = np.array((targ_cord_x,targ_cord_y,end_size))
                    vDistance = vTrue-vTarget

                    # 
                    if not args.debug:

                        # 회전
                        if vDistance[0] < -szX:
                            self.yaw_velocity = S
                            # self.left_right_velocity = S2
                        elif vDistance[0] > szX:
                            self.yaw_velocity = -S
                            # self.left_right_velocity = -S2
                        else:
                            self.yaw_velocity = 0
                        
                        # 위 & 아래 (상승/하강)
                        if vDistance[1] > szY:
                            self.up_down_velocity = S
                        elif vDistance[1] < -szY:
                            self.up_down_velocity = -S
                        else:
                            self.up_down_velocity = 0

                        F = 0
                        if abs(vDistance[2]) > acc[tDistance]:
                            F = S

                        # 앞, 뒤
                        if vDistance[2] > 0:
                            self.for_back_velocity = S + F
                        elif vDistance[2] < 0:
                            self.for_back_velocity = -S - F
                        else:
                            self.for_back_velocity = 0

                    # 얼굴 테두리 박스를 그림
                    cv2.rectangle(frameRet, (x, y), (end_cord_x, end_cord_y), fbCol, fbStroke)

                    # 목표를 원으로 그림
                    cv2.circle(frameRet, (targ_cord_x, targ_cord_y), 10, (0,255,0), 2)

                    # 안전 구역을 그림
                    cv2.rectangle(frameRet, (targ_cord_x - szX, targ_cord_y - szY), (targ_cord_x + szX, targ_cord_y + szY), (0,255,0), fbStroke)

                    # 드론의 얼굴 상자로부터의 상대적 벡터 위치를 구함.
                    cv2.putText(frameRet,str(vDistance),(0,64),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

                # 인식되는 얼굴이 없으면 아무것도 안함.
                if noFaces:
                    self.yaw_velocity = 0
                    self.up_down_velocity = 0
                    self.for_back_velocity = 0
                    print("NO TARGET")

            # 화면의 중심을 그림. 드론이 목표 좌표와 맞추려는 대상이 됨.
            cv2.circle(frameRet, (cWidth, cHeight), 10, (0,0,255), 2)

            dCol = lerp(np.array((0,0,255)),np.array((255,255,255)),tDistance+1/7)

            if OVERRIDE:
                show = "OVERRIDE: {}".format(oSpeed)
                dCol = (255,255,255)
            else:
                show = "AI: {}".format(str(tDistance))

            # 선택된 거리를 그림
            cv2.putText(frameRet,show,(32,664),cv2.FONT_HERSHEY_SIMPLEX,1,dCol,2)

            # 결과 프레임을 보여줌.
            cv2.imshow(f'Tello Tracking...',frameRet)

        # 종료시에 배터리를 출력
        self.tello.get_battery()

        # 전부 완료되면 캡쳐를 해제함.
        cv2.destroyAllWindows()

        # 종료 전에 항상 호출. 자원들을 해제함.
        self.tello.end()


    def battery(self):
        return self.tello.get_battery()[:2]

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)

def lerp(a,b,c):
    return a + c*(b-a)

def main():
    #frontend 객체 생성
    frontend = FrontEnd()

    # run 함수를 실행
    frontend.run()


if __name__ == '__main__':
    main()
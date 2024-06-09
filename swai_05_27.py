# OpenCV(Open Source Computer Vision Library) : 
# 영상처리, 컴퓨터 비전 및 머신러닝 분야에서 사용되는 오픈소스 라이브러리
import cv2

# MediaPipe : 
# 컴퓨터 비전과 머신러닝을 이용하여 영상 및 오디오 데이터를 처리할 수 있는 Google에서 개발한 오픈소스 라이브러리
import mediapipe as mp

# MediaPipe의 Pose(몸 인식) 모델 로드
mp_pose = mp.solutions.pose.Pose()
mp_drawing_utils = mp.solutions.drawing_utils

LEFT_SHOULDER = mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value
RIGHT_SHOULDER = mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value
LEFT_HIP = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
RIGHT_HIP = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value

# VideoCapture() : 카메라 객체 생성
camera = cv2.VideoCapture(0)

while True:
    # read() : 카메라 객체에서 프레임 읽기
    result, frame = camera.read()

    # 읽은 프레임이 없는 경우 종료
    if not result:
        break

    # flip() : 프레임 반전
    frame = cv2.flip(frame, 1)

    # process() : 몸 인식
    results = mp_pose.process(frame)

    # 프레임에서 몸을 인식한 경우
    if results.pose_landmarks:
        # 랜드마크와 연결선을 프레임에 그리기
        mp_drawing_utils.draw_landmarks(
            frame, 
            results.pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS
        )

        left_shoulder = results.pose_landmarks.landmark[LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[RIGHT_SHOULDER]
        left_hip = results.pose_landmarks.landmark[LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[RIGHT_HIP]

        if 0 < left_shoulder.x < 1 and 0 < left_shoulder.y < 1 and \
           0 < right_shoulder.x < 1 and 0 < right_shoulder.y < 1 and \
           0 < left_hip.x < 1 and 0 < left_hip.y < 1 and \
           0 < right_hip.x < 1 and 0 < right_hip.y < 1:
            
            if abs(left_shoulder.y - right_shoulder.y) < 0.05 and \
               abs(left_shoulder.z - right_shoulder.z) < 0.2 and \
               abs(left_hip.z - right_hip.z) < 0.2 and \
               abs(left_shoulder.z - left_hip.z) < 0.45 and \
               abs(right_shoulder.z - right_hip.z) < 0.45:
                cv2.putText(frame, "Good", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Bad", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # imshow() : 윈도우 창에 프레임 출력
    cv2.imshow("frame", frame)
    
    # 'ESC' 를 입력하면 종료
    if cv2.waitKey(5) == 27:
        break

# 카메라 객체 해제
camera.release()

# 모든 윈도우 창 닫음
cv2.destroyAllWindows()
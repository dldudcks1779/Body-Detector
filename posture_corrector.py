import mediapipe as mp

mp_pose = mp.solutions.pose.Pose()

NOSE = mp.solutions.pose.PoseLandmark.NOSE.value
LEFT_SHOULDER = mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value
RIGHT_SHOULDER = mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value
LEFT_HIP = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
RIGHT_HIP = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value

def posture_corrector(frame):
    results = mp_pose.process(frame)

    if results.pose_landmarks:
        nose = results.pose_landmarks.landmark[NOSE]
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
               abs(right_shoulder.z - right_hip.z) < 0.45 and \
               0.12 < abs(left_hip.z - left_shoulder.z) < 0.45 and \
               0.12 < abs(right_hip.z - right_shoulder.z) < 0.45:                
                print("바른 자세")
            else:
                if 0.12 < abs(left_hip.z - left_shoulder.z) and 0.12 < abs(right_hip.z - right_shoulder.z):
                    print("누웠을 때")
                    b = (int(abs(left_hip.z - left_shoulder.z) * 10) + int(abs(right_hip.z - right_shoulder.z) + 100)) // 2
                    
                    if abs(left_shoulder.y - right_shoulder.y) > 0.05:
                        print("어깨 기울어짐")
                        if left_shoulder.y < right_shoulder.y:
                            a = int(abs((right_shoulder.y - left_shoulder.y) * 100))
                        else:
                            a = int(abs((left_shoulder.y - right_shoulder.y) * 100))
                    
                elif abs(left_hip.z - left_shoulder.z) < 0.45 and abs(right_hip.z - right_shoulder.z) < 0.45:
                    print("구부렸을 때")
                    b = (int(abs(left_hip.z - left_shoulder.z) * 100) + int(abs(right_hip.z - right_shoulder.z) + 100)) // 2
                    
                    if abs(left_shoulder.y - right_shoulder.y) > 0.05:
                        print("어깨 기울어짐")
                        if left_shoulder.y < right_shoulder.y:
                            a = int(abs((right_shoulder.y - left_shoulder.y) * 100))
                        else:
                            a = int(abs((left_shoulder.y - right_shoulder.y) * 100))
        else:
            print("인식 안됨")


#opencvtest.py

import cv2
cap = cv2.VideoCapture(1)
cap.set(3, 1600) #WIDTH
cap.set(4, 900) #HEIGHT

#얼굴 인식 캐스케이드 파일 읽는다
face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')

while(True):
    # frame 별로 capture 한다
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #인식된 얼굴 갯수를 출력
    print(len(faces))

    # 인식된 얼굴에 사각형을 출력한다
    for (x,y,w,h) in faces:
         cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    #화면에 출력한다
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


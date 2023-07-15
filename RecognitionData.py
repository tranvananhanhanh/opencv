import cv2
import numpy as np
from PIL import Image
import queryDB as db
from time import sleep
from gtts import gTTS
import time
import os

#khoi tao webcam do phan giai 732*720
cam=cv2.VideoCapture(0)
cam.set(3,732)
cam.set(4,720)

#khoi tao mot doi tuong trong opencv voi tep tin XML chua thong tin ve mo hinh Cascade de phat hiien khuon mat tren hinh anh dau vao
face_cascade=cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
#tao mot doi tuong nhan dien khuon mat bang thuat toan LBPH
recognizer=cv2.face.LBPHFaceRecognizer_creat()
#dung de doc du lieu train tu tep
recognizer.read('recognizer/trainningData.yml')
imgBackground=cv2.imread('image/background.png')

modelType=3
last_time_checked = time.time()

fontface=cv2.FONT_HERSHEY_SIMPLEX

floderModePath= 'image'
modelPathList = os.listdir(folderModePath)
imgModeList=[]

for path in modelPathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

#vong lap vo han de lay lien tuc hinh anh tu camera
while(True):
    # cam.read() la ham de doc hinh anh tu camera va luu tru vao bien frame
    ret, frame =cam.read()
    #doi kich thuoc cua hinh anh 
    frame_resized=cv2.rezie(frame,(732,720))
    imgBackground[0:0+720,0:0+732]=frame_resized
    imgBackground[44:44 + 634,800:800 + 414] = imgModeList[modeType]

    #chuyen doi hinh anh mau sang do xam de don gian trong viec phat hien khuon mat 
    gray=cv2.cvtColor(imgBackground,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray)

    if len(faces)==0:
        modeType=3
    else :
        for(x,y,w,h) in faces:
            #ve hcn xung quanh khuon mat duoc phat hien
            cv2.rectangle(imgBackground,(x,y),(x+w,y+h),(0,255,0),2)
            #thuc hien nhan dien khuon mat va xac dinh nguoi do bang cach so sanh khuon mat phat hien tu cam voi cac khuon mat duoc train tu truoc do
            roi_gray= gray[y:y+h,x:x+w]
            #ket qua nay tra ve la id va confidence 
            id,confidence= recognizer.predict(roi_gray)

            if confidence <40 :
                #goi den ham getProfile de lay thong tin 
                profile=db.getProfile(id)
                #neu profile ma rong thi hien thii ten
                if(profile!=None):
                    #hien thi ten ra khung cam 
                    cv2.putText(imgBackground,""+str(profile[1]),(x+10,y+h-30),fontFace,1,(0,255,0),2)
                    cv2.putText(imgBackground,""+str(100-round(confidence))+"%",(x+10,y-10),fontface,1,(0,255,0),2)
                    current_time= time.time()
                    if(current_time - last_time_checked)>=3:
                        #goi den ham checkin
                        check = db.checkInAndCheckOut(profile[0])
                        if check :
                            modelType=1
                        else:
                            modelType=2
                        elapsed_time = current_time - last_time_checked
                        last_time_checked = current_time
                        minutes = int(elapsed_time//60)
                        seconds = elapsed_time %60
                    else:
                        cv2.putText(imgBackground,"unknow",(x+10,y+h+30),fontface,1,(0,0,255),2)
                        modelType=4

    cv2.imshow(" nhan dien khuon mat ",imgBackground)
    if cv2.waitKey(1)==ord('q'):
        break;
cam.release()
cv2.destroyAllWindows()
                        
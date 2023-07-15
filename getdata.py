import cv2
import numpy as np
import os
import queryDB as db

#Nhap id va tên
id=input("Nhap id ")
name=input("Nhap ten ")
#Goi hamf InsertOrUpdate để lưu trữ thông tin
db.InsertOrUpdate(id,name)

#Khoi tao webcam va cai dat do phan giai 1280x720
cam=cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,720)
#Khoi tao mot doi tuong CascadeClassifier trong thu vien OpenCV voi tap tin XML chứa thông tin về mô hình
#Cascade để phát hiện khuôn mặt trên hình ảnh đầu vào
detector=cv2.CascadeClassifier(*****)

#Số lượng ảnh được chụp
sampleNum=0


while(True):
    #Đọc dữ liệu video từ máy ảnh và lưu trữ khung hình trong biến img
    ret,img=cam.read()
    #Chuyển đổi hình ảnh màu sang độ xám
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #Phát hiện khuôn mặt trong hình ảnh thang độ xám
    faces=detector.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        #Vẽ một hình chữ nhật xung quanh khuôn mặt được phát hiện 
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        #Tạo thư mục dataSet 
        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')

        sampleNum=sampleNum+1
        #Lưu khuôn mặt được phát hiện vào tệp dataSet
        cv2.imwrite("dataSet/User "+id+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.imshow('frame',img)

    #Nhấn phím q để kết thúc
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #Dừng chương trình khi đủ 250 ảnh
    elif sampleNum>250:
        break    
#Giải phóng máy ảnh
cam.release()
cv2.destroyAllWindows()





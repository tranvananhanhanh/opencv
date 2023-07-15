import cv2
import os
import numpy as np
from PIL import Image
#tao ra mt doi tuong nhan dang khuon mat bang thuat toan LBPH
recognizer=cv2.face.LBPHFaceRecognizer_creat()
#duong dan den thu muc chua hinh anh khuon mat
path='dataset'



# Ham nay doc cac hinh anh khuon mat tu thu muc
# ham nay tra ve Id cua nguoi trong anh kem hinh anh tuong ung
def getImagesandLabels(path):
    #sudung modun os de lay danh sach tat ca 
    imagePaths=[os.path.join(path,f)for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.waitkey(1)
    return IDs, faces

# ham nay goi ham getImagesandLabels 
def trainData():
    Ids,faces=getImagesandLabels(path)
    #su dung phuong thuc train cua recognizer
    recognizer.train(faces,np.array(Ids))
    #luu vao tep trainningData.yml
    recognizer.save('recognizer/traiinningData.yml')
    print('train success')



trainData()
cv2.destroyAllWindows()


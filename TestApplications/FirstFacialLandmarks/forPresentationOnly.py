import cv2
import dlib
import sys
import pdb
import numpy as np
from matplotlib import pyplot as plt
import imutils
from imutils import face_utils
from PIL import Image


PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
profile_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_profileface_default.xml')

def sobel (im):
    im = cv2.Sobel(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY),cv2.CV_64F,0,1,ksize=5)
    return im;

def laplace(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# remove noise
    im = cv2.GaussianBlur(gray,(3,3),0)
# convolute with proper kernels
    laplacian = cv2.Laplacian(im,cv2.CV_64F)
    return laplacian



def get_faces (copy, im, target):
    face = face_cascade.detectMultiScale(copy, 1.3, 5)
    
    for(x,y,w,h) in face:
        x = int(round(x*0.9))
        y = int(round(y*0.6))
        w = int(round(w*1.5))
        h = int(round(h*1.7))



        crop_img = copy[y:y+h,x:x+w]
        target[y:y+crop_img.shape[0], x:x+crop_img.shape[1]] = crop_img
        roi = im [y:y+h, x:x+w]
        eye = eye_cascade.detectMultiScale(roi,minNeighbors = 3)
    return im





def get_facial_convex(im, target):
    image = im;
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    out_face = np.zeros_like(image)

    # initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    
    # detect faces in the grayscale image
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
       
        shape = predictor(gray, rect)
        array = []
        for x in range(0,shape.num_parts):
            point = []
            point.append(shape.part(x).x)
            point.append(shape.part(x).y)
            array.append(point)
        
        shape = face_utils.shape_to_np(shape)
        
        remapped_shape = np.zeros_like(shape)
        feature_mask = np.zeros((image.shape[0], image.shape[1]))     
      
        remapped_shape = face_remap(shape)
        
        cv2.fillConvexPoly(feature_mask, remapped_shape[0:27], 1)
        feature_mask = feature_mask.astype(np.bool)



       # out_face[feature_mask] = image[feature_mask]
       
       # img.past


    cv2.imshow()
        #target[y:y+crop_img.shape[0], x:x+crop_img.shape[1]] = crop_img
     #   cv2.imshow("mask_inv", out_face)
     #   cv2.waitKey(0)
#        cv2.imwrite("out_face.png", out_face)
    return 0;


def face_remap(shape):
   remapped_image = shape.copy()
   # left eye brow
   remapped_image[17] = shape[26]
   remapped_image[18] = shape[25]
   remapped_image[19] = shape[24]
   remapped_image[20] = shape[23]
   remapped_image[21] = shape[22]
   # right eye brow
   remapped_image[22] = shape[21]
   remapped_image[23] = shape[20]
   remapped_image[24] = shape[19]
   remapped_image[25] = shape[18]
   remapped_image[26] = shape[17]
   # neatening 
   remapped_image[27] = shape[0]

   return remapped_image



if __name__ == '__main__' :
    image = cv2.imread('images/alexsashaausgang2.JPG')
    cv2.imshow('AUSGANGSBILD', image)
    target = cv2.imread('images/alexsashatarget2.JPG')
    #cv2.imshow('AUSGANGSBILD 2', target)
    #copy = image
    #face = face_cascade.detectMultiScale(image, 1.3, 5)
    #get_faces(copy,image,target)
   #get_profiles (copy, image, target)
    #cv2.imshow('ERGEBNIS', target)
    #cv2.waitKey(0)
   # cv2.destroyAllWindows()
    get_facial_convex(image,target)

import cv2
import dlib
import numpy
import sys
import pdb

PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

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

if __name__ == '__main__' :
    image = cv2.imread('images/alexsashaausgang1.JPG')
    cv2.imshow('AUSGANGSBILD', image)
    target = cv2.imread('images/alexsashatarget1.JPG')
    cv2.imshow('AUSGANGSBILD 2', target)
    copy = image
    face = face_cascade.detectMultiScale(image, 1.3, 5)
    result = get_faces(copy,image,target)
    cv2.imshow('ERGEBNIS', target)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

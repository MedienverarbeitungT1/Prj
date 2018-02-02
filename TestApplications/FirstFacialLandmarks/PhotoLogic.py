import cv2
import dlib
import sys
import pdb
import numpy as np
from matplotlib import pyplot as plt
import imutils
from imutils import face_utils
from PIL import Image
from cStringIO import StringIO


class PhotoLogic:
    PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
    profile_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_profileface_default.xml')

    def __init__(self):
        self.PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
        self.face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
        self.profile_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_profileface_default.xml')

    def sobel (im):
        im = cv2.Sobel(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY),cv2.CV_64F,0,1,ksize=5)
        return im;

    def laplace(im):
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.GaussianBlur(gray,(3,3),0)
        laplacian = cv2.Laplacian(im,cv2.CV_64F)
        return laplacian

    def get_rectangles (self, im):
        copy = im
        face = self.face_cascade.detectMultiScale(copy, 1.3, 5)
        numberOfFaces = 1
        for(x,y,w,h) in face:
            x = int(round(x*0.9))
            y = int(round(y*0.7))
            w = int(round(w*1.5))
            h = int(round(h*1.7))
            
            cv2.rectangle(im, (x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(im,str(numberOfFaces), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            
            #crop_img = copy[y:y+h,x:x+w]
            #target[y:y+crop_img.shape[0], x:x+crop_img.shape[1]] = crop_img
            roi = im [y:y+h, x:x+w]
            eye = self.eye_cascade.detectMultiScale(roi,minNeighbors = 3)
            numberOfFaces = numberOfFaces+1
        return im
    
    def switchRects(self, im, number,target):
        copy = im  
        face = self.face_cascade.detectMultiScale(copy, 1.3, 5)
        count = 1
        for(x,y,w,h) in face:
                x = int(round(x*0.9))
                y = int(round(y*0.7))
                w = int(round(w*1.5))
                h = int(round(h*1.7))
               
                if count==number:
                    
                    crop_img = copy[y:y+h,x:x+w]
                    
                    target[y:y+crop_img.shape[0], x:x+crop_img.shape[1]] = crop_img
                    roi = im [y:y+h, x:x+w]
                    eye = self.eye_cascade.detectMultiScale(roi,minNeighbors = 3)
                    return target

                count = count + 1
        return target


    def switchMasks(self, im,imageObj, number, target):
        
        image = im

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        out_face = np.zeros_like(image)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.PREDICTOR_PATH)
        rects = detector(gray, 1)
        print("Number of faces detected: {}".format(len(rects)))
        for (i, rect) in enumerate(rects):
            if (i==number-1):   
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
                remapped_shape = self.face_remap(shape)
                cv2.fillConvexPoly(feature_mask, remapped_shape[0:27], 1)
                feature_mask = feature_mask.astype(np.bool)
                out_face[feature_mask] = image[feature_mask]
  
        tmp = cv2.cvtColor(out_face, cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
        b, g, r = cv2.split(out_face)
        rgba = [b,g,r, alpha]
        dst = cv2.merge(rgba,4)    
        dst = cv2.cvtColor(dst, cv2.COLOR_RGBA2BGRA)        
        pilImage = Image.fromarray(dst)
        
        x,y = pilImage.size
        pilImage.convert("RGBA")



        #target = cv2.cvtColor(target,cv2.COLOR_BGR2RGB)
        #pilTarget = Image.fromarray(target)
        #pilTarget.convert("RGBA")
        target = cv2.cvtColor(target,cv2.COLOR_BGR2RGB)
        pilTarget = Image.fromarray(target)
        pilTarget.paste(pilImage,(0,0),pilImage)
        return pilTarget;










    def get_faces (self,copy, im, target):
        face = self.face_cascade.detectMultiScale(copy, 1.3, 5)
        numberOfFaces = 1
        for(x,y,w,h) in face:
            x = int(round(x*0.9))
            y = int(round(y*0.7))
            w = int(round(w*1.5))
            h = int(round(h*1.7))
            crop_img = copy[y:y+h,x:x+w]
            target[y:y+crop_img.shape[0], x:x+crop_img.shape[1]] = crop_img
            roi = im [y:y+h, x:x+w]
            eye = self.eye_cascade.detectMultiScale(roi,minNeighbors = 3)
            numberOfFaces = numberOfFaces+1
        return target

    def get_facial_convex(self,im,imageObj):
        image = im
    
        #result = Image.open('images/alexsashaausgang2.JPG')
        result = Image.open('images/IMG_3597.JPG')
        #result = Image.open('images/alexsashaausgang2.JPG')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        out_face = np.zeros_like(image)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.PREDICTOR_PATH)
        rects = detector(gray, 1)
        print("Number of faces detected: {}".format(len(rects)))
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
            remapped_shape = self.face_remap(shape)
            cv2.fillConvexPoly(feature_mask, remapped_shape[0:27], 1)
            feature_mask = feature_mask.astype(np.bool)
            out_face[feature_mask] = image[feature_mask]
  
        
        tmp = cv2.cvtColor(out_face, cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
        b, g, r = cv2.split(out_face)
        rgba = [b,g,r, alpha]
        dst = cv2.merge(rgba,4)    
        dst = cv2.cvtColor(dst, cv2.COLOR_RGBA2BGRA)        
        pilImage = Image.fromarray(dst)
        
        x,y = pilImage.size;
        pilImage.convert("RGBA")
        imageObj.paste(pilImage,(0,0),pilImage)
        
        
                
        imageObj.show()
        cv2.waitKey(0)
    # imageObj.show()
        return image;


    def face_remap(self, shape):
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

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
    face = None   

    def __init__(self):
        self.PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
        self.face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
        self.profile_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_profileface_default.xml')

    '''
    name: make_faces
    arguments:  -self: the PhotoLogic instance
                -im: cv2 image, used as the source image
    returns:    - 
    Description: 
    This causes the face detection to only be executed once.
    '''
    def make_faces(self, im):
        copy = im
        self.face = self.face_cascade.detectMultiScale(copy, 1.3, 5)

    '''
    name: get_rectangles
    arguments:  -self: the PhotoLogic instance
                -im: cv2 image, used as the source image
    returns:    -im    
    Description: 
    This will detect faces in the image and create numbered rectangles around them while counting the faces.
    '''
    def get_rectangles (self, im):
        # count detected faces
        numberOfFaces = 1
        for(x,y,w,h) in self.face:
            
            # adjust the size of the rectangles, so they enclose the entire head, not only the face
            x = x - 50
            y = y - 50
            w = int(round(w*2.2))
            h = int(round(h*2.2))
            
            # draw the rectangles, set their colour to blue
            cv2.rectangle(im, (x,y), (x+w,y+h), (255,0,0),2)
            cv2.putText(im,str(numberOfFaces), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, thickness = 2)
            
            roi = im [y:y+h, x:x+w]
            eye = self.eye_cascade.detectMultiScale(roi,minNeighbors = 3)

            # increment face counter
            numberOfFaces = numberOfFaces+1
        return im


    '''
    name: switchRects
    arguments:  -self: the PhotoLogic instance
                -im: cv2 image, used as source image that will be cropped
                -number: the number entered by the user
                -target: cv2 image, the target image the cropped part is pasted onto
    returns:    -target     
    Description: 
    This will crop the content within the rectangle and paste it onto the target image.
    The rectangle used for the cropping is the one that corresponds with the number the user entered.
    '''
    def switchRects(self, im, number,target):
        copy = im  
        face = self.face_cascade.detectMultiScale(copy, 1.3, 5)
        # count is used to check if the number the user entered equals the number of a detected face
        count = 1
        for(x,y,w,h) in face:

                if count==number:
                    
                    # adjust the size of the rectangles, so they enclose the entire head, not only the face
                    x = x - 50
                    y = y - 50
                    w = int(round(w*2.2))
                    h = int(round(h*2.2))
                  
                    # crop the part of the image within the rectangle
                    crop_img = copy[y:y+h,x:x+w]
                    
                    # paste the cropped part onto the target image
                    target[y:y+crop_img.shape[0], x:x+crop_img.shape[1]] = crop_img
                  
                    return target

                # increment count
                count = count + 1
        return target

    '''
    name: switchMasks
    arguments:  -self: the PhotoLogic instance
                -im: cv2 image, used as source image
                -imageObj: PIL version of the cv2 image im
                -number: the number entered by the user
                -target: the target image the mask is pasted onto
    returns:    -pilTarget     
    Description: 
    This will create a mask of a face in the source image, then crop the content within the mask and paste it onto the target image.
    The cropped face is the one that corresponds with the number the user entered.
    '''
    def switchMasks(self, im, imageObj, number, target):

        copy = im
        face = self.face_cascade.detectMultiScale(copy, 1.3, 5)
        rects = dlib.rectangles()
        for(x,y,w,h) in face:

            rects.append(dlib.rectangle(int(x), int(y), int(x + w), int(y + h))  )
        
        image = im

        # convert colour from BGR to greyscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        out_face = np.zeros_like(image)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.PREDICTOR_PATH)

        print("Log: ---Number of faces detected: {}".format(len(rects)))
        help = 1
        for (i , rect) in enumerate(rects):
            
            if (help == number):   
                
                shape = predictor(gray, rect)
                # array will include the coordinates of the facial landmarks for each face
                array = []
                for x in range(0,shape.num_parts):
                    point = []
                    # add facial landmark coordinates to point
                    point.append(shape.part(x).x)
                    point.append(shape.part(x).y)
                    # add point to array
                    array.append(point)
                shape = face_utils.shape_to_np(shape)
                remapped_shape = np.zeros_like(shape)
                # define blank mask as empty numpy array
                feature_mask = np.zeros((image.shape[0], image.shape[1]))
                # adjust remapped shape     
                remapped_shape = self.face_remap(shape)
                # fill the mask
                cv2.fillConvexPoly(feature_mask, remapped_shape[0:27], 1)
                # use boolean values for the mask
                feature_mask = feature_mask.astype(np.bool)
                out_face[feature_mask] = image[feature_mask]
            help = help + 1

        # convert colour from BGR to greyscale
        tmp = cv2.cvtColor(out_face, cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
        b, g, r = cv2.split(out_face)
        rgba = [b,g,r, alpha]
        dst = cv2.merge(rgba,4)

        # convert colour from RGBA to BGRA    
        dst = cv2.cvtColor(dst, cv2.COLOR_RGBA2BGRA)
        # create a pilImage from dst        
        pilImage = Image.fromarray(dst)
        
        x,y = pilImage.size
        # convert pilImage to RGBA
        pilImage.convert("RGBA")

        # convert colour from BGR to RGB
        target = cv2.cvtColor(target,cv2.COLOR_BGR2RGB)
        pilTarget = Image.fromarray(target)
        # paste cropped mask onto the target image
        pilTarget.paste(pilImage,(0,0),pilImage)
        return pilTarget

    '''
    name: face_remap
    arguments:  -self: the PhotoLogic instance
                -shape: 
    returns:    -remapped_image    
    Description: 
    This adjusts the shape drawn by the facial landmarks.
    '''
    def face_remap(self, shape):
        remapped_image = shape.copy()
   # left eyebrow
        remapped_image[17] = shape[26]
        remapped_image[18] = shape[25]
        remapped_image[19] = shape[24]
        remapped_image[20] = shape[23]
        remapped_image[21] = shape[22]
   # right eyebrow
        remapped_image[22] = shape[21]
        remapped_image[23] = shape[20]
        remapped_image[24] = shape[19]
        remapped_image[25] = shape[18]
        remapped_image[26] = shape[17]
   # neatening 
        remapped_image[27] = shape[0]

        return remapped_image

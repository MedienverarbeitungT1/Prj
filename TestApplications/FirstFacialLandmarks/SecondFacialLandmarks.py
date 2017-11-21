import cv2
import dlib
import numpy
import sys

PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

class NoFaces(Exception):
    pass

def get_faces (copy, im):
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(copy, 1.3, 5)

    for(x,y,w,h) in face:
        x = x - 50
        y = y - 75
        w = w + 100
        h = h + 150
        cv2.rectangle(im, (x,y),(x+w,y+h),(255,0,0),2)
        #roi_gray = gray[y:y+h, x:x+w]
        roi = im [y:y+h, x:x+w]
        eye = eye_cascade.detectMultiScale(roi,minNeighbors = 3)
        for(ex,ey,ew,eh)in eye:
            cv2.rectangle(roi, (ex, ey),(ex+ew, ey+eh),(0,255,0),2)
    return im


def get_landmarks(im):
    rects = detector(im, 1)
    
    if len(rects) == 0:
        raise NoFaces

    return numpy.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])

def annotate_landmarks(im, landmarks):
    im = im.copy()
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])
        cv2.putText(im, str(idx), pos,
                    fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 255))
        cv2.circle(im, pos, 3, color=(0, 255, 255))
    return im



image = cv2.imread('images/test3.jpg')
copy = image
face = face_cascade.detectMultiScale(image, 1.3, 5)

for(x,y,w,h) in face:
    landmarks = get_landmarks(image)
    image = annotate_landmarks(image, landmarks)


#landmarks = get_landmarks(image)
#image_with_landmarks = annotate_landmarks(image, landmarks)
#image_with_fd_landmarks = get_faces(image_with_landmarks)
image_with_fd_landmarks = get_faces(copy,image)

cv2.imshow('Landmarks und Gesichtserkennung', image_with_fd_landmarks)
cv2.waitKey(0)
cv2.destroyAllWindows()

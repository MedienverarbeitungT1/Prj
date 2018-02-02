import cv2
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from PhotoLogic import *
from PIL import ImageTk, Image
import tkFont
from Tkinter import Entry
   
def generateWindow():
    root = Tk()
    root.title("Group Photo Editor 1.0")
   # root.geometry("500x150")
    root.configure(background='grey')
    return root

class GroupPhotoEditor:
   

    initialImg = ""
    targetImg = ""
    noFirstPreviewFrame = True
    noSecondPreviewFrame = True
    noResultFrame = True
    
    resultFrame = NONE
    firstPreviewFrame = NONE
    firstPreviewLabel = NONE
    secondPreviewFrame = NONE
    secondPreviewLabel = NONE
    entryFrame = NONE
    checkBoxFrame = NONE
    firstEntry = False
    okButton = NONE
    firstImage = NONE
    secondImage = NONE
    number = 0 

    varForCheckbutton1 = NONE
    varForCheckbutton2 = NONE


    def __init__(self,master):
        
        varForCheckbutton1 = IntVar()
        varForCheckbutton2 = IntVar()
        firstImg= StringVar()
        secondImg= StringVar()
        firstImg.set("Select first Image")
        secondImg.set("Select second Image")
        #Initialize the topFrame and pack it into our root
        topFrame = Frame(master).pack()
        label = Label(topFrame, text= "Group Photo Editor").pack(fill=X)
        bottomFrame = Frame(master).pack(side = BOTTOM)
        button1 = Button(bottomFrame,textvariable = firstImg, command= lambda:self.onButton1(master,firstImg)).pack(fill=BOTH)
        button2 = Button(bottomFrame,textvariable = secondImg, command = lambda: self.onButton2(master,secondImg)).pack(fill=BOTH)
        button3 = Button(bottomFrame,text = "Generate Image (masks)", command = self.onButton3).pack(fill=BOTH)
        button4 = Button(bottomFrame,text = "Generate Rectangles for Pic 1", command = lambda: self.onButton4(master,True)).pack(fill=BOTH)
        button41 = Button(bottomFrame,text = "Generate Rectangles for Pic 2", command = lambda: self.onButton4(master,False)).pack(fill=BOTH)
        button5 = Button(bottomFrame,text = "Generate Image (faces)", command = self.onButton5).pack(fill=BOTH)
        button6 = Button(bottomFrame,text = "Generate Example", command = lambda: self.onButton6(master,firstImg,secondImg)).pack(fill=BOTH)
        button7 = Button(bottomFrame,text = "Quit", fg="red", command = master.destroy).pack(fill=BOTH)


    def onButton1(self,master,firstImg):
        
        
        filename = askopenfilename(filetypes = (("File Interchange Format", "*.jpg;jpeg")
                                                         ,("PNG files", "*.png")
                                                         ,("All files", "*.*") ))
        if filename: 
            try: 
               firstImg.set(filename)
               self.initialImg = filename
            except: 
                tkMessagebox.showerror("Open Source File", "Failed to read file \n'%s'"%filename)
                return
     
        if self.noFirstPreviewFrame:
            self.firstPreviewFrame = Frame(master).pack(side = BOTTOM)
            self.noFirstPreviewFrame = False      
        else: 
            self.firstPreviewLabel.destroy()
        # create an image by using the filename-URL
        tmp = Image.open(filename)
        self.firstImage = tmp
        tmp = tmp.resize((450, 300), Image.ANTIALIAS)
        theImage = ImageTk.PhotoImage(tmp)
        # destroy the old label: delete all references to the old image
        self.firstPreviewLabel = Label(self.firstPreviewFrame, image = theImage,text ="Image 1", compound=CENTER,font=("Helvetica", 30))
        # make sure the references are correct:
        self.firstPreviewLabel.image = theImage
        # pack the label without image in the frame for preview:
        self.firstPreviewLabel.pack(side = LEFT, fill = BOTH, expand = YES)


    def onButton2(self,master,secondImg):
         
        filename = askopenfilename(filetypes = (("File Interchange Format", "*.jpg;jpeg")
                                                         ,("PNG files", "*.png")
                                                         ,("All files", "*.*") ))
        if filename: 
            try: 
               secondImg.set(filename)
               self.targetImg = filename
            except: 
                tkMessagebox.showerror("Open Source File", "Failed to read file \n'%s'"%filename)
                return
     
        if self.noSecondPreviewFrame:
            self.secondPreviewFrame = Frame(master).pack(side = BOTTOM)
            self.noSecondPreviewFrame = False      
        else: 
            self.secondPreviewLabel.destroy()
        # create an image by using the filename-URL
        tmp = Image.open(filename)
        self.secondImage = tmp
        tmp = tmp.resize((450, 300), Image.ANTIALIAS)
        theImage = ImageTk.PhotoImage(tmp)
        # destroy the old label: delete all references to the old image
        self.secondPreviewLabel = Label(self.secondPreviewFrame, image = theImage,text ="Image 2", compound=CENTER,font=("Helvetica", 30))
        # make sure the references are correct:
        self.secondPreviewLabel.image = theImage
        # pack the label with out image in the frame for preview:
        self.secondPreviewLabel.pack(side = RIGHT, fill = BOTH, expand = YES)

    def onButton3(self):
        imageObj = Image.open(self.initialImg)
        image = cv2.imread(self.targetImg)
        #cv2.imshow('AUSGANGSBILD 1', image)
        #cv2.imshow('AUSGANGSBILD 2', cv2.imread(self.initialImg))
        photoLogic = PhotoLogic()
        photoLogic.get_facial_convex(image,imageObj)

    def onButton4(self,master,first):
        if (first == True):
            image = cv2.imread(self.initialImg)
        else:
            image = cv2.imread(self.targetImg)

        #cv2.imshow('AUSGANGSBILD 1', image)
        #cv2.imshow('AUSGANGSBILD 2', target)
        photoLogic = PhotoLogic()
        result = photoLogic.get_rectangles(image)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)        
        toShow = ImageTk.PhotoImage(Image.fromarray(result).resize((675, 450), Image.ANTIALIAS))
        if (self.firstEntry == False):
             # Generate a frame which contains the entry for user-input and a button in order to switch the faces from left to right
             self.entryFrame = Frame(master).pack(side = BOTTOM)
             entry = Entry(self.entryFrame)
             entry.pack(side = BOTTOM)
             # Set a default-value so python knows that entry contains a string
             entry.setvar("0")
             self.okButton = Button(self.entryFrame,text = "Verschiebe Nr. -->",command = lambda: self.onOk(int(str(entry.get())))).pack(side = BOTTOM)    
             self.firstEntry = True
            
            


        if (first== True):
            self.firstPreviewLabel.destroy()
            self.firstPreviewLabel = Label(self.firstPreviewFrame, image = toShow,text ="Image 1", compound=CENTER,font=("Helvetica", 30))
            # make sure the references are correct:
            self.firstPreviewLabel.image = toShow
            # pack the label without image in the frame for preview:
            self.firstPreviewLabel.pack(side = LEFT, fill = BOTH, expand = YES)
             #Generate checkboxes in ordner to let the user choose whether he/she wants to switch the triangle or the mask of the face
           # self.checkBoxFrame = Frame(master).pack(side = BOTTOM)
           # triangleCheckButton = Checkbutton(self.checkBoxFrame,text ="Triangle",variable  = self.varForCheckbutton1)
           # maskCheckButton = Checkbutton(self.checkBoxFrame,text = "Masks", variable = self.varForCheckbutton2)
           # triangleCheckButton.pack(side = LEFT)
           # maskCheckButton.pack(side = RIGHT)   
        else:
            self.secondPreviewLabel.destroy()
            # destroy the old label: delete all references to the old image
            self.secondPreviewLabel = Label(self.secondPreviewFrame, image = toShow,text ="Image 2", compound=CENTER,font=("Helvetica", 30))
            # make sure the references are correct:
            self.secondPreviewLabel.image = toShow
            # pack the label with out image in the frame for preview:
            self.secondPreviewLabel.pack(side = RIGHT, fill = BOTH, expand = YES)
    
       
    def onOk(self,number):
        self.secondPreviewLabel.destroy()
        photoLogic = PhotoLogic()
        image = cv2.imread(self.initialImg)
        target = cv2.imread(self.targetImg)
        newImage = photoLogic.switch(image, number, target)
        cv2.imwrite("newImage.jpg", newImage)
        newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2RGB)     
        toShow = ImageTk.PhotoImage(Image.fromarray(newImage).resize((675,450), Image.ANTIALIAS))
        self.secondPreviewLabel = Label(self.secondPreviewFrame, image = toShow, compound=CENTER,font=("Helvetica", 30))
        self.secondPreviewLabel.image = toShow
        self.secondPreviewLabel.pack(side = RIGHT, fill = BOTH, expand = YES)
        self.targetImg = "newImage.jpg"
        


    def onButton5(self):
        image = cv2.imread(self.initialImg)
        copy = image
        target = cv2.imread(self.targetImg)
        #cv2.imshow('AUSGANGSBILD 1', image)
        #cv2.imshow('AUSGANGSBILD 2', target)
        photoLogic = PhotoLogic()
        result = photoLogic.get_faces(image,copy,target)
        cv2.imshow('Ergebnis',result)

    def onButton6(self,master,firstImg,secondImg):

        imageObj = Image.open('images/IMG_3597.JPG') 
        image = cv2.imread('images/IMG_3598.JPG')
        self.initialImg = 'images/IMG_3597.JPG'
        self.targetImg = 'images/IMG_3598.JPG'
        firstImg.set('images/IMG_3597.JPG')
        secondImg.set('images/IMG_3598.JPG')

        if self.noFirstPreviewFrame:
            self.firstPreviewFrame = Frame(master).pack(side = BOTTOM)
            self.noFirstPreviewFrame = False      
        else: 
            self.firstPreviewLabel.destroy()
        # create an image by using the filename-URL
        tmp = Image.open('images/IMG_3597.JPG')
        tmp = tmp.resize((450, 300), Image.ANTIALIAS)
        theImage = ImageTk.PhotoImage(tmp)
        # destroy the old label: delete all references to the old image
        self.firstPreviewLabel = Label(self.firstPreviewFrame, image = theImage,text ="Image 1", compound=CENTER,font=("Helvetica", 30))
        # make sure the references are correct:
        self.firstPreviewLabel.image = theImage
        # pack the label with out image in the frame for preview:
        self.firstPreviewLabel.pack(side = LEFT, fill = BOTH, expand = YES)        
        
        if self.noSecondPreviewFrame:
            self.secondPreviewFrame = Frame(master).pack(side = BOTTOM)
            self.noSecondPreviewFrame = False      
        else: 
            self.secondPreviewLabel.destroy()
        # create an image by using the filename-URL
        tmp = Image.open('images/IMG_3598.JPG')
        tmp = tmp.resize((450, 300), Image.ANTIALIAS)
        theImage = ImageTk.PhotoImage(tmp)
        # destroy the old label: delete all references to the old image
        self.secondPreviewLabel = Label(self.secondPreviewFrame, image = theImage,text ="Image 2", compound=CENTER,font=("Helvetica", 30))
        # make sure the references are correct:
        self.secondPreviewLabel.image = theImage
        # pack the label with out image in the frame for preview:
        self.secondPreviewLabel.pack(side = RIGHT, fill = BOTH, expand = YES)

        #cv2.imshow('AUSGANGSBILD 1', image)
        #cv2.imshow('AUSGANGSBILD 2', cv2.imread('images/IMG_3597.JPG'))
        photoLogic = PhotoLogic()
        photoLogic.get_facial_convex(image,imageObj)
    
root = generateWindow()
gpe = GroupPhotoEditor(root)
root.mainloop()

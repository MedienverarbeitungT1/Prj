'''
Module-name: GuiModule
Description:
This module provides the class GroupPhotoEditor, the function generateWindow and is letting the root loop, so the application is visible.
The main-topic of this module is the presentation of the graphical user interface.
If necessary the a Logic-Module-instance will be called in order to solve the logic behind the programm.
'''

# Import statements:
import cv2
import numpy
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from PhotoLogic import *
from PIL import ImageTk, Image
import tkFont
from Tkinter import Entry
import os

'''
name: generateWindow
arguments: -
returns: root
Description:
This function returns a root (window) for the application, set the title and the background
'''
def generateWindow():
    root = Tk()
    root.title("Group Photo Editor")
    root.configure(background='grey')
    return root

class GroupPhotoEditor:
    # Some instance-variables which are going to be important in the functions:
    pl = PhotoLogic() #PhotoLogic-instance
    initialImg = "" # URL of the left image in the application.
    firstTarget = "" # URL of the initial target-URL (right image)
    targetImg = "" # URL of the right image during runtime
    lastImg = "" # URL of the last image, before last action
    noFirstPreviewFrame = True # Bool to determine if the first previewFrame is already set
    noSecondPreviewFrame = True # Bool to determine if the second previewFrame is already set
    noResultFrame = True #Bool to determine if the resultFrame is already set
    firstSwitch = True # Bool to determine if changes were made (runtime)
    resultFrame = NONE # Result-Frame
    firstPreviewFrame = NONE # First PreviewFrame (Left one)
    firstPreviewLabel = NONE # First PreviewLabel (Left image)
    secondPreviewFrame = NONE # Second PreviewFrame (Right one)
    secondPreviewLabel = NONE # Second PreviewLabel (Right image)
    entryFrame = NONE # Frame for the Entry (user-input)
    radioButtonFrame = NONE # Frame for the radio-bottons (masks or rectangles)
    firstEntry = False # Bool to determine if an entry is set for the first time or not
    okButton = NONE # The little Button on which the user confirms an action
    switches = 0 # Integer to see how many changes were made. See onOk() for further details...
    number = 0  # Number of the face which the user wants to change
    varForRadioBtn = NONE # Var for the Radio-Buttons (nothing fancy or special)

    '''
    name: __init__
    arguments:  self:   The GuiModule-instance
                master: The master-root
    returns: -
    Description:
    Initialize the first state of the application.
    '''
    def __init__(self,master):
        # Give the RadioButton-Var an Integer
        self.varForRadioBtn = IntVar()
        # Initialize the URLs
        firstImg= StringVar()
        secondImg= StringVar()
        firstImg.set("Select first Image")
        secondImg.set("Select second Image")
        #Initialize the topFrame and pack it into our root
        topFrame = Frame(master).pack()
        label = Label(topFrame, text= "Group Photo Editor").pack(fill=X)
        bottomFrame = Frame(master).pack(side = BOTTOM)
        
        '''
        Pack the Buttons into the ButtonFrame:
        firstImgButton: Choose the first image via tkFileDialog.
        secondImgButton: Choose the first image via tkFileDialog.
        saveButton: Save the image
        undoButton: Undo the last action.
        '''
        firstImgButton = Button(bottomFrame,textvariable = firstImg, command= lambda:self.onFirstImgButton(master,firstImg)).pack(fill=BOTH)
        secondImgButton = Button(bottomFrame,textvariable = secondImg, command = lambda: self.onSecondImgButton(master,secondImg)).pack(fill=BOTH)
        saveButton = Button(bottomFrame, text = "Save the image", command = self.file_save).pack(fill = BOTH)
        undoButton = Button(bottomFrame,text = "Undo last action", fg="red", command = self.onUndo).pack(fill=BOTH)
      

    '''
    name: onFirstImgButton
    arguments:  self:   The GuiModule-instance
                master: The master-root
                firstImg: A string which represents the path to the first image
    returns: -
    Description:
    This function provides a method in order to pack the image into the first Preview-Frame
    Also it calls the rect-function which generates the rectangles of our viola-jones-solution
    '''
    def onFirstImgButton(self,master,firstImg):
        
        filename = askopenfilename(filetypes = (("File Interchange Format", "*.jpg;*.jpeg")
                                                                    ,("PNG files", "*.png")
                                                                   ,("All files", "*.*") ))
        # Check if a filename is given (When filename == None: Either no file chosen or not compatible)    
        if filename: 
            try: 
               firstImg.set(filename)
               self.initialImg = filename
            except: 
                # When the file is corrupt or another Exception accours a messageBox informs the user about it and return the function
                tkMessagebox.showerror("Open Source File", "Failed to read file \n'%s'"%filename)
                return
        
        # If the User opens up the Frame for the first image for the first time: Put the Frame into the master and put the bool for it on false...
        if self.noFirstPreviewFrame:
            self.firstPreviewFrame = Frame(master).pack(side = BOTTOM)
            self.noFirstPreviewFrame = False      
        # ...if not: Destroy the old Label with the old image 
        else: 
            self.firstPreviewLabel.destroy()
       
         # Create an image by using the filename-URL
        tmp = Image.open(filename)
        tmp = tmp.resize((675, 450), Image.ANTIALIAS)
        # Convert the image into imageTk-format
        theImage = ImageTk.PhotoImage(tmp)
        # Destroy the old label: delete all references to the old image
        self.firstPreviewLabel = Label(self.firstPreviewFrame, image = theImage,text ="Image 1", compound=CENTER,font=("Helvetica", 30))
        # Make sure the references are correct:
        self.firstPreviewLabel.image = theImage
        # Pack the label without image in the frame for preview:
        self.firstPreviewLabel.pack(side = LEFT, fill = BOTH, expand = YES)
        # Call the rect-function to show the image with face-Detection (see rect()-documentation for further details)
        self.rect(master)
   
    '''
    name: onSecondImgButton
    arguments:  self:   The GuiModule-instance
                master: The master-root
                firstImg: A string which represents the path to the second image
    returns: -
    Description:
    This function provides a method in order to pack the image into the second Preview-Frame
    Also, this function pack the radiobuttons into a frame and make it visible after the second image is chosen
    '''   
    def onSecondImgButton(self,master,secondImg):
         
        filename = askopenfilename(filetypes = (("File Interchange Format", "*.jpg;*.jpeg")
                                                         ,("PNG files", "*.png")
                                                         ,("All files", "*.*") ))
        # Check if a filename is given (When filename == None: Either no file chosen or not compatible)
        if filename: 
            try: 
               secondImg.set(filename)
               self.targetImg = filename
               self.firstTarget = filename
            except: 
                # When the file is corrupt or another Exception accours a messageBox informs the user about it and return the function
                tkMessagebox.showerror("Open Source File", "Failed to read file \n'%s'"%filename)
                return
        # If the User opens up the Frame for the first image for the first time: Put the Frame into the master and put the bool for it on false...     
        if self.noSecondPreviewFrame:
            self.secondPreviewFrame = Frame(master).pack(side = BOTTOM)
            self.noSecondPreviewFrame = False      
        else: 
        # ...if not: Destroy the old Label with the old image 
            self.secondPreviewLabel.destroy()
            
        # Create an image by using the filename-URL
        tmp = Image.open(filename)
        tmp = tmp.resize((675, 450), Image.ANTIALIAS)
        theImage = ImageTk.PhotoImage(tmp)
        # Destroy the old label: delete all references to the old image
        self.secondPreviewLabel = Label(self.secondPreviewFrame, image = theImage,text ="Image 2", compound=CENTER,font=("Helvetica", 30))
        # Make sure the references are correct:
        self.secondPreviewLabel.image = theImage
        # Pack the label with out image in the frame for preview:
        self.secondPreviewLabel.pack(side = RIGHT, fill = BOTH, expand = YES)
        # If the user opens up the second image for the first time: Create a radioButtonFrame and pack the Buttons into the frame
        if self.radioButtonFrame == NONE:
            self.radioButtonFrame = Frame(master).pack(side = BOTTOM)
            # Buttons for the option "Rectangle" and "Mask": Paste rectangle of the detection from the first image onto the other image or the mask
            Radiobutton(self.radioButtonFrame, text="Rectangle", padx = 20, variable=self.varForRadioBtn, value=1).pack(side = LEFT)
            Radiobutton(self.radioButtonFrame, text="Mask", padx = 20, variable=self.varForRadioBtn, value=2).pack(side = LEFT)

    '''
    name: rect
    arguments:  self:   The GuiModule-instance
                master: The master-root
    returns: -
    Description:
    rect generates the rectangles around the first image to show the user which face he or she can pick in order to
    switch it to the other image
    '''  
    def rect(self,master):
        # First: read in the initinalImg and store it into an cv2-image-object.
        image = cv2.imread(self.initialImg)
        # Call the make_faces-function in the PhotoLogic() <=> PL(). See documentation in the logic for further details.
        self.pl.make_faces(image)
        # Call the get_rectangles-method of PL() in order to get an image with the rectangles
        result = self.pl.get_rectangles(image)
        # BGR2RGB convertion to prepare the image...
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)   
        # for the convertion into the ImageTk-format. Resize the image in order to show it in the preview-frame
        toShow = ImageTk.PhotoImage(Image.fromarray(result).resize((675, 450), Image.ANTIALIAS))
        if (self.firstEntry == False):
             # Generate a frame which contains the entry for user-input and a button in order to switch the faces from left to right.
             self.entryFrame = Frame(master).pack(side = BOTTOM)
             entry = Entry(self.entryFrame)
             entry.pack(side = BOTTOM)
             # Set a default-value so python knows that entry contains a string
             entry.setvar("0")
             # Create an ok-Button to initiate the onOk-method when a user wants to switch a face from one picure to another.
             self.okButton = Button(self.entryFrame,text = "Paste Nr. -->",command = lambda: self.onOk(int(str(entry.get())))).pack(side = BOTTOM)    
             self.firstEntry = True 
      
        # Destroy the old label.                  
        self.firstPreviewLabel.destroy()
        # Create a new one.
        self.firstPreviewLabel = Label(self.firstPreviewFrame, image = toShow,text ="Image 1", compound=CENTER,font=("Helvetica", 30))
        # Make sure the references are correct:
        self.firstPreviewLabel.image = toShow
        # Pack the label without image in the frame for preview:
        self.firstPreviewLabel.pack(side = LEFT, fill = BOTH, expand = YES)
 
    '''
    name: onUndo
    arguments:  self:   The GuiModule-instance
    returns: -
    Description:
    This function makes it possible for the user to undo the last action he/she made.
    Every image which the user creates in the preview-label during runtime is stored temporally 
    If the user clicks on "Undo last action" the last temp-image is going to be the new image making the user possible 
    to reduce the error-rate of the application.
    An important variable is self.switches: It shows how many times the user created a new image.
    '''                                 
    def onUndo(self):
        if (self.switches < 0):
            # This shouldn't happen but just in case it returns nothing.
            return
        else:
            # Destroy the old label with the image
            self.secondPreviewLabel.destroy()
            # Open up the last Image
            lastImage = Image.open(self.lastImg)
            # Make it an tk-object
            toShow = ImageTk.PhotoImage(lastImage.resize((675, 450), Image.ANTIALIAS))
            # same as alway, put the label into the frame, make sure the dependencies are right (pythons garbage collection...) an pack it in
            self.secondPreviewLabel = Label(self.secondPreviewFrame, image = toShow)
            self.secondPreviewLabel.image = toShow
            self.secondPreviewLabel.pack(side = RIGHT, fill = BOTH, expand = YES)
            # TThe last image-url is now the new target-url, decrement self.switches (further details to self.switch in onOk-documentation)
            self.targetImg = self.lastImg
            self.switches = self.switches - 1
            if (self.switches == 1):
                # If only one change were made, the old url is our initial first url
                self.lastImg = self.firstTarget
 
    '''
    name: onOk
    arguments:  self:   The GuiModule-instance
                number: Number of the face which the user wants to change
    returns: -
    Description:
    When a user clicks the botton "Paste -->" this function will be called to offer a result.
    It pastes the rectangle or the mask via PL().switchRects or PL().switchMasks from the left on the right image
    '''            
    def onOk(self,number):
        # The lastImg is no longer the last one but the actual target before the switch
        self.lastImg = self.targetImg
        # Destroy the old Label
        self.secondPreviewLabel.destroy()
        # Get the current Images
        image = cv2.imread(self.initialImg)
        target = cv2.imread(self.targetImg)
        # Increment switches
        self.switches = self.switches + 1
        # The URL of the new image contains "newImage" plus the number of switches
        # For example: A user has 3 switches made (runtime). The new URL is newImage3.jpg
        url = "newImage"+str(self.switches)+".jpg"
        # The IntVar() for the radiobuttons is one when "Rectangles" is selected.
        if self.varForRadioBtn.get() == 1:
            # Open up switchRects of PL() for the logic. It returns the new image (See: PhotoLogic-Documentation)
            newImage = self.pl.switchRects(image, number, target)
            # Save the image
            cv2.imwrite(url, newImage)
            # Convert the image into an tk-object
            newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2RGB)     
            toShow = ImageTk.PhotoImage(Image.fromarray(newImage).resize((675,450), Image.ANTIALIAS))
            # Create a label and pack it in
            self.secondPreviewLabel = Label(self.secondPreviewFrame, image = toShow, compound=CENTER,font=("Helvetica", 30))
            self.secondPreviewLabel.image = toShow
            self.secondPreviewLabel.pack(side = RIGHT, fill = BOTH, expand = YES)
            self.targetImg = url            
    # IntVar is not 1 when "Masks" is selected:
        else:
            # Some Convertion in order to call the PL()-switchMasks-method
            imageObj = Image.open(self.initialImg)
            image = cv2.imread(self.initialImg)
            newImage = self.pl.switchMasks(image,imageObj,number,target)
            newImage1 = newImage.convert('RGB') 
            open_cv_image = numpy.array(newImage1) 
            # Convert RGB to BGR (Or you'll get blue faces...)
            open_cv_image = open_cv_image[:, :, ::-1].copy() 
            # Save the image
            cv2.imwrite(url, open_cv_image)
            # Create a label and pack it in
            toShow = ImageTk.PhotoImage(newImage.resize((675,450), Image.ANTIALIAS))
            self.secondPreviewLabel = Label(self.secondPreviewFrame, image = toShow, compound=CENTER,font=("Helvetica", 30))
            self.secondPreviewLabel.image = toShow
            self.secondPreviewLabel.pack(side = RIGHT, fill = BOTH, expand = YES)
            self.targetImg = url

    '''
    name: file_save
    arguments:  self:   The GuiModule-instance
    returns: -
    Description:
    When a user clicks on save image the image will be saved
    '''        
    def file_save(self):
        img = cv2.imread(self.targetImg,1)
        cv2.imshow("Result",img)
        cv2.imwrite('C:/Users/alex/Desktop/Results/Image.jpg', img)
        cv2.waitKey(0)






# Generate the window and let it loop
root = generateWindow()
gpe = GroupPhotoEditor(root)
root.mainloop()

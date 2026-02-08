import cv2

cnt=0
# Method to draw boundary around the detected feature
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords


# Method to detect the features
def detect(img, faceCascade, eyeCascade, mouthCascade):
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
    coords = draw_boundary(img, faceCascade, 1.1, 12, color['blue'], "Persona")
    # If feature is detected, the draw_boundary method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0
    if len(coords)==4:
        #cv2.putText(img, "Persona: ", (20,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        # Updating region of interest by cropping image
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        # Passing roi, classifier, scaling factor, Minimum neighbours, color, label text
        coords = draw_boundary(roi_img, eyeCascade, 1.1, 16, color['red'], "")
        
        coords = draw_boundary(roi_img, mouthCascade, 1.1, 18, color['white'], "")
    return img


# Loading classifiers

dropped = 0 # drop frames count

vid = cv2.VideoCapture('http://10.87.12.92/live') # open webcam capture



faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyesCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouthCascade = cv2.CascadeClassifier('Mouth.xml')



while True:
    ret, frame = vid.read() # get frame-by-frame
    print(vid.isOpened(), ret)
    if frame is not None:
        img = detect(frame, faceCascade, eyesCascade, mouthCascade)
        if dropped > 0: dropped = 0 # reset
        cv2.imshow('VIGILANCIA',img) # display frame
        if cv2.waitKey(22) & 0xFF == ord('q'): # press q to quit
            break
    else:
        dropped += 1
        if dropped > 100:
           print("SERVIDOR CAIDO")
           break


# Done, clear all resources
vid.release()
cv2.destroyAllWindows()

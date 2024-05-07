import cv2
import numpy as np

def createPremask(filename):
    img = cv2.imread(filename)

    # увеличение резкости
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.Canny(img, 150, 150)
    img = cv2.GaussianBlur(img, (9, 9), 0)

    kernel = np.ones((5, 5), np.uint8)
    img = cv2.dilate(img, kernel, iterations=45) #45

    kernel = np.ones((5, 5), np.uint8)
    img = cv2.erode(img, kernel, iterations=60) #60

    # наложение черной рамки, чтобы перекрыть поля сканера
    w = img.shape[1]
    h = img.shape[0]
    size = 40
    cv2.rectangle(img, (0,0), (w,size), (0,0,0),thickness=cv2.FILLED)
    cv2.rectangle(img, (0,0), (size,h), (0,0,0),thickness=cv2.FILLED)
    cv2.rectangle(img, (0,h-size), (w,h), (0,0,0),thickness=cv2.FILLED)
    cv2.rectangle(img, (w-size,0), (w,h), (0,0,0),thickness=cv2.FILLED)

    #cv2.imwrite(premask_name, img)

    return img


def createDetectionMask(filename, contour_mask_name):
    
    img = createPremask(filename)
    w = img.shape[1]
    h = img.shape[0]
                  
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    # Drawing Rectangle Contours
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.intp(box) #int0
        img = cv2.drawContours(img, [box], 0, (255,255,255), thickness=-1) #BGR_Color_Sequence

    img = cv2.GaussianBlur(img, (7, 7), 0)
    
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    # Drawing Rectangle Contours
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.intp(box) #int0
        img = cv2.drawContours(img, [box], 0, (255,255,255), thickness=-1) #BGR_Color_Sequence
   
    size = 40
    cv2.rectangle(img, (0,0), (w,size), (0,0,0),thickness=cv2.FILLED)
    cv2.rectangle(img, (0,0), (size,h), (0,0,0),thickness=cv2.FILLED)
    cv2.rectangle(img, (0,h-size), (w,h), (0,0,0),thickness=cv2.FILLED)
    cv2.rectangle(img, (w-size,0), (w,h), (0,0,0),thickness=cv2.FILLED)

    cv2.imwrite(contour_mask_name, img) #saving the Final Image

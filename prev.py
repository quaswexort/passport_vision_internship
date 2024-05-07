#print(text)
# # img[0:100, 0:100]
# cv2.imshow('Image', img)
# # print(img.shape)
# cv2.waitKey(0)

# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
# while True:
#     success, img = cap.read()

#     img = cv2.GaussianBlur(img, (3, 3), 0)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img = cv2.Canny(img, 30, 30)
#     kernel = np.ones((3, 3), np.uint8)  
#     img = cv2.dilate(img, kernel, iterations=1)
#     img = cv2.erode(img, kernel, iterations=1)

#     cv2.imshow('Video', img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# photo = np.zeros((300, 300, 3), np.uint8)
# # photo[0:100, 0:100] = [255, 0, 0]   
# cv2.rectangle(photo, (0, 0), (100, 100), (119, 201, 105), cv2.FILLED)
# cv2.line(photo, (0, photo.shape[0]//2), (photo.shape[1], photo.shape[0]//2), (200, 201, 105), 3)
# cv2.circle(photo, (photo.shape[1]//2, photo.shape[0]//2), 50, (0, 0, 255), 2)
# cv2.putText(photo, 'Hello World', (100, 90), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 2)
# cv2.imshow('Photo', photo)
# cv2.waitKey(0)

# img = cv2.imread('ex2.jpg')
# img = cv2.resize(img, (img.shape[1]//7, img.shape[0]//7))
# #img = cv2.flip(img, -1)
# def rotate(img_param, angle):
#     (h, w) = img.shape[:2]
#     center = (w//2, h//2)
#     M = cv2.getRotationMatrix2D(center, angle, 1)
#     return cv2.warpAffine(img, M, (w, h))
# #img = rotate(img, 90)
# #смещение
# def translate(img_param, x, y):
#     M = np.float32([[1, 0, x], [0, 1, y]])
#     return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
# def transform(img_param, x, y):
#     mat = np.float32([[1, 0, x], [0, 1, y]])
#     return cv2.warpAffine(img_param, mat, (img.shape[1], img.shape[0]))
# img = transform(img, 30, 200)
# cv2.imshow('Image', img)
# cv2.waitKey(0)

# #contoors and shape detection
# img = cv2.imread('pages//ex11.jpg')
# img = cv2.resize(img, (img.shape[1]//7, img.shape[0]//7))
# new_img = np.zeros(img.shape, np.uint8)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.GaussianBlur(img, (3, 3), 0)
# img = cv2.Canny(img, 100, 100)
# img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
# con, hir = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(new_img, con, -1, (43, 201, 14), 1)
# #print(con)
# cv2.imshow('Image', new_img)
# cv2.waitKey(0)

# #img = np.zeros((350, 350, 3), np.uint8)
# photo = cv2.imread('pages//ex11.jpg')
# img = np.zeros((photo.shape[:2], 3), dtype='uint8')

# circle = cv2.circle(img.copy(), (0, 0), 50, (255, 255, 255), -1)
# square = cv2.rectangle(img.copy(), (25, 25), (250, 350), (255, 255, 255), -1) 


# img = cv2.bitwise_and(photo, photo, mask=square)

# cv2.imshow('Image', img)
# cv2.waitKey(0)
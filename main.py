import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import numpy as np
import cv2
import fd_util
def show_img(im_stack):
    cv2.imshow('image', im_stack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def print_img_size(im):
    result = im.shape
    print('len of im:' + str(len(result)))
    print result[1], result[0]

# open in grayscale
im = cv2.imread('image/7seg.jpg')
#print_img_size(im)

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#print_img_size(imgray)

imgblur = cv2.GaussianBlur(imgray, (5, 5), 0)
#print_img_size(imgblur)

# find contours
ret, thres = cv2.threshold(imgblur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#print_img_size(thres)

kernel = np.ones((5, 5), np.uint8)
dilation = cv2.dilate(thres, kernel, iterations = 2)
#print_img_size(dilation)

_, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im, contours, -1, (0, 255, 0), 1)

print('contours: ' + str(len(contours)))

stack_img = np.hstack((imgray, imgblur, thres, dilation))
#show_img(stack_img)
#show_img(im)

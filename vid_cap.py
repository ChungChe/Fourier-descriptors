import sys
import cv2
from time import gmtime, strftime
import golden

import sqlite3 as db
import db_util

try:
    con = db.connect('curve.db')
    print('Connect to curve.db')
    cur =con.cursor()
except db.Error, e:
    if con:
        con.rollback()
        sys.exit(1)

cam = cv2.VideoCapture(0)
def cam_setup(cam):
    '''
    I don't know how to turn off webcam's white balancing
    But in http://stackoverflow.com/questions/5652085/how-to-disable-automatic-white-balance-from-webcam
    Gavimoss's comment, so I reduce the framerate to 21(mine is 30)
    Thanks Gavimoss
    '''
    cam.set(cv2.CAP_PROP_FPS, 21)
    '''
    test = cam.get(cv2.CAP_PROP_POS_MSEC)
    ratio = cam.get(cv2.CAP_PROP_POS_AVI_RATIO)
    frame_rate = cam.get(cv2.CAP_PROP_FPS)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    brightness = cam.get(cv2.CAP_PROP_BRIGHTNESS)
    contrast = cam.get(cv2.CAP_PROP_CONTRAST)
    saturation = cam.get(cv2.CAP_PROP_SATURATION)
    hue = cam.get(cv2.CAP_PROP_HUE)
    gain = cam.get(cv2.CAP_PROP_GAIN)
    exposure = cam.get(cv2.CAP_PROP_EXPOSURE)
    print("Ratio: ", ratio)
    print("Frame Rate: ", frame_rate)
    print("Height: ", height)
    print("Width: ", width)
    print("Brightness: ", brightness)
    print("Contrast: ", contrast)
    print("Saturation: ", saturation)
    print("Hue: ", hue)
    print("Gain: ", gain)
    print("Exposure: ", exposure)
    '''
last_val = -1 
while True:
    cam_setup(cam)
    s, im = cam.read()
    cv2.imshow("Test", im)
    key = cv2.waitKey(1000)
    if key == 27:
        break
    if key == 1048603:
        break
    val = golden.identify_number(im)
    diff = abs(last_val - val)
    #print("val: {}, diff: {}".format(val, diff))
    if last_val != -1 and diff < 30:
        print(val)
        db_util.insert_data(con, cur, 1, float(val))
    # unreasonable results, dump for debug
    if diff > 8 or val > 80:
        current_time = strftime("%Y-%m-%d_%H-%M-%S")
        output_file_name = 'bug_{}_{}.jpg'.format(current_time, val)
        cv2.imwrite(output_file_name, im, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    last_val = val
if cur:
    cur.close()
if con:
    con.close()
    
cv2.destroyAllWindows()
cv2.VideoCapture(0).release()



import sys
import Image
sys.path.append('/usr/local/lib/python2.7/site-packages')
from flask import Flask, render_template, request, jsonify, send_file 
from collections import OrderedDict
import json
import sqlite3 as db
import numpy as np
import cv2
import fd_util

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
def show_1st_level(hierarchy):
	for i in range(0, len(hierarchy)):
		if len(hierarchy[i]) != 4:
			continue
		if hierarchy[i][0] == -1:
			continue
		print(i)

def show_img(im_stack):
    cv2.imshow('image', im_stack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def print_img_size(im):
    result = im.shape
    print('len of im:' + str(len(result)))
    print result[1], result[0]
def query(start, end, machine_list):
	return [1, 2, 3]

@app.context_processor
def utility_processor():
	def zfill(value, digit):
		return str(value).zfill(digit)
	return dict(zfill=zfill)

@app.route('/get_image')
def get_image():
	# open in grayscale
	im = cv2.imread('image/7seg.jpg')
	print_img_size(im)

	imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	imgray1 = cv2.cvtColor(imgray, cv2.COLOR_GRAY2BGR)
	#print_img_size(imgray)

	imgblur = cv2.GaussianBlur(imgray, (5, 5), 0)
	print_img_size(imgblur)
	imgblur1 = cv2.cvtColor(imgblur, cv2.COLOR_GRAY2BGR)
	# find contours
	ret, thres = cv2.threshold(imgblur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	#print_img_size(thres)

	kernel = np.ones((5, 5), np.uint8)
	dilation = cv2.dilate(thres, kernel, iterations = 2)
	dilation1 = cv2.cvtColor(dilation, cv2.COLOR_GRAY2BGR)
	#print_img_size(dilation)

	# CHAIN_APPROX_SIMPLE
	_, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(im, contours, -1, (0, 255, 0), 1)
	print('hierarchy: ' + str(len(hierarchy[0])))
	show_1st_level(hierarchy[0])
	# print ith contour's first point
	print((contours[0][0][0][0]))
	# print ith contour's second point
	print((contours[0][0][0][1]))


	stack_img = np.vstack((imgray1, imgblur1, dilation1, im))
	# opencv uses BGR but numpy uses RGB, stack_img uses RGB, so we need to convert to BGR again
	pil_bgr = cv2.cvtColor(stack_img, cv2.COLOR_RGB2BGR)
	pil_rgb = Image.fromarray(pil_bgr, 'RGB')
	pil_rgb.save('static/image/lala.jpg')
	return send_file('static/image/lala.jpg', mimetype='image/jpeg')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
	print("home")	
	outputList = []	
	user = {'nickname': 'CurveGoGo'}
	return render_template('index.html', 
			title = path, 
			user = user, output = outputList )

@app.route('/draw_chart', methods = ['POST'])
def draw_chart():
	print("post")	
	my_json = request.json
	start = my_json.get('datetime_start')
	end = my_json.get('datetime_end')
	machine_list = my_json.get('mlist')
	outputList = query(start, end, machine_list)
	my_dict = []
	print('total result: ' + str(len(outputList)))
	for element in outputList:
		my_dict.append(OrderedDict([("datetime", element[2]), ("M" + str(element[0]), format(float(element[1]), '.2f'))]))
	return jsonify(data=my_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0')








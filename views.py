import sys
from PIL import Image
sys.path.append('/usr/local/lib/python2.7/site-packages')
from flask import Flask, render_template, request, jsonify, send_file 
from collections import OrderedDict
import json
import sqlite3 as db
import numpy as np
import cv2
import fd_util as fu

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

'''
 Show 0 - 9 contour indexes
 hierarchy has 4 elements
 next contour, previous contour, first child contour, parent contour
 Real number    9  7  8    6  5  4  1  0  2  3
 ----------------------------------------------------------------------
 index		    0  2  3    6  8  9 10 11 13 14
				|    / \   |          |
 child          1   4   5  7          12 
'''
def show_1st_level(hierarchy):
	for i in range(0, len(hierarchy)):
		if len(hierarchy[i]) != 4:
			continue
		#if hierarchy[i][0] == -1:
		#	continue
		print(i, hierarchy[i][0], hierarchy[i][1], hierarchy[i][2], hierarchy[i][3])

def show_img(im_stack):
    cv2.imshow('image', im_stack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def print_img_size(im):
    result = im.shape
    print('len of im:' + str(len(result)))
    print result[1], result[0]

'''
 return 
	{ data: [{x: 123, y: 234}, {x: 245, y: 111}, ...] }
'''
def contour2json(contours, index):
	ret = {}
	list_of_coord = []
	x_list = []
	y_list = []
	for contour_i in contours[index]:
		coord = {}
		x = int(contour_i[0][0])
		y = int(contour_i[0][1])
		x_list.append(x)
		y_list.append(y)

		coord['x'] = x
		coord['y'] = y
		list_of_coord.append(coord)
	
	ret['data'] = list_of_coord

	fd_x, fd_y = fu.get_fd(x_list, y_list)
	#for i in range(0, len(fd_x)):
	#	print(i, fd_x[i], fd_y[i])
	rev_x, rev_y = fu.get_inv_fd(fd_x, fd_y, 21)
	#print('==============================================')	
	result_list = []
	for i in range(0, len(rev_x)):
		coord = {}
		coord['x'] = int(rev_x[i])
		coord['y'] = int(rev_y[i])
		#print(i, rev_x[i], rev_y[i])
		result_list.append(coord)
	ret['final'] = result_list
	return ret

''' 
	input param: index ith contour in 7seg.jpg
'''
def extact_contours(index):
	im = cv2.imread('image/7seg.jpg')
	imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	imgblur = cv2.GaussianBlur(imgray, (5, 5), 0)
	ret, thres = cv2.threshold(imgblur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	kernel = np.ones((5, 5), np.uint8)
	dilation = cv2.dilate(thres, kernel, iterations = 2)
	# open cv 3
    #_, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(im, contours, -1, (0, 255, 0), 1)
	print('hierarchy: ' + str(len(hierarchy[0])))
	show_1st_level(hierarchy[0])
	print('contours: {}'.format(str(len(contours))))
	print('contours[{}] : {}'.format(index, str(len(contours[index]))))
	print('contours[{}][0] : {}'.format(index, str(len(contours[index][0]))))
	print('contours[{}][0][0] : {}'.format(index, str(len(contours[index][0][0]))))

	ccc = 0
	for contour_i in contours:
			x, y, w, h = cv2.boundingRect(contour_i)
			print(ccc, x, y, w, h)
			ccc += 1
			
#print('contours[0][0]:' + str(len(contours[0][0])))
#	print('contours[0][0][0]:' + str(len(contours[0][0][0])))
	
	my_dict = contour2json(contours, index)
#my_dict = [("contours", contours), ("hierarchy", hierarchy)]
	# [ [[x y]] [[x y]] ...]
	# print ith contour's first point
	#print((contours[0][0][0][0]))
	# print ith contour's second point
	#print((contours[0][0][0][1]))
	return my_dict


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
	print("OpenCV version:" + cv2.__version__)	
	outputList = []	
	user = {'nickname': 'Press run to get ith 7-segment display fourier descriptors'}
	return render_template('index.html', 
			title = path, 
			user = user, output = outputList )

@app.route('/extract', methods = ['POST'])
def extract():
	print("post")	
	my_json = request.json
	idx = my_json.get('index')
	print('idx:' + str(idx))
#print('total result: ' + str(len(outputList)))
#	for element in outputList:
#		my_dict.append(OrderedDict([("datetime", element[2]), ("M" + str(element[0]), format(float(element[1]), '.2f'))]))
	my_dict = extact_contours(int(idx))
	
	print('-----------------------------------------')
#print(my_dict)
	# write my_dict to file
	with open('my_dict_debug.json', 'w') as f:
		json.dump(my_dict, f)
	print('=========================================')
	return jsonify(my_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from PIL import Image
from flask import Flask, render_template, request, jsonify, send_file 
import json
import sqlite3 as db
import numpy as np
import cv2
from engine import *

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

@app.context_processor
def utility_processor():
    def zfill(value, digit):
        return str(value).zfill(digit)
    return dict(zfill=zfill)

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
#    for element in outputList:
#        my_dict.append(OrderedDict([("datetime", element[2]), ("M" + str(element[0]), format(float(element[1]), '.2f'))]))
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

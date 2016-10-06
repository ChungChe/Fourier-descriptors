import sys
import math
import my_tree
import time
import numpy as np
import cv2
import fd_util as fu
from collections import deque

'''
 Show 0 - 9 contour indexes
 hierarchy has 4 elements
 next contour, previous contour, first child contour, parent contour
 Real number    9  7  8    6  5  4  1  0  2  3
 ----------------------------------------------------------------------
 index          0  2  3    6  8  9 10 11 13 14
                |    / \   |          |
 child          1   4   5  7          12 
'''
def traverse_top_level(hierarchy, idx, l):
    if hierarchy[idx][0] != -1:
        l.append(hierarchy[idx][0])
        traverse_top_level(hierarchy, hierarchy[idx][0], l)

def find_first_non_negative_idx(hierarchy):
    idx = 0
    for i in xrange(0, len(hierarchy)):
        if hierarchy[i][0] != -1:
            idx = i
            break
    return idx

def build_hierarchy_tree(hierarchy):
    t = my_tree.tree()
    for i in xrange(0, len(hierarchy)):
        # top nodes
        if hierarchy[i][3] == -1:
            t.add_node(str(i))
        elif hierarchy[i][3] != -1:
            #print("add node {} under {}".format(str(i), str(hierarchy[i][3])))
            t.add_node(str(i), str(hierarchy[i][3]))
    return t
'''
    t.bfs("Root")
    print("--------")
    print(t.get_node("3").get_children())
    print("--------")
    print(t.get_node("6").get_children())
    print("--------")
'''

def show_top_level(hierarchy):
    # find first non -1 index
    top_level_idx_list = []
    first_idx = find_first_non_negative_idx(hierarchy)
    top_level_idx_list.append(first_idx)
    traverse_top_level(hierarchy, first_idx, top_level_idx_list)
    #print(top_level_idx_list)

# Row order sorting
def compare(contourA, contourB):
    x1, y1, w1, h1 = cv2.boundingRect(contourA)
    x2, y2, w2, h2 = cv2.boundingRect(contourB)
    if x1 <= x2:
        if y1 + h1 > y2:
            return -1
        else:
            return 1
    else:
        if y2 + h2 > y1:
            return 1
        else:
            return -1

def take_normalized_partial_fd(fds, n):
    ret_X = []
    ret_Y = []
    h = int((n - 1) / 2)
    n = len(fds)
    for i in xrange(n - h, n):
        ret_X.append(fds[i][0])
        ret_Y.append(fds[i][1])

    # translation invariant
    ret_X.append(0)
    ret_Y.append(0)
    for i in xrange(1, h):
        ret_X.append(fds[i][0])
        ret_Y.append(fds[i][1])
    # scaling invariant
    ret = zip(ret_X, ret_Y)
    G_plus_one = math.sqrt(fds[h+1][0] * fds[h+1][0] + fds[h+1][1] + fds[h+1][1])
    G_minus_one = math.sqrt(fds[h-1][0] * fds[h-1][0] + fds[h-1][1] + fds[h-1][1])
    factor = 1.0 / (G_plus_one + G_minus_one)
    #max_value = max(map(lambda p: math.sqrt(p[0] * p[0] + p[1] * p[1]), ret))
    #s_X = map(lambda v: v/max_value, ret_X)
    #s_Y = map(lambda v: v/max_value, ret_Y)
    s_X = map(lambda v: v * factor, ret_X)
    s_Y = map(lambda v: v * factor, ret_Y)
    return zip(s_X, s_Y)
# G-
def rotate_negative_fd(x, y, angle):
	ret_x = x * math.cos(angle) + y * math.sin(angle)
	ret_y = y * math.cos(angle) - x * math.sin(angle) 
	return (ret_x, ret_y)

# G+
def rotate_positive_fd(x, y, angle):
	ret_x = x * math.cos(angle) - y * math.sin(angle)
	ret_y = x * math.sin(angle) + y * math.cos(angle)
	return (ret_x, ret_y)

def fp(fds, angle):
    s = 0
    half = (len(fds) - 1) / 2
    for i in xrange(1, half + 1):
        minus_x = fds[half - i][0]
        minus_y = fds[half - i][1]
        plus_x = fds[half + i][0]
        plus_y = fds[half + i][1]
        # minus part
        z1 = rotate_negative_fd(minus_x, minus_y, angle)
        # plus part
        z2 = rotate_positive_fd(plus_x, plus_y, angle)
        s += z1[0] * z2[1] - z1[1] * z2[0]
    return s
def get_start_point_phase(fds):
    cmax = -99999
    ret = 0
    k = 400
    for i in xrange(0, k):
        angle = math.pi * i / float(k)
        c = fp(fds, angle)
        if c > cmax:
            cmax = c
            ret = angle
    return ret
def shift_start_point_phase(fds, angle):
    fds_tmp = fds
    half = (len(fds_tmp) - 1) / 2
    for i in xrange(1, half + 1):
        minus_x = fds[half - i][0]
        minus_y = fds[half - i][1]
        plus_x = fds[half + i][0]
        plus_y = fds[half + i][1]
        z1 = rotate_negative_fd(minus_x, minus_y, angle)
        z2 = rotate_positive_fd(plus_x, plus_y, angle)
        fds_tmp[half - i] = z1
        fds_tmp[half + i] = z2
    return fds_tmp

def make_start_point_invariant(fds):
    angle = get_start_point_phase(fds)
    return shift_start_point_phase(fds, angle)
def draw_points(pt, title):
    max_x = -99999
    min_x = 99999
    max_y = -99999
    min_y = 99999
    
    for p in pt:
        if p[0] > max_x:
            max_x = p[0]
        if p[0] < min_x:
            min_x = p[0]
        if p[1] > max_y:
            max_y = p[1]
        if p[1] < min_y:
            min_y = p[1]
    factor = 1
    half_x = int((max_x - min_x) / 2 * factor)
    half_y = int((max_y - min_y) / 2 * factor)
    width = int((max_x - min_x) * factor)
    height = int((max_y - min_y) * factor)
    print("w, h = ({}, {})".format(width, height))
    print("hx, hy = ({}, {})".format(half_x, half_y))
    img = np.zeros((height, width, 3), np.uint8)
    # draw vertical line
    cv2.line(img, (half_x, 0), (half_x, height -1), (255, 0, 0), 1)
    # draw horizontal line
    cv2.line(img, (0, half_y), (width - 1, half_y), (255, 0, 0), 1)
    for idx, p in enumerate(pt):
        pos_x = int(p[0] * factor) + half_x
        pos_y = int(p[1] * factor) + half_y
        #print("[{}]: ({}, {})".format(idx, pos_x, pos_y))
        cv2.circle(img, (pos_x, pos_y), 3, (0, 0, 255), -1)
    show_img(img, title)
def get_golden(contours, index):
    list_of_coord = []
    x_list = []
    y_list = []
    for contour_i in contours[index]:
        coord = {}
        x = int(contour_i[0][0])
        y = int(contour_i[0][1])
        x_list.append(x)
        y_list.append(y)
    original_points = zip(x_list, y_list)

    start1 = time.clock()    
    fds = fu.get_fd(original_points)
    end1 = time.clock()
	
    fds_half_count = (len(fds) - 21) / 2
    print("@@@@@ {} @@@@@@@@".format(fds_half_count))	
    #partial_fds = take_normalized_partial_fd(fds, 21) 
    tmp_fds = take_normalized_partial_fd(fds, 21) 
    partial_fds = make_start_point_invariant(tmp_fds)
    
    for i in xrange(0, fds_half_count):
    #for i in xrange(0, 192):
        partial_fds.insert(0, (0, 0))
        partial_fds.append((0, 0))
    items = deque(partial_fds)
    print(items)
    items.rotate(-202)
    print("$$$$$$$$$$")
    final = list(items)
    print(final)
    #max_value = max(map(lambda x: math.sqrt(x[0] * x[0] + x[1] * x[1]), partial_fds))
    #print(max_value)
    
    print("get_fd takes:"+str(end1-start1))
    #for i in xrange(0, len(fd_x)):
    #    print(i, fd_x[i], fd_y[i])
    start2 = time.clock()    
    #rev_points = fu.get_inv_fd(fds, 21)
    rev_points = fu.get_inv_fd(fds, 21)
    print("##### rev points for idx: {} = {} ##### {}".format(index, len(rev_points), len(fds)))
    end2 = time.clock()
    print("get_inv_fd takes:"+str(end2-start2))
    draw_points(rev_points, 'idx: {}'.format(str(index)))
    #print('==============================================')   
    pos_x = 0.0
    pos_y = 0.0
    for i in xrange(1, 10):
        pos_x += (1.0 / i) * (partial_fds[10 + i][0] + partial_fds[10 - i][0])
        pos_y += (1.0 / i) * (partial_fds[10 + i][1] + partial_fds[10 - i][1])
    print("pos ({}, {})".format(pos_x, pos_y))
    final_angle = math.atan2(pos_y, pos_x) * (180.0 / math.pi)
    print("final_angle = {}".format(final_angle))
    for idx, p in enumerate(partial_fds):
        angle = math.atan2(p[1], p[0]) * (180.0 / math.pi)
        radius = math.sqrt(p[0] * p[0] + p[1] * p[1])
        print("{}: ({}, {}) angle = {} r = {}".format(idx, p[0], p[1], angle, radius))
    plus_one_angle = math.atan2(partial_fds[11][1], partial_fds[11][0]) * (180.0 / math.pi)
    minus_one_angle = math.atan2(partial_fds[9][1], partial_fds[9][0]) * (180.0 / math.pi)
    shape_angle = (plus_one_angle + minus_one_angle) / 2.0
    print("shape_angle = {}".format(shape_angle))
    middle_x = (partial_fds[11][0] + partial_fds[9][0]) / 2.0
    middle_y = (partial_fds[11][1] + partial_fds[9][1]) / 2.0
    print("({}, {})".format(middle_x, middle_y))
    #print('==============================================')   
    #draw_line_test(partial_fds, str(index))
def show_img(im_stack, title):
    cv2.imshow(title, im_stack)
def draw_line_test(pt, title):
    max_x = -99999
    min_x = 99999
    max_y = -99999
    min_y = 99999
    
    for p in pt:
        if p[0] > max_x:
            max_x = p[0]
        if p[0] < min_x:
            min_x = p[0]
        if p[1] > max_y:
            max_y = p[1]
        if p[1] < min_y:
            min_y = p[1]
    factor = 25
    half_x = int((max_x - min_x) / 2 * factor)
    half_y = int((max_y - min_y) / 2 * factor)
    width = int((max_x - min_x) * factor)
    height = int((max_y - min_y) * factor)
    print("w, h = ({}, {})".format(width, height))
    print("hx, hy = ({}, {})".format(half_x, half_y))
    img = np.zeros((height, width, 3), np.uint8)
    # draw vertical line
    cv2.line(img, (half_x, 0), (half_x, height -1), (255, 0, 0), 1)
    # draw horizontal line
    cv2.line(img, (0, half_y), (width - 1, half_y), (255, 0, 0), 1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    for idx, p in enumerate(pt):
        pos_x = int(p[0] * factor) + half_x
        pos_y = int(p[1] * factor) + half_y
        cv2.circle(img, (pos_x, pos_y), 3, (0, 0, 255), -1)
        cv2.putText(img, str(idx), (pos_x, pos_y), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    show_img(img, title)

def extact_contours():

    im = cv2.imread('image/7seg.jpg')
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imgray, (5, 5), 0)
    ret, thres = cv2.threshold(imgblur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(thres, kernel, iterations = 2)

    (cv_version, _, _) = cv2.__version__.split(".")
    if cv_version == 3:
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    else:
        _, contours, hierarchy= cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(im, contours, -1, (0, 255, 0), 1)
    show_img(im, 'source with contour')
    
    #print('hierarchy: ' + str(len(hierarchy[0])))
    show_top_level(hierarchy[0])
#print('contours: {}'.format(str(len(contours))))
#    print('contours[{}] : {}'.format(index, str(len(contours[index]))))
#    print('contours[{}][0] : {}'.format(index, str(len(contours[index][0]))))
#    print('contours[{}][0][0] : {}'.format(index, str(len(contours[index][0][0]))))
    t = build_hierarchy_tree(hierarchy[0])
    str_list = t.get_node("Root").get_children()
    #print(t.get_node("Root").get_children())

    # convert str list to int list
    int_list = map(int, str_list)
    print(int_list)
    
    '''
    for i in int_list:
        x, y, w, h = cv2.boundingRect(contours[i])
        print(i, x, y, w, h)
        contour_lst.append(contours[i])
    '''
    contour_lst = map(lambda x: contours[x], int_list)
    
    '''
    contour_lst.sort(compare)
    #print(compare(contour_lst[0], contour_lst[1]))
    #print(compare(contour_lst[1], contour_lst[0]))
    #sorted(contour_lst, cmp=compare)
    print('-----------------------')
    for i in contour_lst:
        x, y, w, h = cv2.boundingRect(i)
        print(x, y, w, h)
    '''
    # Sort all contours coordinate by row order
    print('-----------------------')
    row_sorted_order_list = sorted(range(len(contour_lst)), key=lambda k: contour_lst[k], cmp=compare)
    print(row_sorted_order_list)
    row_idx_list = map(lambda x: int_list[x], row_sorted_order_list)
    print(row_idx_list)
    #print('contours[0][0]:' + str(len(contours[0][0])))
    #print('contours[0][0][0]:' + str(len(contours[0][0][0])))
    get_golden(contours, 0)
    get_golden(contours, 6)
#    start = time.clock()
#    my_dict = get_golden(contours, index)
#    end = time.clock()
#    print("get_golden takes:"+str(end-start))
    #my_dict = [("contours", contours), ("hierarchy", hierarchy)]
    # [ [[x y]] [[x y]] ...]
    # print ith contour's first point
    #print((contours[0][0][0][0]))
    # print ith contour's second point
    #print((contours[0][0][0][1]))
#return my_dict
    cv2.waitKey()
extact_contours()

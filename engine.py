import sys
import math
import my_tree
import time
import numpy as np
import cv2
import fd_util as fu

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

def show_img(im_stack):
    cv2.imshow('image', im_stack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def print_img_size(im):
    result = im.shape
    print('len of im:' + str(len(result)))
    print result[1], result[0]

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
    max_value = max(map(lambda p: math.sqrt(p[0] * p[0] + p[1] * p[1]), ret))
    s_X = map(lambda v: v/max_value, ret_X)
    s_Y = map(lambda v: v/max_value, ret_Y)
    return zip(s_X, s_Y)
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
    original_points = zip(x_list, y_list)

    start1 = time.clock()    
    fds = fu.get_fd(original_points)
    end1 = time.clock()

    # invariants
    # translation invariant
    #fds[0][0] = 0
    #fds[0][1] = 0
    #fds = (0, 0) + fds[1:]
    # scaling invariant
    partial_fds = take_normalized_partial_fd(fds, 21) 
    #max_value = max(map(lambda x: math.sqrt(x[0] * x[0] + x[1] * x[1]), partial_fds))
    #print(max_value)
    

    fd_list = []
    for i in xrange(0, len(partial_fds)):
        coord = {}
        coord['i'] = i
        coord['x'] = partial_fds[i][0]
        coord['y'] = partial_fds[i][1]
        fd_list.append(coord)
    ret['fd'] = fd_list

    print("get_fd takes:"+str(end1-start1))
    #for i in xrange(0, len(fd_x)):
    #    print(i, fd_x[i], fd_y[i])
    start2 = time.clock()    
    rev_points = fu.get_inv_fd(fds, 21)
    end2 = time.clock()
    print("get_inv_fd takes:"+str(end2-start2))
    #print('==============================================')    
    result_list = []
    for i in xrange(0, len(rev_points)):
        coord = {}
        coord['x'] = int(rev_points[i][0])
        coord['y'] = int(rev_points[i][1])
        #print(i, rev_x[i], rev_y[i])
        result_list.append(coord)
    ret['final'] = result_list
    return ret

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
    (cv_version, _, _) = cv2.__version__.split(".")
    if cv_version == 3:
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    else:
        _, contours, hierarchy= cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(im, contours, -1, (0, 255, 0), 1)
    print('hierarchy: ' + str(len(hierarchy[0])))
    show_top_level(hierarchy[0])
    print('contours: {}'.format(str(len(contours))))
    print('contours[{}] : {}'.format(index, str(len(contours[index]))))
    print('contours[{}][0] : {}'.format(index, str(len(contours[index][0]))))
    print('contours[{}][0][0] : {}'.format(index, str(len(contours[index][0][0]))))
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
    start = time.clock()
    my_dict = contour2json(contours, index)
    end = time.clock()
    print("contour2json takes:"+str(end-start))
    #my_dict = [("contours", contours), ("hierarchy", hierarchy)]
    # [ [[x y]] [[x y]] ...]
    # print ith contour's first point
    #print((contours[0][0][0][0]))
    # print ith contour's second point
    #print((contours[0][0][0][1]))
    return my_dict



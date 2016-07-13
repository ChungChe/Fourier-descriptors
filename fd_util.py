import sys
import math

def get_angle(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return math.degrees(math.atan2(y_diff, x_diff))
# get fourier descriptors, this function takes a lot of time
def get_fd(P):
    N = len(P)
    ret_x = []
    ret_y = []
    for u in range(0, N):
        total_X = 0
        total_Y = 0
        for k in range(0, N):
            theta = 2 * 3.14159 * u * k / N;
            cos_value = math.cos(theta)
            sin_value = math.sin(theta)
            total_X += P[k][0] * cos_value + P[k][1] * sin_value
            total_Y += P[k][1] * cos_value - P[k][0] * sin_value
        total_X /= N
        total_Y /= N
        ret_x.append(total_X)
        ret_y.append(total_Y)    
        #ret.push((total_X, total_Y))
    return zip(ret_x, ret_y)
# get inverse fourier descriptors
# param: (X_u, Y_u) uth fd, count from the middle
# param:  M, number of fds to reconstruct the original contour
#          M must be odd
#def get_inv_fd(X, Y, M):
def get_inv_fd(P, M):
    if M % 2 == 0:
        print "Error: M must be odd"
        return
    N = len(P)
    ret_x = []
    ret_y = []
    for k in range(0, N):
        total_x = 0
        total_y = 0
        half = (M - 1) / 2
        
        #left = int(N / 2) - 1 - int( M / 2)
        #right = int(N / 2) + int( M / 2)
        #for u in range(left, right):
        for u in range(0, half + 1):
            theta = 2 * 3.14159 * u * k / N;
            cos_value = math.cos(theta)
            sin_value = math.sin(theta)
            
            total_x += P[u][0] * cos_value - P[u][1] * sin_value
            total_y += P[u][1] * cos_value + P[u][0] * sin_value
        for u in range(N - half, N):
            theta = 2 * 3.14159 * u * k / N;
            cos_value = math.cos(theta)
            sin_value = math.sin(theta)
            
            total_x += P[u][0] * cos_value - P[u][1] * sin_value
            total_y += P[u][1] * cos_value + P[u][0] * sin_value
        ret_x.append(total_x)
        ret_y.append(total_y)
        #ret.push((total_x, total_y))
    return zip(ret_x, ret_y)

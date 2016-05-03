import sys
import math
import cv2
# get fourier descriptors
def get_fd(x, y):
	if len(x) != len(y):
		print "Error: The length of input x and y should be equal"
		return
	N = len(x)
	for u in range(0, N):
		total_X = 0
		total_Y = 0
		for k in range(0, N):
			theta = 2 * 3.14159 * u * k / N;
			cos_value = math.cos(theta)
			sin_value = math.sin(theta)
			total_X += x[k] * cos_value + y[k] * sin_value
			total_Y += y[k] * cos_value - x[k] * sin_value
		total_X /= N
		total_Y /= N
		ret.push((total_X, total_Y))
	return ret
# get inverse fourier descriptors
# param: (X_u, Y_u) uth fd, count from the middle
# param:  M, number of fds to reconstruct the original contour
#		  M must be odd
def get_inv_fd(X, Y, M):
	if len(X) != len(Y):
		print "Error: The length of input x and y should be equal"
		return
	if M % 2 == 0:
		print "Error: M must be odd"
		return
	N = len(X)
	for k in range(0, N):
		total_x = 0
		total_y = 0
		left = int(N / 2) - 1 - int( M / 2)
		right = int(N / 2) + int( M / 2)
		for u in range(left, right):
			theta = 2 * 3.14159 * u * k / N;
			cos_value = math.cos(theta)
			sin_value = math.sin(theta)
			
			total_x += X[u] * cos_value - Y[u] * sin_value
			total_y += Y[u] * cos_value + X[u] * sin_value
		ret.push((total_x, total_y))
	return ret

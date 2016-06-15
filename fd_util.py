import sys
import math
# get fourier descriptors
def get_fd(x, y):
	if len(x) != len(y):
		print "Error: The length of input x and y should be equal"
		return
	N = len(x)
	ret_x = []
	ret_y = []
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
		ret_x.append(total_X)
		ret_y.append(total_Y)	
		#ret.push((total_X, total_Y))
	return ret_x, ret_y
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
			
			total_x += X[u] * cos_value - Y[u] * sin_value
			total_y += Y[u] * cos_value + X[u] * sin_value
		for u in range(N - half, N):
			theta = 2 * 3.14159 * u * k / N;
			cos_value = math.cos(theta)
			sin_value = math.sin(theta)
			
			total_x += X[u] * cos_value - Y[u] * sin_value
			total_y += Y[u] * cos_value + X[u] * sin_value
		ret_x.append(total_x)
		ret_y.append(total_y)
		#ret.push((total_x, total_y))
	return ret_x, ret_y


# -*- coding: utf-8 -*-
"""
Description: 
    
Created on %(date)s

@author: %(username)s

Contact: tpluu2207 at gmail.com
"""
# =============================================================================
# IMPORT PACKAGES
import os, sys, inspect, time
import cv2 
import numpy as np
from matplotlib import pyplot as plt
# Custom packages
from luu_utils import get_varargin
# =============================================================================
def face_detect (imFilePath, **kwargs): # add counter in argument for multiple image files (i.e. in a video)
	# face dete
	# Options
	save_fig = get_varargin(kwargs, 'save_fig', True);
	print_output = get_varargin(kwargs, 'print_output', True);
	max_faces = get_varargin(kwargs, 'max_faces', 4);
	
	# BEGIN
	face_cascade = cv2.CascadeClassifier ('./models/haarcascade_frontalface_default.xml')
	# eye_cascade = cv2.CascadeClassifier ('haarcascade_eye.xml')


	img = cv2.imread (imFilePath)
	gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)

	#finding faces in the image
	faces = face_cascade.detectMultiScale (gray, 1.2, max_faces)

	# faces is a tuple and the ouput are of the form (x, y, w, h) 
	# the x,y coordinates of the upper left hand corner and
	#  the w, h which is the width adn height of the face respectively

	# initializing the lists
	centroid_x = [0] * len(faces) # where len(faces) is the number of faces detected
	centroid_y = [0] * len(faces)

	index = 0
	for (x,y,w,h) in faces:
		# drawing the rectangles on the faces
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]

	    centroid_x[index] = x+ (w/2)
	    centroid_y[index] = y+ (h/2)

	    index +=1;
	if save_fig is True:
		figname = imFilePath.replace(".jpg", "_output.jpg");
		print("Save fig: {}".format(figname))
		cv2.imwrite(figname, img)
		cv2.imshow('img', img)
		# cv2.waitKey(0)
		cv2.destroyAllWindows()

	centroid = [centroid_x, centroid_y]
	if print_output is True:
		print("Centroids: {}".format(centroid))
	return centroid
	# parse the result of this as such list of lists
	# [ [list of all the x-centroids] , [list of all the y-centroids]]
#
# MAIN
def main():
    print('RUNNING: %s' % inspect.stack()[0][3])    
    startTime = time.time();
    # ==== BEGIN ====
    face_detect('./images/sample.jpg', save_fig = False, print_output = True)
    # img = cv2.imread('sample.jpg',0)
    # plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    # plt.show()
# ==== END ====
    print('DONE: {}. Elapsed time: {:.2f}s'.format(inspect.stack()[0][3], 
          time.time()-startTime));
# =============================================================================
# DEBUG
if __name__ == '__main__':
    main()
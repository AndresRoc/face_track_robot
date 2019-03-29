# -*- coding: utf-8 -*-
"""
Description: 
    
Created on %(date)s

@author: %(username)s

Contact: tpluu2207 at gmail.com
"""
# =============================================================================
# IMPORT PACKAGES
import os, inspect, datetime, time
import numpy as np
import cv2
# Custom packages
from luu_utils import get_varargin
# =============================================================================
# SETTINGS and GLOBAL VARIABLES
# =============================================================================
def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
# =============================================================================
def cascade_detect(img, face_cascade, **kwargs):
    # Parse input arguments
    scaleFactor = get_varargin(kwargs, 'scaleFactor', 1.2);
    minNeighbors = get_varargin(kwargs, 'minNeighbors', 4);
    minSize = get_varargin(kwargs, 'minSize', (10,10));
    maxSize = get_varargin(kwargs, 'maxSize', (200,200));
    # =======
    # Convert Image to Gray
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = face_cascade.detectMultiScale(gray_img, scaleFactor, minNeighbors, 
                                        minSize = minSize, maxSize = maxSize);
    if len(rects) == 0:
        return []
    print(rects)
    print(type(rects))
    centroids = centroid_rects(rects);
    return rects, centroids
# =============================================================================
def cascade_detect_one_face(img, face_cascade, **kwargs):
    # Parse input arguments
    scaleFactor = get_varargin(kwargs, 'scaleFactor', 1.2);
    minNeighbors = get_varargin(kwargs, 'minNeighbors', 4);
    minSize = get_varargin(kwargs, 'minSize', (10,10));
    maxSize = get_varargin(kwargs, 'maxSize', (200,200));
    # =======
    # Convert Image to Gray
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = face_cascade.detectMultiScale(gray_img, scaleFactor, minNeighbors, 
                                        minSize = minSize, maxSize = maxSize);
    if len(rects) == 0:
        return [[0,0,0,0]], [0,0]
    centroids = centroid_rects(rects);
    return [rects[0]], centroids[0]   
# =============================================================================
def save_fig(img, **kwargs):
    print('RUNNING: %s' % inspect.stack()[0][3])    
    startTime = time.time();
    # ==== BEGIN ====
    fig_path = get_varargin(kwargs, "file_path", "./fig_output.jpg");
    print("Save fig: {}".format(fig_path))
    cv2.imwrite(fig_path, img)
     # ==== END ====
    print('DONE: {}. Elapsed time: {:.2f}s'.format(inspect.stack()[0][3], 
          time.time()-startTime));
# =============================================================================
def draw_rect_faces(img, faces):
    if len(faces) != 0:
    	for (x,y,w,h) in faces:
    		# drawing the rectangles on the faces
    	    cv2.rectangle(img,(x,y),(x+w,y+h), color = (0,255,0), thickness = 2)
# =============================================================================
def centroid_rects(rects):
    centroids = np.zeros((len(rects), 2));
    index = 0;
    for (x,y,w,h) in rects:
        centroids[index] = [x+(w/2), y+(h/2)];
        index += 1;
    return centroids
# =============================================================================
# MAIN
def main():
    print('RUNNING: %s' % inspect.stack()[0][3])    
    startTime = time.time();
    # ==== BEGIN ====
    model_path = './models/haarcascade_frontalface_default.xml';
    face_cascade = cv2.CascadeClassifier (model_path)
    img = cv2.imread('./images/sample.jpg');
    # faces, centroids = cascade_detect(img, face_cascade)
    faces, centroids = cascade_detect_one_face(img, face_cascade);
    draw_rect_faces(img, faces)
    save_fig(img, file_path = './sample_output_2.jpg')
    print(faces)
    print(centroids)
    # ==== END ====
    print('DONE: {}. Elapsed time: {:.2f}s'.format(inspect.stack()[0][3], 
          time.time()-startTime));
# =============================================================================
# DEBUG
if __name__ == '__main__':
    main()
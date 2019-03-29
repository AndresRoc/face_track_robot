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
import face_track_lib as my_facetrack
# local modules
from video import create_capture
from common import clock, draw_str
# =============================================================================
# SETTINGS and GLOBAL VARIABLES

# =============================================================================
def kalman_face_track_init(trackPoint, **kwargs):
    dynamParams = get_varargin(kwargs, 'dynam_params', 4);     # State matrix dimension
    measureParams = get_varargin(kwargs, 'measure_params', 2); # Output dimension, x,y
    controlParams = get_varargin(kwargs, 'control_params', 0); # Used as estimator
    
    kalman = cv2.KalmanFilter(dynamParams, measureParams, controlParams);
    #  Initialize
    kalman.transitionMatrix = np.array([[1., 0., .1, 0.],
                                        [0., 1., 0., .1],
                                        [0., 0., 1., 0.],
                                        [0., 0., 0., 1.]])
    kalman.measurementMatrix = 1. * np.eye(2, 4)
    kalman.processNoiseCov = 1e-5 * np.eye(4, 4)
    kalman.measurementNoiseCov = 1e-3 * np.eye(2, 2)
    kalman.errorCovPost = 1e-1 * np.eye(4, 4)
    # Write track point for first frame
    kalman.statePost = np.array([trackPoint[0], trackPoint[1], 0 , 0], dtype = 'float64');
    pt = (0,   trackPoint[0], trackPoint[1])
    return kalman
# =============================================================================
def kalman_face_track(kalman, trackPoint, **kwargs):
    prediction = kalman.predict();
    state = kalman.statePost;
    framecount = 1;
    if np.count_nonzero(trackPoint) != 0 :
        state = np.array([trackPoint[0], trackPoint[1], 0 , 0], dtype = 'float64');
        measurement = (np.dot(kalman.measurementNoiseCov, np.random.randn(2, 1))).reshape(-1)
        measurement = np.dot(kalman.measurementMatrix, state) + measurement
        posterior = kalman.correct(measurement)
        pos = (posterior[0], posterior[1])
    else:
        measurement = (np.dot(kalman.measurementNoiseCov, np.random.randn(2, 1))).reshape(-1)
        measurement = np.dot(kalman.measurementMatrix, state) + measurement
        pos = (prediction[0], prediction[1])
    process_noise = np.sqrt(kalman.processNoiseCov[0, 0]) * np.random.randn(4, 1)
    state = np.dot(kalman.transitionMatrix, state) + process_noise.reshape(-1)
    # pt = (frameCounter, pos[0], pos[1])
    return kalman, pos
# =============================================================================
# MAIN
def main():
    print('RUNNING: %s' % inspect.stack()[0][3])    
    startTime = time.time();
    # ==== BEGIN ====
    model_path = './models/haarcascade_frontalface_default.xml';
    face_cascade = cv2.CascadeClassifier (model_path)
    cam = create_capture(0, fallback='synth:bg=./images/lena.jpg:noise=0.05')
    ret, frame = cam.read()
    # frame = cv2.imread('./images/sample.jpg');
    # frame = cv2.imread('./fruits.jpg');
    # Initialize First frame
    # detect face in first frame
    rect, centroid = my_facetrack.cascade_detect_one_face(frame, face_cascade)
    kalman = kalman_face_track_init(centroid);
    while True:
        t = clock()
        ret, frame = cam.read();
        if not ret:
            break;
        prediction = kalman.predict()
        pos = 0;
        faces, centroid = my_facetrack.cascade_detect_one_face(frame, face_cascade);
        kalman, pos = kalman_face_track(kalman, centroid);
        my_facetrack.draw_rect_faces(frame, faces)
        cv2.circle(frame, (int(pos[0]), int(pos[1])) ,20, color = (0,0,255));
        dt = (clock() - t)*1000;
        draw_str(frame, (20, 20), 'time: %.1f ms' % (dt))
        cv2.imshow('facedetect', frame)
        print(pos);
        if cv2.waitKey(5) == 27:
            break
    # ==== END ====
    print('DONE: {}. Elapsed time: {:.2f}s'.format(inspect.stack()[0][3], 
          time.time()-startTime));
# =============================================================================
# DEBUG
if __name__ == '__main__':
    main()
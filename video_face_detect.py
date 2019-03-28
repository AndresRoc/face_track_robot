#!/usr/bin/env python

'''
face detection using haar cascades
USAGE:
    facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2

# local modules
from video import create_capture
from common import clock, draw_str


def detect(img, cascade):
    # rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
    #                                  flags=cv2.CASCADE_SCALE_IMAGE)
    rects = cascade.detectMultiScale(img, 1.5, 3, minSize = (20,20), maxSize=(200,200));
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def main():
    import sys, getopt

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try:
        video_src = video_src[0]
    except:
        video_src = 0
    args = dict(args)
    # cascade_fn = args.get('--cascade', "./models/haarcascade_frontalface_alt.xml")
    # nested_fn  = args.get('--nested-cascade', "./models/haarcascade_eye.xml")

    # cascade = cv2.CascadeClassifier(('./models/haarcascade_frontalface_default.xml'))
    cascade = cv2.CascadeClassifier(('./models/lbpcascade_frontalface.xml'))
    # nested = cv2.CascadeClassifier(('./models/haarcascade_eye.xml'))

    cam = create_capture(video_src, fallback='synth:bg=./images/lena.jpg:noise=0.05')


    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        t = clock()
        rects = detect(gray, cascade)
        # rects = cascade.detectMultiScale(img, 1.2, 3);
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        # if not nested.empty():
        #     for x1, y1, x2, y2 in rects:
        #         roi = gray[y1:y2, x1:x2]
        #         vis_roi = vis[y1:y2, x1:x2]
        #         subrects = detect(roi.copy(), nested)
        #         draw_rects(vis_roi, subrects, (255, 0, 0))
        dt = (clock() - t)*1000;

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt))
        cv2.imshow('facedetect', vis)
        # print("Elapsed Time: {:.1f} ms".format(dt))
        print(rects)
        

        if cv2.waitKey(5) == 27:
            break

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv2.destroyAllWindows()
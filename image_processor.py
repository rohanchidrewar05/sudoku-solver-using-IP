import matplotlib.pyplot as plt
import numpy as np
import math
import operator
import os
import cv2
import sys

def getcontourorder(contour):
# Used to map the contour to the correct position in the array
  loc = cv2.boundingRect(contour)
  return math.floor(loc[1]/20)*2000+loc[0]

def l2_dist(pt1,pt2):
# Calculates the L2 distance between points pt1 and pt2
  return np.sqrt((pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2)

def warp(img):
  '''
  Converts the original RGB to gray, applies Gaussian blur if the image is large,
  applies pixel thresolding, finds the largest contour in the image (the boundary around the Sudoku puzzle)
  crops and warps the original image to a square.
  '''
  gray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)

  if max(gray.shape[0],gray.shape[1])>500:
      blurred = cv2.GaussianBlur(gray.copy(), (9,9),0)
  else:
      blurred = gray.copy()

  thresh = cv2.adaptiveThreshold(blurred.copy(),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,7,2 )

  conts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  conts = sorted(conts, key=cv2.contourArea, reverse=True)
  cont = conts[0]

  bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in cont]), key=operator.itemgetter(1))
  top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in cont]), key=operator.itemgetter(1))
  bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in cont]), key=operator.itemgetter(1))
  top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in cont]), key=operator.itemgetter(1))

  original_rect = np.array([cont[top_left][0],cont[top_right][0],cont[bottom_right][0],cont[bottom_left][0]],dtype='float32')

  topleft, topright, bottomright, bottomleft = original_rect

  max_len = int( max( l2_dist(topleft,topright),l2_dist(topright,bottomright),l2_dist(bottomright,bottomleft),l2_dist(bottomleft,topright) ) )
  target_rect = np.array([ [0,0], [max_len,0] ,[max_len,max_len],[0,max_len]] , dtype='float32')

  pers_transform = cv2.getPerspectiveTransform(original_rect,target_rect)
  warped = cv2.warpPerspective(blurred.copy(), pers_transform, (max_len,max_len) )
  after_warp = warped[3:max_len-3,3:max_len-3]
  return after_warp,max_len


def sudoku_extractor(img_name):
  '''
  Locates the position of each box of the sudoku puzzle in the image and extract digits from them.
  '''
  print(img_name)
  img = cv2.imread(img_name)

  warped,maxlen = warp(img)
  boxdims = [int(n) for n in np.linspace(0,maxlen,10)]
  boxlen = int(maxlen/9)
  
  # Reads the template, find the 10 largest contours (each is a digit), and map the index of digits to the appropriate contours
  numbers_template = cv2.imread(os.getcwd()+'/utils/numbers.jpg',0)
  template_conts, _ = cv2.findContours(numbers_template, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  template_conts = sorted(template_conts, key=cv2.contourArea, reverse=True)
  template_conts= template_conts[:10]
  template_conts = sorted(template_conts, key=lambda x:getcontourorder(x))
  digits={}
  for (i,c) in enumerate(template_conts):
    (x,y,w,h)=cv2.boundingRect(c)
    roi = numbers_template[y:y+h ,x:x+w]
    roi = cv2.resize(roi,(35,60))
    digits[i]=roi

  kernelsize = int(maxlen/4)
  if kernelsize%2==0:
    kernelsize+=1

  # For each box in the Sudoku puzzle, apply thresholding followed by flood-filling to isolate the digit inside the box.
  # The digit in each box is matched with each template, and the template with the highest score will be
  matrix=[]
  row=[]
  for y in range(len(boxdims)-1):
    row=[]
    for x in range(len(boxdims)-1):
      x1 = boxdims[x]
      x2 = boxdims[x+1]
      y1 = boxdims[y]
      y2 = boxdims[y+1]
      
      roi = warped[y1:y2, x1:x2]

      roithresh = cv2.adaptiveThreshold(roi,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,kernelsize,2 )

      max_area=boxlen*boxlen*0.05
      seed_point = (int(0.5*boxlen), int(0.5*boxlen))
      flag=0

      for m in range(int(0.3*boxlen), int(0.7*boxlen)):
        for n in range(int(0.3*boxlen), int(0.7*boxlen)):
          if roithresh[n, m] == 255:  
            area = cv2.floodFill(roithresh.copy(), None, (m, n), 150)
            if area[0] > max_area: 
              max_area = area[0]
              seed_point = (m, n)
              flag=1

      if (roithresh[seed_point[1],seed_point[0]]==0) or flag==0:
        num=0
      else:
        flood=0
        flood = cv2.floodFill(roithresh.copy(),None,seed_point,150)

        canvas = roithresh.copy()
        for i in range(canvas.shape[0]):
          for j in range(canvas.shape[1]):
              if flood[1][i][j]==150:
                canvas[i][j]=255
              else:
                canvas[i][j]=0  

        contour = cv2.findContours(canvas,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contour = contour[0]
        (box_x,box_y,box_w,box_h) =cv2.boundingRect(contour[0])
        isolated_digit = canvas[box_y:box_y+box_h ,box_x:box_x+box_w]
        isolated_digit = cv2.resize(isolated_digit,(35,60))

        scores=[]
        for (_,digit_template) in digits.items():
          result = cv2.matchTemplate(isolated_digit, digit_template,cv2.TM_CCOEFF)
          (_,score,_,_) = cv2.minMaxLoc(result)
          scores.append(score)
        num = np.argmax(scores)

      row.append(num)
      
    matrix.append(row)
    
  return matrix

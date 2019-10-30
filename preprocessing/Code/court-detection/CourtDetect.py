import cv2
import numpy as np
from operator import itemgetter
np.set_printoptions(precision=5, suppress=True)

img = cv2.imread('./original_chou.jpg')

#detect all white pixels
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
ret, img_thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)

# ##### USING YCbCr #####
# img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
# Y,Cb,Cr=cv2.split(img_ycrcb)
# # eliminate phase 1
# taw = 8
# sigma_l = 128
# sigma_d = 20
# max_row = np.shape(Y)[0]
# max_col = np.shape(Y)[1]
# img_candidate = Y.copy()

# for row in range(max_row):
#     # if row %100 == 0:
#         # print("row = {}".format(row))
#     for col in range(max_col):
#         candidate_flag = 1
#         for taw_idx in range(1,taw+1):
#             if row - taw_idx < 0 or row + taw_idx >= max_row or col - taw_idx < 0 or col + taw_idx >= max_col:
#                 pass
#             else:
#                 if Y[row][col] >= sigma_l and Y[row][col] - Y[row - taw_idx][col] > sigma_d and Y[row][col] - Y[row + taw_idx][col] > sigma_d: 
#                     candidate_flag = 1
#                 elif Y[row][col] >= sigma_l and Y[row][col] - Y[row][col - taw_idx] > sigma_d and Y[row][col] - Y[row][col + taw_idx] > sigma_d:                       
#                     candidate_flag = 1
#                 else:
#                     candidate_flag = 0
        
#         img_candidate[row][col] = candidate_flag

# #output result
# img_output = img.copy()
# img_output[img_candidate == 1] = 0
# cv2.imwrite('white_pixel_detection_phase1.jpg', img_output)

#### USING GRAY #####
#eliminate phase 1
taw = 8
sigma_l = 200
sigma_d = 15
max_row = np.shape(img_thresh)[0]
max_col = np.shape(img_thresh)[1]
img_candidate = img_thresh.copy()

for row in range(max_row):
    for col in range(max_col):
        candidate_flag = 1
        for taw_idx in range(1,taw+1):
            if row - taw_idx < 0 or row + taw_idx >= max_row or col - taw_idx < 0 or col + taw_idx >= max_col:
                pass
            else:
                if img_thresh[row][col] >= sigma_l and img_thresh[row][col] - img_thresh[row - taw_idx][col] > sigma_d and img_thresh[row][col] - img_thresh[row + taw_idx][col] > sigma_d: 
                    candidate_flag = 1
                elif img_thresh[row][col] >= sigma_l and img_thresh[row][col] - img_thresh[row][col - taw_idx] > sigma_d and img_thresh[row][col] - img_thresh[row][col + taw_idx] > sigma_d:                       
                    candidate_flag = 1
                else:
                    candidate_flag = 0
        
        if candidate_flag == 0:
            img_candidate[row][col] = 0

# # eliminate phase 2 (not used yet)
# # 1,0 : x direction gradient
# sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
# # 0,1 : y direction gradient
# sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)


# Court line candidate dectector
#cv_pi/180
lines = cv2.HoughLines(img_candidate,1,np.pi/180,200)
print(np.shape(lines))
print(len(img_candidate == 1))

# Classify horizon and vertical (pi/2-theta < 25 => horizontal)
horizontal_line = []
vertical_line = []
angle_threshold = 25
print("threshold = {}".format(angle_threshold/180*np.pi))

for i in range(np.shape(lines)[0]):
    # print(float(abs(np.pi/2-lines[i][0][1])))
    if float(abs(np.pi/2-lines[i][0][1])) <= float(angle_threshold/180*np.pi) :
        horizontal_line.append([lines[i][0][0],lines[i][0][1]])
    else:
        vertical_line.append([lines[i][0][0],lines[i][0][1]])

print("horizontal line = {}".format(np.shape(horizontal_line)))
print("vertical line = {}".format(np.shape(vertical_line)))

# convert rho theta to slope and bias. Sort horizontal and vertical lines
horizontal_rho2line =[]
vertical_rho2line =[]
given_y = max_col/2
given_x = max_row/2

for line in horizontal_line:
    rho = line[0]
    theta = line[1]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1e4*(-b))
    y1 = int(y0 + 1e4*(a))
    x2 = int(x0 - 1e4*(-b))
    y2 = int(y0 - 1e4*(a))
    
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    distance_y = m * given_x + b
    

    horizontal_rho2line.append([m,b,distance_y])

print("=======================================")
print(horizontal_rho2line[0:5])
horizontal_line_sorted = sorted(horizontal_rho2line,key=itemgetter(2))
print(horizontal_line_sorted[0:5])
print("=======================================")

for line in vertical_line:
    rho = line[0]
    theta = line[1]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1e4*(-b))
    y1 = int(y0 + 1e4*(a))
    x2 = int(x0 - 1e4*(-b))
    y2 = int(y0 - 1e4*(a))
    
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    distance_x = (given_y - b) / m

    vertical_rho2line.append([m,b,distance_x])

print("=======================================")
print(vertical_rho2line[0:5])
vertical_line_sorted = sorted(vertical_rho2line,key=itemgetter(2))
print(vertical_line_sorted[0:5])
print("=======================================")

print("sorted horizontal line = {}".format(horizontal_line_sorted[0:2]))
print("sorted vertical line = {}".format(vertical_line_sorted[0:2]))

#output result
img_output = img.copy()
img_output[img_thresh == 255] = 0
cv2.imwrite('white_pixel_detection_all.jpg', img_output)


img_output = img.copy()
img_output[img_candidate == 255] = 0
cv2.imwrite('white_pixel_detection_phase1.jpg', img_output)


img_output = img.copy()
for line in horizontal_line:
    m = line[0]
    b = line[1]
    
    x1 = int(1e4)
    y1 = int(m * x1 + b)
    x2 = int(-1e4)
    y2 = int(m * x2 + b)
    cv2.line(img_output,(x1,y1),(x2,y2),(0,0,255),2)

for line in vertical_line:
    m = line[0]
    b = line[1]
    
    x1 = int(1e4)
    y1 = int(m * x1 + b)
    x2 = int(-1e4)
    y2 = int(m * x2 + b)
    cv2.line(img_output,(x1,y1),(x2,y2),(0,255,255),2)
cv2.imwrite('court_line_detection_phase1.jpg', img_output)
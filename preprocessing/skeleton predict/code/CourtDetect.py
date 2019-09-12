
# coding: utf-8

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import json
import cv2


# In[7]:
'''

img = cv2.imread('3417.jpg')
img.shape


# In[89]:


img = cv2.imread('tai.jpg')
img.shape


# # CourtLineCandidateDetector.cpp distanceThreshold = 8 (chou) 

# In[39]:


upper_base_left = (659,527)
lower_base_left = (492,1044)
lower_base_right = (1512,1069)
upper_base_right = (1383,545)

upper_base_leftsingles = (718,529)
lower_base_leftsingles = (576,1046)
lower_base_rightsingles = (1428,1067)
upper_base_rightsingles = (1324,544)

upper_service_leftsingles = (678,673)
upper_service_rightsingles = (1353,689)
lower_service_leftsingles = (637,822)
lower_service_rightsingles = (1383,840)

upper_service_centerservice = (1015,681)
lower_service_centerservice = (1010,831)
left_side_netline = (590,742)
right_side_netline = (1436,763)

cv2.line(img, upper_base_left, upper_base_right, (0, 0, 255), 2)
cv2.line(img, lower_base_left, lower_base_right, (0, 0, 255), 2)
cv2.line(img, upper_base_leftsingles, lower_base_leftsingles, (0, 0, 255), 2)
cv2.line(img, upper_base_rightsingles, lower_base_rightsingles, (0, 0, 255), 2)

cv2.circle(img,upper_base_left, 3, (0, 255, 255), 2)
cv2.circle(img,upper_base_right, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_left, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_right, 3, (0, 255, 255), 2)

cv2.circle(img,upper_base_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,upper_base_rightsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_rightsingles, 3, (0, 255, 255), 2)

cv2.circle(img,upper_service_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,upper_service_rightsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_rightsingles, 3, (0, 255, 255), 2)

cv2.circle(img,upper_service_centerservice, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_centerservice, 3, (0, 255, 255), 2)
cv2.circle(img,left_side_netline, 3, (0, 255, 255), 2)
cv2.circle(img,right_side_netline, 3, (0, 255, 255), 2)

cv2.imwrite('output_chou.jpg', img)


# # CourtLineCandidateDetector.cpp distanceThreshold = 6 (tai)

# In[31]:


upper_base_left = (455,327)
lower_base_left = (326,643)
lower_base_right = (944,641)
upper_base_right = (832,328)

upper_base_leftsingles = (486,327)
lower_base_leftsingles = (377,643)
lower_base_rightsingles = (893,641)
upper_base_rightsingles = (801,327)

upper_service_leftsingles = (459,406)
upper_service_rightsingles = (824,406)
lower_service_leftsingles = (428,494)
lower_service_rightsingles = (850,493)

upper_service_centerservice = (642,406)
lower_service_centerservice = (640,494)
left_side_netline = (406,447)
right_side_netline = (874,446)

cv2.line(img, upper_base_left, upper_base_right, (0, 0, 255), 2)
cv2.line(img, lower_base_left, lower_base_right, (0, 0, 255), 2)
cv2.line(img, upper_base_leftsingles, lower_base_leftsingles, (0, 0, 255), 2)
cv2.line(img, upper_base_rightsingles, lower_base_rightsingles, (0, 0, 255), 2)

cv2.circle(img,upper_base_left, 3, (0, 255, 255), 2)
cv2.circle(img,upper_base_right, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_left, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_right, 3, (0, 255, 255), 2)

cv2.circle(img,upper_base_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,upper_base_rightsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_rightsingles, 3, (0, 255, 255), 2)

cv2.circle(img,upper_service_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,upper_service_rightsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_rightsingles, 3, (0, 255, 255), 2)

cv2.circle(img,upper_service_centerservice, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_centerservice, 3, (0, 255, 255), 2)
cv2.circle(img,left_side_netline, 3, (0, 255, 255), 2)
cv2.circle(img,right_side_netline, 3, (0, 255, 255), 2)

cv2.imwrite('output_tai.jpg', img)


# # CourtLineCandidateDetector.cpp distanceThreshold = 6 (chou)

# In[42]:


upper_base_left = (599,525)
lower_base_left = (408,1042)
lower_base_right = (1511,1069)
upper_base_right = (1383,546)

upper_base_leftsingles = (664,527)
lower_base_leftsingles = (499,1044)
lower_base_rightsingles = (1421,1067)
upper_base_rightsingles = (1319,544)

upper_service_leftsingles = (618,671)
upper_service_rightsingles = (1347,690)
lower_service_leftsingles = (571,820)
lower_service_rightsingles = (1377,841)

upper_service_centerservice = (983,680)
lower_service_centerservice = (974,830)
left_side_netline = (520,740)
right_side_netline = (1437,763)

cv2.line(img, upper_base_left, upper_base_right, (0, 0, 255), 2)
cv2.line(img, lower_base_left, lower_base_right, (0, 0, 255), 2)
cv2.line(img, upper_base_leftsingles, lower_base_leftsingles, (0, 0, 255), 2)
cv2.line(img, upper_base_rightsingles, lower_base_rightsingles, (0, 0, 255), 2)

cv2.circle(img,upper_base_left, 3, (0, 255, 255), 2)
cv2.circle(img,upper_base_right, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_left, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_right, 3, (0, 255, 255), 2)

cv2.circle(img,upper_base_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,upper_base_rightsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_base_rightsingles, 3, (0, 255, 255), 2)

cv2.circle(img,upper_service_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,upper_service_rightsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_leftsingles, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_rightsingles, 3, (0, 255, 255), 2)

cv2.circle(img,upper_service_centerservice, 3, (0, 255, 255), 2)
cv2.circle(img,lower_service_centerservice, 3, (0, 255, 255), 2)
cv2.circle(img,left_side_netline, 3, (0, 255, 255), 2)
cv2.circle(img,right_side_netline, 3, (0, 255, 255), 2)

cv2.imwrite('output_chou.jpg', img)

'''
# ## Test projection

# In[2]:


import numpy as np
import cv2
X=np.array([[414,604],[831,1065],[1827,974],[1116,561]],np.float32)
print(np.shape(X))
print(type(X))
Y=np.array([[457,319],[312,676],[1012,676],[862,319]],np.float32)
print(type(Y))
print(np.shape(Y))
print(cv2.getPerspectiveTransform(X,Y))


# # Draw ground truth court

# In[6]:


# 單位:mm
def draw_court():
    upper_base_left = (0,0)
    lower_base_left = (0,1340)
    lower_base_right = (610,1340)
    upper_base_right = (610,0)

    upper_base_leftsingles = (42,0)
    lower_base_leftsingles = (42,1340)
    lower_base_rightsingles = (568,1340)
    upper_base_rightsingles = (568,0)

    upper_secondbase_leftsingles = (0,72)
    lower_secondbase_leftsingles = (0,1268)
    lower_secondbase_rightsingles = (610,1268)
    upper_secondbase_rightsingles = (610,72)

    left_side_netline = (0,670)
    right_side_netline = (610,670)

    upper_service_leftsingles = (0,472)
    upper_service_rightsingles = (610,472)
    lower_service_leftsingles = (0,868)
    lower_service_rightsingles = (610,868)

    upper_service_centerservice_up = (305,0)
    upper_service_centerservice_bottom = (305,472)
    lower_service_centerservice_up = (305,868)
    lower_service_centerservice_bottom = (305,1340)


    img = np.zeros((1920,1080,3),np.uint8)

    cv2.line(img, upper_base_left, upper_base_right, (255, 255, 255), 4)
    cv2.line(img, upper_base_left, lower_base_left, (255, 255, 255), 4)
    cv2.line(img, lower_base_left, lower_base_right, (255, 255, 255), 4)
    cv2.line(img, lower_base_right, upper_base_right, (255, 255, 255), 4)

    cv2.line(img, upper_base_leftsingles, upper_base_rightsingles, (255, 255, 255), 4)
    cv2.line(img, upper_base_leftsingles, lower_base_leftsingles, (255, 255, 255), 4)
    cv2.line(img, lower_base_leftsingles, lower_base_rightsingles, (255, 255, 255), 4)
    cv2.line(img, lower_base_rightsingles, upper_base_rightsingles, (255, 255, 255), 4)

    cv2.line(img, upper_secondbase_leftsingles, upper_secondbase_rightsingles, (255, 255, 255), 4)
    cv2.line(img, lower_secondbase_leftsingles, lower_secondbase_rightsingles, (255, 255, 255), 4)

    cv2.line(img, left_side_netline, right_side_netline, (0, 0, 255), 4)

    cv2.line(img, upper_service_leftsingles, upper_service_rightsingles, (255, 255, 255), 4)
    cv2.line(img, lower_service_leftsingles, lower_service_rightsingles, (255, 255, 255), 4)

    cv2.line(img, upper_service_centerservice_up, upper_service_centerservice_bottom, (255, 255, 255), 4)
    cv2.line(img, lower_service_centerservice_up, lower_service_centerservice_bottom, (255, 255, 255), 4)
    
    return img

'''
# In[86]:


#Test real-world and tai court homorgraphy,座標有包含外面的2M(don't move)
src=np.array([[1010,1740],[0,1740],[1010,0],[0,0]],np.float32)
dst=np.array([[1103,716],[226,716],[895,307],[424,307]],np.float32)

test_dst = np.array([1010,1740,1])

H = cv2.getPerspectiveTransform(src,dst)
print(H)
# inv_H = np.linalg.inv(H)
# inv_point = inv_H.dot(test_Y.transpose())
# inv_point.round()

# point = H.dot(test_dst.transpose()).round().astype(int)
point = H.dot(test_dst.transpose()).round(3)
point /= point[2]
point.astype(int)

# src_img = cv2.imread('tai.jpg')

# print(tuple([src_img.shape[0],src_img.shape[1]]))

# perspective = cv2.warpPerspective(src_img, H, tuple([src_img.shape[0],src_img.shape[1]]), cv2.INTER_LINEAR)
# cv2.imwrite( "./tai_perspective.jpg", perspective);


# In[28]:
'''

player_bot = pd.read_csv('../../skeleton/bot_player_info_0_6_3.csv')
player_top = pd.read_csv('../../skeleton/top_player_info_0_6_3.csv')
video_name = 'project_skeleton.avi'

dst=np.array([[610,1340],[0,1340],[610,0],[0,0]],np.float32)

# 影像中球場位置(右下、左下、右上、左上)
src=np.array([[1011,671],[276,671],[880,383],[404,383]],np.float32)

H = cv2.getPerspectiveTransform(src,dst)
print(H)
# point = H.dot(test_dst.transpose()).round(3)
# point /= point[2]
# point = point.astype(int)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

video = cv2.VideoWriter(video_name, fourcc, 25, (1080,1920))

for i in range(len(player_bot)):
    img = draw_court()
    
    #middle point of bottom player
    bot_mid_x = (player_bot['x11'][i] + player_bot['x14'][i])/2
    bot_mid_y = (player_bot['y11'][i] + player_bot['y14'][i])/2
    bot_mid_point = np.array([bot_mid_x,bot_mid_y,1])
    bot_H_point = H.dot(bot_mid_point.transpose()).round(3)
    bot_H_point /= bot_H_point[2]
    bot_H_point = bot_H_point.astype(int)
    bot_point = tuple([bot_H_point[0],bot_H_point[1]])
    cv2.circle(img, bot_point, 3, (0, 255, 255), 3)
    
    #middle point of top player
    top_mid_x = (player_top['x11'][i] + player_top['x14'][i])/2
    top_mid_y = (player_top['y11'][i] + player_top['y14'][i])/2
    top_mid_point = np.array([top_mid_x,top_mid_y,1])
    top_H_point = H.dot(top_mid_point.transpose()).round(3)
    top_H_point /= top_H_point[2]
    top_H_point = top_H_point.astype(int)
    top_point = tuple([top_H_point[0],top_H_point[1]])
    cv2.circle(img, top_point, 3, (255, 0, 255), 3)
    
    #right ankle and left ankle of bottom player
    bot_right_ankle = np.array([player_bot['x11'][i],player_bot['y11'][i],1])
    bot_H_right_ankle = H.dot(bot_right_ankle.transpose()).round(3)
    bot_H_right_ankle /= bot_H_right_ankle[2]
    bot_H_right_ankle = bot_H_right_ankle.astype(int)
    bot_H_right_ankle = tuple([bot_H_right_ankle[0],bot_H_right_ankle[1]])
    bot_left_ankle = np.array([player_bot['x14'][i],player_bot['y14'][i],1])
    bot_H_left_ankle = H.dot(bot_left_ankle.transpose()).round(3)
    bot_H_left_ankle /= bot_H_left_ankle[2]
    bot_H_left_ankle = bot_H_left_ankle.astype(int)
    bot_H_left_ankle = tuple([bot_H_left_ankle[0],bot_H_left_ankle[1]])
    cv2.line(img, bot_H_right_ankle, bot_H_left_ankle, (0, 255, 255), 3)
    cv2.circle(img, bot_H_right_ankle, 3, (255, 0, 0), 3)
    cv2.circle(img, bot_H_left_ankle, 3, (0, 0, 255), 3)
    
    #right ankle and left ankle of top player
    top_right_ankle = np.array([player_top['x11'][i],player_top['y11'][i],1])
    top_H_right_ankle = H.dot(top_right_ankle.transpose()).round(3)
    top_H_right_ankle /= top_H_right_ankle[2]
    top_H_right_ankle = top_H_right_ankle.astype(int)
    top_H_right_ankle = tuple([top_H_right_ankle[0],top_H_right_ankle[1]])
    top_left_ankle = np.array([player_top['x14'][i],player_top['y14'][i],1])
    top_H_left_ankle = H.dot(top_left_ankle.transpose()).round(3)
    top_H_left_ankle /= top_H_left_ankle[2]
    top_H_left_ankle = top_H_left_ankle.astype(int)
    top_H_left_ankle = tuple([top_H_left_ankle[0],top_H_left_ankle[1]])
    cv2.line(img, top_H_right_ankle, top_H_left_ankle, (0, 255, 255), 3)
    cv2.circle(img, top_H_right_ankle, 3, (255, 0, 0), 3)
    cv2.circle(img, top_H_left_ankle, 3, (0, 0, 255), 3)
    
    print(top_right_ankle)
    video.write(img)

cv2.destroyAllWindows()
video.release()
print(len(player_bot))


# In[152]:


inv_point = np.array([333, 344, 1])
inv_H = np.linalg.inv(H)
inv_point = inv_H.dot(inv_point.transpose())
inv_point /= inv_point[2]
inv_point.astype(int)


# # Compute camera matrix
# #### 網子高度是1.55M左右

# In[6]:


src=np.array([[610,1340],[0,1340],[610,0],[0,0]],np.float32)
dst=np.array([[1011,671],[276,671],[880,383],[404,383]],np.float32)

H = cv2.getPerspectiveTransform(src,dst)
print(H)
test_dst = np.array([1011,671,1])
inv_H = np.linalg.inv(H)
point = inv_H.dot(test_dst.transpose()).round(3)
point /= point[2]
point = point.astype(int)
point


# In[8]:


net_h = 1550
camera_matrix = np.insert(H, 2, np.array((0, 0, 0)), 1)
print(camera_matrix)
y0 = camera_matrix[1][3]/camera_matrix[2][3]
yn = 140  #use darklabel check net height in image system
m23 = (yn - y0)*camera_matrix[2][3]/net_h
camera_matrix[1][2] = m23
print(camera_matrix)


# In[8]:


real_world = []
image_coord = [[554,408,1],[545,395,1],[541,392,1]]
for coord in image_coord:
    print(coord)
    inv_camera_matrix = np.linalg.inv(camera_matrix)
    point = inv_camera_matrix.dot(coord.transpose()).round(3)   #camera matrix not square,it's 3x4
    point /= point[2]
    point = point.astype(int)
    real_world.append(point)
    
point


# In[ ]:


src=np.array([[610,1340],[0,1340],[610,0],[0,0]],np.float32)
dst=np.array([[1011,671],[276,671],[880,383],[404,383]],np.float32)

H = cv2.getPerspectiveTransform(src,dst)
print(H)
test_dst = np.array([1011,671,1])
inv_H = np.linalg.inv(H)
point = inv_H.dot(test_dst.transpose()).round(3)
point /= point[2]
point = point.astype(int)
point


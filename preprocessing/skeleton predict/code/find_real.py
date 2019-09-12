import pandas as pd
import matplotlib.pyplot as plt
import math
import json
import numpy as np
import cv2

def save_to_csv(sets, frame, top_x, top_y, bot_x, bot_y):
    result = pd.DataFrame([])
    result['frame'] = frame
    result['top_x'] = top_x
    result['top_y'] = top_y
    result['bot_x'] = bot_x
    result['bot_y'] = bot_y

    result.to_csv("../data/set"+str(sets+1)+"_skeleton.csv", index=False, encoding = 'utf-8')

player_bot = pd.read_csv('../data/bottom_player_skeleton.csv')
player_top = pd.read_csv('../data/top_player_skeleton.csv')

# 真實世界球場位置
dst=np.array([[610,1340],[0,1340],[610,0],[0,0]], np.float32)

# 影像中球場位置(右下、左下、右上、左上): !!! 要重新確認座標點 !!!
src=np.array([[1011,671],[276,671],[880,383],[404,383]], np.float32)

H = cv2.getPerspectiveTransform(src,dst)

frame = []
top_x = []
top_y = []
bot_x = []
bot_y = []
sets = 0

for i in range(len(player_bot)):
    #img = draw_court()
    if sets != int(player_bot['set'][i]):
        save_to_csv(sets, frame, top_x, top_y, bot_x, bot_y)
        frame = []
        top_x = []
        top_y = []
        bot_x = []
        bot_y = []
        sets = int(player_bot['set'][i])

    frame.append(player_bot['frame_id'][i])

    # middle point of bottom player
    bot_mid_x = (player_bot['x11'][i] + player_bot['x14'][i])/2
    bot_mid_y = (player_bot['y11'][i] + player_bot['y14'][i])/2
    bot_mid_point = np.array([bot_mid_x,bot_mid_y,1])
    bot_H_point = H.dot(bot_mid_point.transpose()).round(3)
    bot_H_point /= bot_H_point[2]
    bot_H_point = bot_H_point.astype(int)
    bot_point = tuple([bot_H_point[0],bot_H_point[1]])
    
    # middle point of top player
    top_mid_x = (player_top['x11'][i] + player_top['x14'][i])/2
    top_mid_y = (player_top['y11'][i] + player_top['y14'][i])/2
    top_mid_point = np.array([top_mid_x,top_mid_y,1])
    top_H_point = H.dot(top_mid_point.transpose()).round(3)
    top_H_point /= top_H_point[2]
    top_H_point = top_H_point.astype(int)
    top_point = tuple([top_H_point[0],top_H_point[1]])
    
    # right ankle and left ankle of bottom player
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
    bot_x.append(bot_H_left_ankle[0])
    bot_y.append(bot_H_left_ankle[1])
    
    # right ankle and left ankle of top player
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
    top_x.append(top_H_left_ankle[0])
    top_y.append(top_H_left_ankle[1])

save_to_csv(sets, frame, top_x, top_y, bot_x, bot_y)
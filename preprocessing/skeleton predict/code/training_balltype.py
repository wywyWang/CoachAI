import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn import svm
from sklearn.metrics import *
from sklearn.model_selection import *
from xgboost import XGBClassifier
from functions import *

needed = ['now_right_x', 'now_right_y', 'now_left_x', 'now_left_y', 
		'next_right_x', 'next_right_y', 'next_left_x', 'next_left_y', 
		'right_delta_x', 'right_delta_y', 'left_delta_x', 'left_delta_y',
		'right_x_speed', 'right_y_speed','right_speed',
		'left_x_speed', 'left_y_speed', 'left_speed', 'hit_height', 'type', 'avg_ball_speed']
train_needed = ['now_right_x', 'now_right_y', 'now_left_x', 'now_left_y', 
		'next_right_x', 'next_right_y', 'next_left_x', 'next_left_y', 
		'right_delta_x', 'right_delta_y', 'left_delta_x', 'left_delta_y',
		'right_x_speed', 'right_y_speed','right_speed',
		'left_x_speed', 'left_y_speed', 'left_speed', 'avg_ball_speed']
test_needed = ['type']

def LoadData(filename, ball_height_predict):
	data = pd.read_csv(filename)
	ball_height = pd.read_csv(ball_height_predict)
	data = data[needed]
	data.dropna(inplace=True)
	data.reset_index(drop=True, inplace=True)
	data = data[data.type != '未擊球' and data.type != '掛網球' and data.tpye != '未過網' and data.type != '發球犯規']
	
	eng_type_to_num = {'cut': 1, 'drive': 2, 'lob': 3, 'long': 4, 'netplay': 5, 'rush': 6, 'smash': 7, 'error': 8}

	ball_type = []

	for t in data['type']:
		ball_type.append(eng_type_to_num[ball_type_convertion(t)])
	
	data['type'] = ball_type
	data['Predict'] = ball_height['Predict']

	x_train = data[train_needed+['Predict']]
	y_train = ball_type
	
	y_train = np.array(y_train).ravel()
	return x_train, y_train

def SVM(x_train, y_train, model_name):
	model = svm.SVC(kernel='rbf')
	model.fit(x_train, y_train)
	joblib.dump(model, model_name)

def XGBoost(x_train, y_train, model_name):
	params = {
        'learning_rate': 0.01,
        'n_estimators': 1000,
        'max_depth': 4,
        'min_child_weight': 1,
        'gamma': 0,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'reg_alpha': 0.005,
        'objective':'binary:logistic',
        'scale_pos_weight': 1
    }
	xgbc = XGBClassifier()
	xgbc.fit(x_train, y_train)
	joblib.dump(xgbc, model_name)

def Run(filename, svm_option, svm_model_name, svm_ball_height_predict_result, xgboost_option, xgboost_model_name, xgboost_ball_height_predict_result):
	
	if svm_option and svm_model_name != '':
		print("SVM training...")
		x_train, y_train = LoadData(filename, svm_ball_height_predict_result)
		SVM(x_train, y_train, svm_model_name)
		print("SVM training done!")
	if xgboost_option and xgboost_model_name != '':
		print("XGBoost training...")
		x_train, y_train = LoadData(filename, xgboost_ball_height_predict_result)
		XGBoost(x_train, y_train, xgboost_model_name)
		print("XGBoost training done!")

Run('../data/set1_with_skeleton.csv', False, '../model/SVM_balltype.joblib.dat', '../data/result/SVM_set1_skeleton_out.csv',True, '../model/XGB_balltype.joblib.dat', '../data/result/XGB_set1_skeleton_out.csv')
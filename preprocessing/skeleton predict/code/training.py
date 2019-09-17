import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn import svm
from sklearn.metrics import *
from sklearn.model_selection import *
from xgboost import XGBClassifier



needed = ['ball_round', 'pos_x', 'pos_y', 'next_x', 'next_y', 'hit_height']
train_needed = ['ball_round', 'pos_x', 'pos_y', 'next_x', 'next_y']
test_needed = ['hit_height']

def convert_area(area):
	val = {'E': 0, 'C': 4, 'A': 8, 'B': 12, 'D': 16}
	return float(val[area[0]]+float(area[1]))

def LoadData(filename):
	data = pd.read_csv(filename)
	data = data[needed]
	data.dropna(inplace=True)
	x_train = data[train_needed]
	y_train = data[test_needed].values

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
	'''
	xgbc = XGBClassifier(**params)
	grid_params = {
        'learning_rate': [i/100.0 for i in range(1,6)],
        'max_depth': range(3,6),
        #'min_child_weight': range(0,10,1),
        #'subsample': [i/10.0 for i in range(6,9)],
        #'colsample_bytree': [i/10.0 for i in range(6,9)],
        'gamma': [i/10.0 for i in range(0,6)],
        'reg_alpha':[1e-5, 1e-2, 0.1, 1, 100]
    }
	grid = GridSearchCV(xgbc, grid_params, cv = 5)

	xgboost_model = grid.fit(x_train, y_train)
	'''
	xgbc.fit(x_train, y_train)
	joblib.dump(xgbc, model_name)

def Run(filename, svm_option, svm_model_name, xgboost_option, xgboost_model_name):
	x_train, y_train = LoadData(filename)
	if svm_option and svm_model_name != '':
		print("SVM training...")
		SVM(x_train, y_train, svm_model_name)
		print("SVM training done!")
	if xgboost_option and xgboost_model_name != '':
		print("XGBoost training...")
		XGBoost(x_train, y_train, xgboost_model_name)
		print("XGBoost training done!")

Run('../data/set1_with_skeleton.csv', False, 'SVM.joblib.dat', True, 'XGB.joblib.dat')
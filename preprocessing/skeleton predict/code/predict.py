import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.externals import joblib
from sklearn import svm
from sklearn.metrics import *
from xgboost import XGBClassifier

needed = ['ball_round', 'pos_x', 'pos_y', 'next_x', 'next_y', 'hit_height']
test_needed = ['ball_round', 'pos_x', 'pos_y', 'next_x', 'next_y']

def convert_area(area):
	val = {'E': 0, 'C': 4, 'A': 8, 'B': 12, 'D': 16}
	return float(val[area[0]]+float(area[1]))

def LoadData(filename):
	data = pd.read_csv(filename)
	data = data[needed]
	data.dropna(inplace=True)
	x_predict = data[test_needed]

	return x_predict

def SVM(filename, x_predict, model_name, svm_outputname):
	data = pd.read_csv(filename)
	data = data[needed]
	data.dropna(inplace=True)

	model = joblib.load(model_name)
	prediction = model.predict(x_predict)

	result = pd.DataFrame([])
	result['Real'] = data['hit_height']
	result['Predict'] = prediction

	result.to_csv(svm_outputname,index=None)

	print("Accuracy: "+str(accuracy_score(data['hit_height'], prediction)))
	print("Precision: "+str(precision_score(data['hit_height'], prediction, labels = [1, 2], average=None)))
	print("Recall: "+str(recall_score(data['hit_height'], prediction, labels = [1, 2], average=None)))


def XGBoost(filename, x_predict, model_name, xgb_outputname):
	data = pd.read_csv(filename)
	data = data[needed]
	data.dropna(inplace=True)

	model = joblib.load(model_name)
	prediction = model.predict(x_predict)

	result = pd.DataFrame([])
	result['Real'] = data['hit_height']
	result['Predict'] = prediction

	result.to_csv(xgb_outputname, index=None)

	print("Accuracy: "+str(accuracy_score(data['hit_height'], prediction)))
	print("Precision: "+str(precision_score(data['hit_height'], prediction, labels = [1, 2], average=None)))
	print("Recall: "+str(recall_score(data['hit_height'], prediction, labels = [1, 2], average=None)))



def Run(filename, svm_option, svm_model_name, svm_outputname, xgboost_option, xgboost_model_name, xgboost_outputname):
	x_predict = LoadData(filename)
	if svm_option and svm_model_name != '':
		print("SVM predicting...")
		print("")
		SVM(filename, x_predict, svm_model_name, svm_outputname)
		print("")
		print("SVM predict done!")

	if xgboost_option and xgboost_model_name != '':
		print("XGBoost predicting...")
		print("")
		XGBoost(filename, x_predict, xgboost_model_name, xgboost_outputname)
		print("")
		print("XGBoost predict done!")

Run('../data/set3_with_skeleton.csv', False, 'SVM.joblib.dat', 'SVM_out.csv', True, 'XGB.joblib.dat', 'XGB_out.csv')
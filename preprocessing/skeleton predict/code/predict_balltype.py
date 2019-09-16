import csv
import pandas as pd
import numpy as np
import xgboost as xgb
import itertools
import functions

from sklearn.externals import joblib
from sklearn.metrics import *
from xgboost import plot_importance
import matplotlib.pyplot as plt

def LoadData(filename):
	data = pd.read_csv(filename)
	data = data[needed]
	data.dropna(inplace=True)
	x_predict = data[test_needed]

	return x_predict

def prediction_to_ClipInfo_csv()

def plot_Confusion_Matrix(model_type, cm, groundtruth, grid_predictions, classes):
    plt.imshow(cm, cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.xlabel('Actual Class')
    plt.ylabel('Predicted Class')
    plt.xticks(np.arange(len(classes)-1), classes)
    plt.yticks(np.arange(len(classes)-1), classes)
   
    for j, i in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if i == j:
            plt.text(i+0.03, j+0.2, str(format(cm[j, i], 'd'))+'\n'+str( round(precision_score(groundtruth, grid_predictions, average=None)[i]*100,1))+'%', 
            color="white" if cm[j, i] > cm.max()/2. else "black", 
            horizontalalignment="center")
        else:
            plt.text(i, j, format(cm[j, i], 'd'), 
            color="white" if cm[j, i] > cm.max()/2. else "black", 
            horizontalalignment="center")

    plt.savefig('confusion_matrix_'+str(model_type)+'.png')
    plt.close(0)

def plot_chart(model_type, model, groundtruth, grid_predictions, labels):
    # feature importance
    feature_importance(model)
    # confusion matrix
    plot_Confusion_Matrix(model_type, confusion_matrix(groundtruth, grid_predictions), groundtruth, grid_predictions, labels)
    plt.clf()
    plt.close()

def run(filename_predict, model_path, filename_result):
    label_name_dict = {
        0:"cut",
        1:"drive",
        2:"lob",
        3:"long",
        4:"netplay",
        5:"rush",
        6:"smash",
        7:""
    }
    new_dict = {v : k for k, v in label_name_dict.items()}

    type_labels = pd.DataFrame(label_name_dict, index=[0])
    type_labels = type_labels.values[0]

    xgboost_model = joblib.load(model_path)
    
    # load dataset
    data_predict = np.array([])

    with open(filename_predict, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        c = 0
        for row in reader:
            if c == 0:
                data_predict = np.hstack((data_predict, np.array(row)))
                c = 1
            else:
                data_predict = np.vstack((data_predict, np.array(row)))

    x_predict = data_predict[:,:-1]

    # prediction
    grid_predictions = xgboost_model.predict(x_predict)

    # output
    pd.DataFrame(grid_predictions,columns=['prediction']).to_csv(filename_result,index=None)

    # plot graph
    #result_chart(xgboost_model, data_predict[:, -1], grid_predictions, type_labels, new_dict)

    # print precision and recall
    print("Precision: "+str(precision_score(data_predict[:, -1], grid_predictions, labels = ['cut', 'drive', 'lob', 'long', 'netplay', 'rush', 'smash'], average=None)))
    print("Recall: "+str(recall_score(data_predict[:, -1], grid_predictions, labels = ['cut', 'drive', 'lob', 'long', 'netplay', 'rush', 'smash'], average=None)))

def Run(filename, prediction_result_file, svm_option, svm_model_name, svm_outputname, xgboost_option, xgboost_model_name, xgboost_outputname):
	x_predict, y_predict = LoadData(filename, prediction_result_file)
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

Run('../data/set3_with_skeleton.csv', 'XGB_skeleton_out.csv', False, 'SVM_balltype.joblib.dat', 'SVM_balltype_out.csv', True, 'XGB_balltype.joblib.dat', 'XGB_balltype_out.csv')
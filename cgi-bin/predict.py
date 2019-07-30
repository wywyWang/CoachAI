import csv
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.externals import joblib
import warnings 
import os
warnings.filterwarnings('ignore')

def exec(filename_predict, model_path, filename_result):

    xgboost_model = joblib.load(model_path)
    
    # load dataset
    data_predict = np.array([])

    with open(filename_predict, newline='', encoding='utf8') as f:
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

def verify(pre_dir, filename_predict, model_path, result_dir, filename_result):
    
    # pre_dir: where the files after preprocessing saved
    # filename_predict: the file that we want to predict
    # model_path: the model generated after running the training code
    # result_dir: the directory that store the result
    # filename_result: where the result will be saved

    if os.path.isdir(pre_dir) and os.path.isfile(filename_predict) and os.path.isfile(model_path) and not os.path.isfile(filename_result):
        if not os.path.isdir(result_dir):
            os.mkdir(result_dir)

        print("Start predict...")
        exec(filename_predict, model_path, filename_result)
        print("Prediction done...")
        
    else:
        if not os.path.isfile(model_path):
            print("No such model named: "+str(model_path))
        if not os.path.isdir(pre_dir):
            print("No such directory named: "+str(pre_dir))
        if not os.path.isfile(filename_predict):
            print("No such file: "+str(filename_predict))
        if os.path.isfile(filename_result):
            print("Already exist result file: "+str(filename_result))

import csv
import pandas as pd
import numpy as np
import xgboost as xgb
import warnings 
import os
warnings.filterwarnings('ignore')

pre_dir = "./data/"
model_name = ""
name_predict = ["tai_train"]
name_result_type = ["predict_ball"]
ext = ".csv"

def exec():

    xgboost_model = xgb.Booster().load_model(model_name)
    
    for k in range(len(name_predict)):
        filename_predict = pre_dir + name_predict[k] + ext
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
        pd.DataFrame(grid_predictions,columns=['prediction']).to_csv("./result/"+name_result_type[k]+ext,index=None)

def verify():
    if os.path.exist(pre_dir) and os.path.exist(name_predict) and os.path.exist(model_name):
        exec()
    else:
        if not os.path.exist(model_name):
            print("No such model named: "+str(model_name))
        if not os.path.exist(pre_dir):
            print("No such directory named: "+str(pre_dir))
        if not os.path.exist(name_predict):
            print("No such file named: "+str(name_predict))

verify()
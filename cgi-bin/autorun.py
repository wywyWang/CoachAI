import training
import predict

pre_dir = "./training/data/"
result_dir = "./training/result/"
model_path = "./training/model/0730.joblib.dat"

name_train = "video3_train"
name_predict = "tai_train"
name_result = "0730_test"

ext = ".csv"

filename_train = pre_dir + name_train + ext
filename_predict = pre_dir + name_predict + ext
filename_result = result_dir + name_result + ext

if __name__ == "__main__":
    print("Content-Type: text/plain")    # plain is following
    print()                             # blank line, end of headers
    
    # training and prediction
    training.verify(pre_dir, filename_train, model_path)
    predict.verify(pre_dir, filename_predict, model_path, result_dir, filename_result)
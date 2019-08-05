import auto_segmentation
import raw2train as training_preprocess
import training
import predict

# training and predict input params
pre_dir = "./preprocessing/Data/training/data/"
result_dir = "./preprocessing/Data/training/result/"
model_path = "./preprocessing/Data/training/model/model.joblib.dat"

name_train = "video3_train"
name_predict = "tai_train"
name_result = "model_test"
ext = ".csv"

filename_train = pre_dir + name_train + ext
filename_predict = pre_dir + name_predict + ext
filename_result = result_dir + name_result + ext

# training data preprocessing input params
raw_data = ""

# has players' position info? 1/0 : yes/no
# if yes, player_pos_file (.csv) is needed
player_pos_option = 0
player_pos_file = ""
# training with specific frames? 1/0 : yes/no
# if yes, specific_frame_file (.csv) is needed
frame_option = 0
specific_frame_file = ""

# unique_id for get_velocity function
unique_id = ''

raw_data += ext
training_data_savename = raw_data + "_train" + ext
player_pos_file += ext
specific_frame_file += ext

if __name__ == "__main__":
    print("Content-Type: text/plain")    # plain is following
    print()                             # blank line, end of headers
    
    # Run segmentation
    auto_segmentation.begin()
    
	# training and prediction
	# training_preprocess.run(raw_data, training_data_savename, unique_id, player_pos_option, frame_option)
	# training.verify(pre_dir, filename_train, model_path)
	# predict.verify(pre_dir, filename_predict, model_path, result_dir, filename_result)
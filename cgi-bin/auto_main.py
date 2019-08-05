import auto_segmentation
import raw2train as training_preprocess
import training
import predict

# training data preprocessing input params
pre_dir = "./preprocessing/Data/training/data/"
raw_data = "set1"
ext = ".csv"

# has players' position info? 1/0 : yes/no
# if yes, player_pos_file (.csv) is needed
player_pos_option = 0
player_pos_file = ''
# training with specific frames? 1/0 : yes/no
# if yes, specific_frame_file (.csv) is needed
frame_option = 0
specific_frame_file = ''

# unique_id for get_velocity function
unique_id = ''

preprocessed_filename = pre_dir + raw_data + "_preprocessed" + ext
raw_data = pre_dir + raw_data + ext

if player_pos_option != 0:
	player_pos_file += ext
if frame_option != 0:
	specific_frame_file += ext


# training and predict input params
result_dir = "./preprocessing/Data/training/result/"
model_path = "./preprocessing/Data/training/model/model.joblib.dat"

name_train = "video3_train"
name_result = "0806_predict_result"

filename_train = pre_dir + name_train + ext
filename_result = result_dir + name_result + ext


if __name__ == "__main__":
    print("Content-Type: text/plain")    # plain is following
    print()                             # blank line, end of headers
    
    # Run segmentation
    auto_segmentation.begin()

	# training and prediction
    training_preprocess.run(raw_data, preprocessed_filename, unique_id, player_pos_option, frame_option, player_pos_file, specific_frame_file)
    #training.verify(pre_dir, filename_train, model_path)
    predict.verify(pre_dir, preprocessed_filename, model_path, result_dir, filename_result)
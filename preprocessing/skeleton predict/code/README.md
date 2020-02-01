#Codes for training and prediction

- find_real.py: transform the video coordinate to real world coordinate
	- **YOU MUST CHANGE SOME PARAMETERS FOR DIFFERENT VIDEO**.

- functions.py: some convertion function for preprocessing.

- merge.py: merge set_info and skeleton_info, and generate training features.

- predict.py: laod model from model directory and predict active/passive hitting type.

- predict_balltype.py: laod model from model directory and predict ball type.

- split_clipinfo.py: seperate difference set info to difference files from clip info file.

- training.py: training active/passive hitting type model and save it to model directory.

- training.py: training ball type model and save it to model directory.

- xy_to_area.py: mapping video coordinate to "English+number" area info.
	- *If set_info don't have this feature then you will need this.*
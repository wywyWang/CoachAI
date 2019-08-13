import xy_to_area as convert
from functions import map_reason
import pandas as pd

def convert_hit_area(filename, savename):
	hit_x = []
	hit_y = []
	hit_area = []
	landing_x = []
	landing_y = []
	landing_area = []
	time = []
	getpoint_player = []
	lose_reason = []
	ball_type = []
	frame = []
	output = pd.DataFrame([]) 

	data = pd.read_csv(filename)
	frame = data['Frame']
	time = data['Time']
	hit_x = data['Y']
	hit_y = data['X']
	getpoint_player = data['Getpoint_player']
	
	for reason in data['Lose_reason']:
		lose_reason.append(map_reason(reason))

	hit_area = convert.to_area(hit_x, hit_y)

	output['frame_num'] = frame
	output['time'] = time
	output['hit_area'] = hit_area
	output['hit_x'] = hit_x
	output['hit_y'] = hit_y
	output['landing_area'] = pd.Series(hit_area[1:])
	output['landing_x'] = pd.Series(hit_x.values[1:])
	output['landing_y'] = pd.Series(hit_y.values[1:])
	output['lose_reason'] = pd.Series(lose_reason)
	output['getpoint_player'] = pd.Series(getpoint_player)
	output['type'] = pd.Series(ball_type)


	output.to_csv(savename, index = False, encoding = 'utf-8')

def run(filename, savename):
	convert_hit_area(filename, savename)

#run("record_segmentation.csv", "out.csv")
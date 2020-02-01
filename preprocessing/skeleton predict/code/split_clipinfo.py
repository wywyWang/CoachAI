import pandas as pd

needed_with_id = ['unique_id', 'rally', 'ball_round', 'time', 'frame_num', 'player', 'server', 'type', 'around_head', 'backhand', 
			'hit_area', 'hit_x', 'hit_y', 'hit_height', 'lose_reason', 'win_reason', 'roundscore_A', 'roundscore_B',
			'getpoint_player', 'landing_area', 'landing_x', 'landing_y', 'landing_height']
save = ['rally', 'ball_round', 'time', 'frame_num', 'player', 'server', 'type', 'around_head', 'backhand', 
			'hit_area', 'hit_x', 'hit_y', 'hit_height', 'lose_reason', 'win_reason', 'roundscore_A', 'roundscore_B',
			'getpoint_player', 'landing_area', 'landing_x', 'landing_y', 'landing_height']

needed_without_id = ['rally', 'ball_round', 'time', 'frame_num', 'player', 'server', 'type', 'aroundhead', 'backhand', 
			'hit_area', 'hit_x', 'hit_y', 'hit_height', 'lose_reason', 'win_reason', 'roundscore_A', 'roundscore_B',
			'getpoint_player', 'landing_area', 'landing_x', 'landing_y', 'landing_height']

pre_dir = "../data/"

def load_data(filename):
	data = pd.read_excel(filename)
	data = data[needed_with_id]
	return data

def load_data_with_sheet(filename, sheet):
	data = pd.read_excel(filename, sheet_name=sheet)
	data = data[needed_without_id]
	return data

def split_data_with_unique_id(filename, game_name):
	needed_data = load_data(filename)
	pre_idx = 0
	now_id = needed_data['unique_id'][0]

	for i in range(len(needed_data)):
		if needed_data['unique_id'][i] != now_id:
			set_data = needed_data[pre_idx:i]
			set_data.reset_index(drop=True, inplace=True)
			print("Saving set "+str(now_id))
			set_data.to_csv(pre_dir+game_name+'/'+game_name+"_set"+str(now_id.split("-")[-1])+".csv", index=False, encoding = 'utf-8')
			pre_idx = i
			now_id = needed_data['unique_id'][i]


	set_data = needed_data[pre_idx:len(needed_data)]
	set_data.reset_index(drop=True, inplace=True)
	print("Saving set "+str(now_id))
	set_data.to_csv(pre_dir+game_name+'/'+game_name+"_set"+str(now_id.split("-")[-1])+".csv", index=False, encoding = 'utf-8')

def split_data_with_data_sheet(filename, game_name, sheet_cnt):
	for i in range(sheet_cnt):
		needed_data = load_data_with_sheet(filename, i)
		needed_data.to_csv(pre_dir+game_name+'/'+game_name+"_set"+str(i+1)+".csv", index=False, encoding = 'utf-8')
		print("Saving set "+str(i+1))

def run(filenames):
	for f in filenames:
		#split_data_with_unique_id(pre_dir+f+"/clip_info_"+f+".xlsx", f)
		split_data_with_data_sheet(pre_dir+f+"/clip_info_"+f+".xlsx", f, sheet_cnt)

sheet_cnt = 3
run(["19SIN_CG"])
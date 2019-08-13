import json
import pandas as pd

def export_json(savefile, data):
	with open(savefile, 'w') as outputfile:
		json.dump(json.JSONDecoder().decode(pd.DataFrame(data).to_json(orient='records')), outputfile, separators=(',', ': '), indent = 4)
	
def rally_count(rawfile, predict_file, savefile):
	data = pd.read_csv(rawfile)
	predict_result = pd.read_csv(predict_file)
	needed_data = data[['hit_area', 'getpoint_player', 'lose_reason', 'type']]

	a_score = 0
	b_score = 0
	rally_cnt = 1
	hit_count = 0
	sets = []
	rally = []
	score = []
	stroke = []
	winner = []

	for i in range(len(needed_data['hit_area'])):
		if type(needed_data['getpoint_player'][i]) != float:
			if needed_data['getpoint_player'][i] == "A":
				a_score += 1
			elif needed_data['getpoint_player'][i] == "B":
				b_score += 1

			rally.append(rally_cnt)
			score.append(str(a_score)+":"+str(b_score))
			stroke.append(hit_count)
			winner.append(needed_data['getpoint_player'][i])
			sets.append(1)

			rally_cnt += 1
			hit_count = 0

		hit_count += 1
	    
	lose_detail = needed_data[['hit_area','lose_reason']].dropna().reset_index(drop=True)

	cnt = 0
	balltype = []
	for i in range(len(needed_data['getpoint_player'])):
	    if (needed_data['getpoint_player'][i] == 'A' or needed_data['getpoint_player'][i] == 'B') and cnt in range(len(predict_result['prediction'])):
	        balltype.append(predict_result['prediction'][cnt])
	        cnt += 1

	result_data = pd.DataFrame(columns = ["set", "rally", "score", "stroke", "winner", "on_off_court", "balltype", "lose_area"])
	
	result_data["set"] = sets
	result_data["rally"] = rally
	result_data["score"] = score
	result_data["stroke"] = stroke
	result_data["winner"] = winner
	result_data["on_off_court"] = list(lose_detail['lose_reason'].values)
	result_data["balltype"] = balltype
	result_data["lose_area"] = list(lose_detail['hit_area'].values)

	result_data = (result_data.groupby(['set'], as_index = True)
	            .apply(lambda x: x[['rally','score','stroke','winner','on_off_court','balltype','lose_area']].to_dict('records'))
	            .reset_index()
	            .rename(columns={0:'result'})
	            )

	export_json(savefile, result_data)


def rally_type(rawfile, predict_file, savefile):
	rally_data = pd.read_csv(rawfile)
	result = pd.DataFrame(columns = ["set", "rally", "player", "balltype", "count"])
	ball_id = {'cut': 0, 'drive': 1, 'lob': 2, 'long': 3, 'netplay': 4, 'rush': 5, 'smash': 6}
	ball_cnt = [0]*len(ball_id)
	sets = [1]
	rally_cnt = 1

	result_A = pd.DataFrame(columns = ["set", "rally", "player", "balltype", "count"])
	result_B = result_A

	# not done
	#for hit in range(len(rally_data['hit_area'])):


def run(rawfile, predict_file, rally_count_savefile, rally_type_savefile):
	rally_count(rawfile, predict_file, rally_count_savefile)
	#rally_type(rawfile, predict_file, rally_type_savefile)

run("../../Data/training/data/out.csv", "../../Data/training/result/0811_predict_result.csv", "../../Data/Output/rally_count_our.json", "")
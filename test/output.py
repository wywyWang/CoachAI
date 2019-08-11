import json
import pandas as pd

def export_json(savefile, data):
	data = (data.groupby(['set'], as_index = True)
            .apply(lambda x: x[['rally','score','stroke','winner','on_off_court','balltype','lose_area']].to_dict('records'))
            .reset_index()
            .rename(columns={0:'result'})
            )

	with open(savefile, 'w') as outputfile:
		json.dump(json.JSONDecoder().decode(pd.DataFrame(data).to_json(orient='records')), outputfile, separators=(',', ': '), indent = 4)
	
def exec(rawfile, savefile):
	data = pd.read_csv(rawfile)
	needed_data = data[['hit_area', 'getpoint_player', 'lose_reason', 'type']]

	a_score = 0
	b_score = 0
	rally_count = 1
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

			rally.append(rally_count)
			score.append(str(a_score)+":"+str(b_score))
			stroke.append(hit_count)
			winner.append(needed_data['getpoint_player'][i])
			sets.append(1)

			rally_count += 1
			hit_count = 0

		hit_count += 1
	    
	lose_detail = needed_data[['hit_area','lose_reason']].dropna().reset_index(drop=True)

	lose_ball = needed_data[['type','getpoint_player']]
	balltype = []
	for i in range(len(lose_ball)):
	    if lose_ball['getpoint_player'][i] == 'A' or lose_ball['getpoint_player'][i] == 'B':
	        balltype.append(lose_ball['type'][i-1])

	result_data = pd.DataFrame(columns = ["set", "rally", "score", "stroke", "winner", "on_off_court", "balltype", "lose_area"])
	
	result_data["set"] = sets
	result_data["rally"] = rally
	result_data["score"] = score
	result_data["stroke"] = stroke
	result_data["winner"] = winner
	result_data["on_off_court"] = list(lose_detail['lose_reason'].values)
	result_data["lose_area"] = list(lose_detail['hit_area'].values)

	export_json(savefile, result_data)

def run(rawfile, savefile):
	exec(rawfile, savefile)

run("out.csv", "rally_count_our.json")
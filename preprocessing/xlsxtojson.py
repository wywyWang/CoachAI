import pandas as pd
import json
from collections import Counter

rally = pd.read_excel('../../clip_info_new.xlsx')
rally = rally[['unique_id','rally','ball_round','player','frame_num','server','type','lose_reason']]
rally_drop = rally.drop(["frame_num","server","lose_reason"],axis=1)
# mapping={
#     '挑球':'lob',
#     '放小球':'netplay',
#     '切球':'cut',
#     '長球':'long',
#     '殺球':'smash',
#     '平球':'drive',
#     '未擊球':'unhit',
#     '擋小球':''
# }
# iris["species"]=iris["species"].map(species)
field = rally_drop.groupby(['unique_id','rally'])
filepath = '../statistics/rally_type.json'

def export_json(filepath,data):
    with open(filepath,'a') as outfile:
        json.dump(json.JSONDecoder().decode(data.to_json(orient='records',date_format='iso')),outfile)

result = pd.DataFrame()
for i in list(field.groups.keys()):
    # print(i)
    tmp = pd.Series.to_frame(field.get_group(i).groupby('player')['type'].value_counts())
    # result.assign(tmp)
    print(tmp)
    # print(tmp.index.tolist()[0][1])
    export_json(filepath,tmp)
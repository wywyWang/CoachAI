import pandas as pd
import json
import numpy as np
from collections import Counter
import itertools  as it

rally = pd.read_excel('./clip_info_new.xlsx')
rally = rally[['unique_id','rally','ball_round','player','frame_num','server','type','lose_reason']]
rally_drop = rally.drop(["frame_num","server","lose_reason"],axis=1)
rally_drop = rally_drop[rally_drop['type'] != '未擊球'].reset_index(drop=True)
rally_drop = rally_drop[rally_drop['type'] != '未過網'].reset_index(drop=True)
rally_drop = rally_drop[rally_drop['type'] != '掛網球'].reset_index(drop=True)
totaltype = ["挑球","放小球","切球","長球","殺球","平球","擋小球","回挑","發小球","小平球","撲球","掛網球"]
field = rally_drop.groupby(['unique_id','rally'])
filepath = './rally_type.json'

def export_json(filepath,data):
    with open(filepath,'w') as outfile:
        json.dump(json.JSONDecoder().decode(data.to_json(orient='records',date_format='iso')),outfile,indent = 4,separators=(',', ':'))

#process to rally_type_real.json
result = pd.DataFrame(columns = ["rally","player","balltype","count"])

roundcnt = 1
for i in list(field.groups.keys()):
    resultA = pd.DataFrame(columns = ["rally","player","balltype","count"])
    resultB = pd.DataFrame(columns = ["rally","player","balltype","count"])
    print("========================")
    tmp = pd.Series.to_frame(field.get_group(i).groupby('player')['type'].value_counts())

    # print(tmp['type'].index)
    tmptolist = tmp.index.tolist()
    ballround = []
    player = []
    balltype = []
    ballsum = []
    for j in range(len(tmptolist)):
        ballround += ['1-' + str(roundcnt)]
        player += [tmptolist[j][0]]
        balltype += [tmptolist[j][1]]
        ballsum += [tmp['type'][j]]

    print("player A = ",Counter(player)['A'])
    print("player B = ",Counter(player)['B'])
    brA = ballround[:Counter(player)['A']]
    plA = player[:Counter(player)['A']]
    btA = balltype[:Counter(player)['A']]
    bsA = ballsum[:Counter(player)['A']]
    # 放A因為前半段是A 後半段是B
    brB = ballround[Counter(player)['A']:]
    plB = player[Counter(player)['A']:]
    btB = balltype[Counter(player)['A']:]
    bsB = ballsum[Counter(player)['A']:]

    for item in totaltype:
        if item not in btA:
            brA += ['1-' + str(roundcnt)]
            plA += ['A']
            btA += [item]
            bsA += [0]
        if item not in btB:
            brB += ['1-' + str(roundcnt)]
            plB += ['B']
            btB += [item]
            bsB += [0]

    roundcnt += 1

    resultA['rally'] = brA
    resultA['player'] = plA
    resultA['balltype'] = btA
    resultA['count'] = bsA
    resultA = resultA.sort_values(['balltype'])
    result = result.append(resultA)

    resultA = (resultA.groupby(['rally','player'], as_index=False)
             .apply(lambda x: x[['balltype','count']].to_dict('r'))
             .reset_index()
             .rename(columns={0:'result'})
             )

    resultB['rally'] = brB
    resultB['player'] = plB
    resultB['balltype'] = btB
    resultB['count'] = bsB
    resultB = resultB.sort_values(['balltype'])

    result = result.append(resultB)

result = (result.groupby(['rally','player'], as_index=False)
            .apply(lambda x: x[['balltype','count']].to_dict('r'))
            .reset_index()
            .rename(columns={0:'result'})
            )
print(result)
export_json(filepath,result)

#process to rally_count_real
rally = pd.read_excel('./clip_info_new.xlsx')
rally = rally[['unique_id','rally','ball_round','getpoint_player','lose_reason']]
rally['unique_id'][0].split('-')
for i in range(len(rally['unique_id'])):
    rally['unique_id'][i] = rally['unique_id'][i].split('-')[-2] + '-' + rally['unique_id'][i].split('-')[-1]

field = rally.groupby(['unique_id','rally'])

set = []
rallys = []
hit_number = []
winner = rally['getpoint_player']
winner = winner.dropna().reset_index(drop=True)
result = pd.DataFrame(columns = ["set","rally","stroke","winner","on_off_court","balltype","lose_area"])
for i in range(len(field.groups.keys())):
    setrally = list(field.groups.keys())[i][0].split('-')
    set += [int(setrally[1])]
    rallys +=[list(field.groups.keys())[i][1]]
    hit_number += [len(field.get_group(list(field.groups.keys())[i])['ball_round'].value_counts())]
    
result['set'] = set
result['rally'] = rallys
result['stroke'] = hit_number
result['winner'] = winner

rally2 = pd.read_excel('./clip_info_new.xlsx')
rally2 = rally2[['hit_area','lose_reason']].dropna().reset_index(drop=True)
result['on_off_court'] = rally2['lose_reason']
result['lose_area'] = rally2['hit_area']

rally2 = pd.read_excel('./clip_info_new.xlsx')
rally2 = rally2[['type','getpoint_player']]
balltype = []
for i in range(len(rally)):
    if rally2['getpoint_player'][i] == 'A' or rally2['getpoint_player'][i] == 'B':
        balltype += [rally2['type'][i-1]]
result['balltype'] = balltype
print(result)

result = (result.groupby(['set'], as_index=False)
            .apply(lambda x: x[['rally','stroke','winner','on_off_court','balltype','lose_area']].to_dict('r'))
            .reset_index()
            .rename(columns={0:'result'})
            )

filepath = './rally_count_real.json'
export_json(filepath,result)
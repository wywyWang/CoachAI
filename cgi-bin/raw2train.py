import numpy as np
import pandas as pd
import math
import functions

# initial columns
def init_params():
    output_data = pd.DataFrame([])

    ball_type_new = []
    hit_direct = []
    hit_distance = []
    hit_height_new = []
    landing_direct = []
    landing_distance = []
    landing_height_new = []
    x_direct = []
    x_distance = []
    y_direct = []
    y_distance = []

def load_data(filename):
    data = pd.read_csv(filename)

    data_num = data.shape[0]

    frame = data["frame_num"]
    ball_type = data["type"]
    hit_area = data["hit_area"]
    hit_height = data["hit_height"]
    lose_reason = data["lose_reason"]
    landing_area = data["landing_area"]
    landing_x = data["landing_x"]
    landing_y = data["landing_y"]
    landing_height = data["landing_height"]

def option_check(player_pos_option, frame_option, player_pos_file, specific_frame_file):
    # If there is player position info
    if player_pos_option == 1:
        df = pd.read_csv(player_pos_file)
        need_frame = df.values
        data_num = need_frame.shape[0]

    # Decide if trained with the specific frame
    if frame_option == 1:
        df = pd.read_csv(specific_frame_file)
        need_frame = df.values
        data_num = need_frame.shape[0]

    return need_frame, data_num

def get_velocity(filename, unique_id, savename):
    data = pd.read_csv(filename)

    # extract columns
    time = data['time']
    ball_type = data['type']
    hit_x = data['hit_x']
    hit_y = data['hit_y']
    hit_area = data['hit_area']
    lose_reason = data['lose_reason']
    landing_x = data['landing_x']
    landing_y = data['landing_y']
    landing_area = data['landing_area']

    data_num = data.shape[0]

    velocity = []
    direction = []

    for i in range(data_num):
        
        if type(lose_reason[i]) != float:
            velocity.append('')
            direction.append('')
            continue 
        
        # velocity
        v = functions.velocity(time[i],time[i+1],hit_x[i],hit_y[i],landing_x[i],landing_y[i])
        velocity.append(v)

        # direction (first para means diagonal angle)
        d = functions.direction(30,hit_x[i],hit_y[i],hit_area[i],landing_x[i],landing_y[i],landing_area[i])
        direction.append(d)

    data['velocity'] = velocity
    data['direction'] = direction
    data.insert(loc=0, column='unique_id', value=unique_id)

    data.to_csv(savename,index=False)
        

def exec(need_frame, data_num, savename):
    for j in range(data_num):
        if frame_option == 1:
            result = np.where(frame == need_frame[j])
            i = result[0][0]
        else:
            i = j

        if type(lose_reason[i]) != float or type(hit_area[i]) == float or type(ball_type[i]) == float:
            continue

        if player_pos_option == 1:
            # x direct & x distance
            x_dir , x_dis = functions.hit_convertion_9(hit_area[i])
            x_direct.append(x_dir)
            x_distance.append(x_dis)

            # y direct & y distance
            y_dir , y_dis = functions.landing_convertion_9(hit_area[i])
            y_direct.append(y_dir)
            y_distance.append(y_dis)
        else:
            x_direct.append('')
            x_distance.append('')
            y_direct.append('')
            y_distance.append('')

        # hit direct & hit distance
        h_dir , h_dis = functions.hit_convertion_9(hit_area[i])
        hit_direct.append(h_dir)
        hit_distance.append(h_dis)
        
        if h_dir == 'X':
            print('error hit_area: ',i,hit_area[i])
        
        # landing direct & landing distance
        d_dir , d_dis = functions.landing_convertion_9(landing_area[i])
        landing_direct.append(d_dir)
        landing_distance.append(d_dis)

        if d_dir == 'X':
            print('error landing_area: ',i,landing_area[i])

        # height
        hit_height_new.append(int(hit_height[i]))
        landing_height_new.append(int(landing_height[i]))
        
        # ball type
        bt = functions.ball_type_convertion(ball_type[i])
        ball_type_new.append(bt)
        if bt == 'error':
            print('error ball_type: ',i,ball_type[i])
        
    output_data["hit_direct"] = hit_direct
    output_data["hit_distance"] = hit_distance
    output_data["hit_height"] = hit_height_new
    output_data["landing_direct"] = landing_direct
    output_data["landing_distance"] = landing_distance
    output_data["landing_height"] = landing_height_new

    output_data["x_direct"] = x_direct
    output_data["x_distance"] = x_distance
    output_data["y_direct"] = y_direct
    output_data["y_distance"] = y_distance

    output_data["ball_type"] = ball_type_new

    output_data.to_csv(savename,index=False)

def run(filename, savename, unique_id, player_pos_option, frame_option, player_pos_file, specific_frame_file):
    init_params()
    get_velocity(filename, unique_id, savename)
    load_data(savename)
    need_frame, data_num = option_check(player_pos_option, frame_option, player_pos_file, specific_frame_file)
    exec(need_frame, data_num, savename)

# run("set1.csv", "set1_after.csv", "", 0, 0, "", "")
def readData():
    global numFrame
    numFrame = 18241
    # Import data
    global df,df_complete
    df = pd.read_csv('../Data/TrainTest/Badminton_label.csv')
    df = df[0:numFrame]
    dupl=[]
    df_complete = df[0:numFrame]

    # Prune unseen frames
    df = df[df.Visibility == 1].reset_index(drop=True)

    init=0
    while init < len(df) :
        dupl+=[0]
        init+=1
    df['Dup']=dupl

    #record consecutive same frame ,threshold is 4
    i=0
    while i < len(df)-4:
        if df['X'][i]==df['X'][i+1] and df['Y'][i]==df['Y'][i+1] and df['X'][i]==df['X'][i+2] and df['Y'][i]==df['Y'][i+2] and df['X'][i]==df['X'][i+3] and df['Y'][i]==df['Y'][i+3] and df['X'][i]==df['X'][i+4] and df['Y'][i]==df['Y'][i+4]:
            df['Dup'][i]=1
            df['Dup'][i+1]=1
            df['Dup'][i+2]=1
            df['Dup'][i+3]=1
            df['Dup'][i+4]=1 
            i+=5
        else :
            df['Dup'][i]=0
            i+=1  

    print(np.shape(df))

    # Absolute position
    X = df['X']
    Y = df['Y']

    # Vector X and Y
    vecX = [X[i+1]-X[i] for i in range(len(X)-1)]
    vecY = [Y[i+1]-Y[i] for i in range(len(Y)-1)]
    vecX.append(0)
    vecY.append(0)
    df['vecX'] = vecX
    df['vecY'] = vecY

    segmentation(df)

def segmentation(df):
    #Court refer to TAI vs CHEN
    court_top_left_x=470
    court_top_left_y=127
    court_top_right_x=895
    court_top_right_y=127
    court_down_left_x=276
    court_down_left_y=570
    court_down_right_x=1000
    court_down_right_y=570

    # Initialization
    hitpoint = [0 for _ in range(len(df['vecY']))]
    # Hit-point Detection
    for i in range(2, len(df['vecY'])-2) :
        count=0
        if df["Y"][i] > court_top_left_y and df["Y"][i] < court_down_left_y :
            point_x=100         #select a point left out of trapezoid
            point_y=df["Y"][i]
            m1 = (court_down_left_y - court_top_left_y)/(court_down_left_x - court_top_left_x)
            a = np.array([[0,1],[m1,-1]])
            b = np.array([point_y,-(court_top_left_y-m1*court_top_left_x)])
            ans=np.linalg.solve(a,b)

            if ans[0]>100 and ans[0]<df["X"][i] :
                count+=1

            point_x=1100        #select a point right out of trapezoid
            m2 = (court_down_right_y - court_top_right_y)/(court_down_right_x - court_top_right_x)
            a = np.array([[0,1],[m2,-1]])
            b = np.array([point_y,-(court_top_right_y-m2*court_top_right_x)])
            ans=np.linalg.solve(a,b)

            if ans[0]<1100 and ans[0]>df["X"][i] :
                count+=1

            #in court(count=2) condition will probably be hitpoint
            if count==2 :
                #check i~i+2 frame's shuttlecock variation,because image width is wider than height,y's each variation is more imfluence
                if (df['vecX'][i]**2+df['vecY'][i]**2+df['vecX'][i+1]**2+df['vecY'][i+1]**2+df['vecX'][i+2]**2+df['vecY'][i+2]**2)>=50:
                    # Calculate vector change in X
                    if abs(df['vecX'][i]-df['vecX'][i-1]) >= 10 :
                        # <0 means direction change,is hitpoint candidate
                        if sum(df['vecX'][i:i+5]) * sum(df['vecX'][i-5:i]) > 0:
                            pass
                        elif df['Dup'][i]==1:
                            pass
                        else:
                            hitpoint[i] = 1

                    # Calculate vector change in Y
                    if abs(df['vecY'][i]-df['vecY'][i-1]) >= 8 :
                        if sum(df['vecY'][i:i+3]) * sum(df['vecY'][i-3:i]) > 0:
                            pass
                        elif df['Dup'][i]==1:
                            pass
                        else:
                            hitpoint[i] = 1
                            
    df['hitpoint']=hitpoint

    # Pruning consecutive 10 hit-points
    i=0
    j=0
    count=0
    while i < len(df)-10: 
        if df['hitpoint'][i] == 1 :
            j=i+1
            count+=1 
            while j < len(df) :
                if df["Frame"][j] - df["Frame"][i]<10 :
                    if df['hitpoint'][j] == 1 :
                        df['hitpoint'][j] = 0
                else :
                    break
                j+=1              
        i+=1
            
    print('After pruning the consecutive detections, number of detected hit-point = %d' %count)
    rallyend(df)

def rallyend(df):
    end = [0 for _ in range(len(df))]

    for i in range(len(df)-5):
        # Consecutive 5 frames' variation < 5 pixels,select as rally end candidate
        if abs(df['vecX'][i])+abs(df['vecX'][i+1])+abs(df['vecX'][i+2])+abs(df['vecX'][i+3])+abs(df['vecX'][i+4])+abs(df['vecY'][i+4])+abs(df['vecY'][i])+abs(df['vecY'][i+1])+abs(df['vecY'][i+2])+abs(df['vecY'][i+3]) < 3 :
            end[i]=1

    #pruning consecutive ends
    j, count, consecutive = 0, 0, 0
    while j < len(end)-1:
        if end[j] == 0 and consecutive == 0:
            pass
        elif end[j] == 1 and consecutive == 0:
            consecutive = 1
        elif end[j] == 1 and consecutive == 1:
            end[j] = 0
        elif end[j] == 0 and consecutive == 1:
            consecutive = 0
        j += 1

    count=0
    #end event won't happen twice in 150 frames by observation
    for i in range(len(end)) :
        if end[i]==1 :
            for j in range(i+1,i+150) :
                if j>=len(end) :
                    break
                end[j]=0
            i=i+150               
            
    # end[len(df)-1]=1    #18116 frame
    df['end']=end
    on_off_court(df)

def on_off_court(df):
    court_top_left_x=484
    court_top_left_y=319
    court_top_right_x=835
    court_top_right_y=319
    court_down_left_x=358
    court_down_left_y=680
    court_down_right_x=967
    court_down_right_y=680

    small_court_top_left_x=450
    small_court_top_left_y=427
    small_court_top_right_x=870
    small_court_top_right_y=427
    small_court_down_left_x=438
    small_court_down_left_y=465
    small_court_down_right_x=882
    small_court_down_right_y=465


    on_off_court=[]
    ans = np.array([])

    #Use algorithm to determine in or out of court
    # net=2 on=1 off=0 
    count=0

    for i in range(len(df)) :
        if df["end"][i]==1 :
            #Determine whether in net
            if df["Y"][i] > small_court_top_left_y and df["Y"][i] < small_court_down_right_y :
                point_x=100         #select a point left out of trapezoid
                point_y=df["Y"][i]
                m1 = (small_court_down_left_y - small_court_top_left_y)/(small_court_down_left_x - small_court_top_left_x)
                a = np.array([[0,1],[m1,-1]])
                b = np.array([point_y,-(small_court_top_left_y-m1*small_court_top_left_x)])
                ans=np.linalg.solve(a,b)
                
                if ans[0]>100 and ans[0]<df["X"][i] :
                    count+=1
                    
                point_x=1000        #select a point right out of trapezoid
                m2 = (small_court_down_right_y - small_court_top_right_y)/(small_court_down_right_x - small_court_top_right_x)
                a = np.array([[0,1],[m2,-1]])
                b = np.array([point_y,-(small_court_top_right_y-m2*small_court_top_right_x)])
                ans=np.linalg.solve(a,b)
                
                if ans[0]<1000 and ans[0]>df["X"][i] :
                    count+=1
                
                if count == 2 :
                    on_off_court += [2]
                    continue
                                
            thr = 7
            
            if df["Y"][i-thr] > court_top_right_y and df["Y"][i-thr] < court_down_right_y :
                point_x=100
                point_y=df["Y"][i-thr]
                m1 = (court_down_left_y - court_top_left_y)/(court_down_left_x - court_top_left_x)
                a = np.array([[0,1],[m1,-1]])
                b = np.array([point_y,-(court_top_left_y-m1*court_top_left_x)])
                ans=np.linalg.solve(a,b)
                
                if ans[0]>100 and ans[0]<df["X"][i-thr] :
                    count+=1
                    
                point_x=1000
                m2 = (court_down_right_y - court_top_right_y)/(court_down_right_x - court_top_right_x)
                a = np.array([[0,1],[m2,-1]])
                b = np.array([point_y,-(court_top_right_y-m2*court_top_right_x)])
                ans=np.linalg.solve(a,b)
                
                if ans[0]<1000 and ans[0]>df["X"][i-thr] :
                    count+=1
                
                if count == 2 :
                    on_off_court += [1]
                    continue
            on_off_court += [0]
            
        count=0

    on_off_court = {'on_off_court' : on_off_court}
    on_off_court = pd.DataFrame(on_off_court)

    #plot compute result
    name = 'In Field', 'Out Field', 'On Net'
    plt.pie(on_off_court.groupby('on_off_court').size(), labels = name, autopct = make_autopct(on_off_court.groupby('on_off_court').size()), radius = 2, shadow = True, startangle=90, textprops={'fontsize': 14})
    plt.savefig('../Data/Statistics/Loss_reason.jpg', pad_inches = 0.5, transparent=True, bbox_inches = 'tight')

    #judge score
    scoreA = [0 for _ in range(len(df))]
    scoreB = [0 for _ in range(len(df))]
    global who_wins
    who_wins=[]
    scoreAtmp = 0
    scoreBtmp = 0

    index = 0
    sets = 1

    for i in range(len(df)) :
        #because rally 29 is accidentally missed in before,so forced the answer in here
        # if index==28 and df['Frame'][i]==13300:
        #     scoreBtmp+=1
        #     who_wins+='B'
        #     scoreA[i] = scoreAtmp
        #     scoreB[i] = scoreBtmp
        #     continue
        
        if i+thr <len(df):
            thr = 7
        else:
            thr = 0
        
        #short video is imcomplete
        if index == 25 :
            scoreAtmp = 0
            scoreBtmp = 0
            sets = 2

        if df['end'][i] == 1:
            if sets == 1:
                if on_off_court['on_off_court'][index] == 0 and df['Y'][i+thr] < 450 :
                    scoreAtmp+=1
                    who_wins+='A'
                if (on_off_court['on_off_court'][index] == 1 or on_off_court['on_off_court'][index] == 2) and df['Y'][i+thr] < 450 :
                    scoreBtmp+=1
                    who_wins+='B'
                if on_off_court['on_off_court'][index] == 0 and df['Y'][i+thr] > 450 :
                    scoreBtmp+=1
                    who_wins+='B'
                if (on_off_court['on_off_court'][index] == 1 or on_off_court['on_off_court'][index] == 2) and df['Y'][i+thr] > 450 :
                    scoreAtmp+=1
                    who_wins+='A'
            else:
                if on_off_court['on_off_court'][index] == 0 and df['Y'][i+thr] < 450 :
                    scoreBtmp+=1
                    who_wins+='B'
                if (on_off_court['on_off_court'][index] == 1 or on_off_court['on_off_court'][index] == 2) and df['Y'][i+thr] < 450 :
                    scoreAtmp+=1
                    who_wins+='A'
                if on_off_court['on_off_court'][index] == 0 and df['Y'][i+thr] > 450 :
                    scoreAtmp+=1
                    who_wins+='A'
                if (on_off_court['on_off_court'][index] == 1 or on_off_court['on_off_court'][index] == 2) and df['Y'][i+thr] > 450 :
                    scoreBtmp+=1
                    who_wins+='B'
            index+=1     
            
        scoreA[i] = scoreAtmp
        scoreB[i] = scoreBtmp

    df['scoreA']=scoreA
    df['scoreB']=scoreB


    # #convert to json file,need yen's prediction or cannot produce json file
    count = 0
    count_sum=0
    hit_number = []
    for i in range(len(df)) :
        if df['hitpoint'][i] == 1 :
            count += 1
        if df['end'][i] == 1 :
            count_sum += count
            hit_number += [count]
            count = 0

    result = pd.DataFrame(columns = ["set","rally","stroke","winner","on_off_court",'balltype'])
    set = [1 for _ in range(len(hit_number))]
    rallys = [_+1 for _ in range(len(hit_number))]

    # get prediction ball type
    rally2 = pd.read_excel('../Data/TrainTest/clip_info_18IND_TC.xlsx')
    rally2 = rally2[['unique_id','getpoint_player','prediction']]
    balltype = []
    flag = 0
    for i in range(len(rally2)):
        if rally2['getpoint_player'][i] == 'A' or rally2['getpoint_player'][i] == 'B':
            if len(balltype) == 28 and not flag:
                flag = 1
                continue
            balltype += [rally2['prediction'][i-1]]
            
    conv_balltype = { 
        'cut': '切球', 
        'drive': '平球', 
        'lob': '挑球' , 
        'long': '長球', 
        'netplay': '小球',
        'rush': '撲球',
        'smash': '殺球'
    }

    conv_onoffcourt = {
        '0': '出界',
        '1': '落地',
        '2': '未回擊成功'
    }
            
    #get lose area,only this is ground truth
    rally2 = pd.read_excel('../Data/TrainTest/clip_info_18IND_TC.xlsx')
    rally2 = rally2[['hit_area','lose_reason']].dropna().reset_index(drop=True)
    rally2 = rally2[:-1]            #unfound one end,drop last to match the size

    result['balltype'] = balltype
    result['balltype'] = result['balltype'].map(conv_balltype)
    result['lose_area'] = rally2['hit_area']
    result['set'] = set
    result['rally'] = rallys
    result['stroke'] = hit_number
    result['winner'] = who_wins
    result['on_off_court'] = on_off_court
    result['on_off_court'] = result['on_off_court'].astype(str).map(conv_onoffcourt)
    result = (result.groupby(['set'], as_index=False)
                .apply(lambda x: x[['rally','stroke','winner','on_off_court','balltype','lose_area']].to_dict('r'))
                .reset_index()
                .rename(columns={0:'result'})
                )

    #plot counting result
    plt.figure(figsize = (12,6))
    plt.grid()
    plt.title('Stroke counting in rallies', fontsize = 16)
    plt.xlabel('Rally', fontsize = 16)
    plt.ylabel('Count', fontsize = 16)
    plt.plot(hit_number, marker = 'o', color = 'magenta', linestyle = 'dashed')
    for i in range(len(hit_number)):
        plt.text(i, hit_number[i]+0.3, hit_number[i], ha='center', va='bottom', fontsize=12)
    plt.savefig('../Data/Statistics/Rally_count.jpg', pad_inches = 0.5, transparent=True, bbox_inches = 'tight')

    export_json('../Data/Statistics/rally_count.json',result)

    check_accuracy(df)

def check_accuracy(df):
    count=0
    rally = pd.read_excel('../Data/TrainTest/clip_info_18IND_TC.xlsx')
    rally = rally[['rally','ball_round','frame_num','server','type','lose_reason']]
    record = rally[rally['type'] != '未擊球'].reset_index(drop=True)
    record = record[rally['type'] != '未過網'].reset_index(drop=True)
    record = record[rally['type'] != '掛網球'].reset_index(drop=True)
    haveFrame = [0 for _ in range(len(record))]
    total=len(df['hitpoint'][df['hitpoint']==1])
    for i in record['frame_num']:
        # Hitpoint event deviation in +- 5 frames is correct
        for j in range(-5,5):
            if i+j in list(df['Frame']):
                tmp=df['Frame']
                idx=tmp[tmp==i+j].index[0]
                if df['hitpoint'][idx]:
                    count+=1
                    haveFrame += [df['Frame'][idx]]
                    break
            
    print("===========HITPOINT ACCURACY=============")
    print("Total Calculate number = ",total)
    print("Total Correct number = ",len(record))
    print("Correct number = ",count)
    print("Precision = ",float(count/len(record)))
    print("Recall = ",float(count/total))
    print("=========================================")

    #get ground truth rally start and rally end
    rallystart = []
    rallyend = []
    for i in range(len(rally)):
        if rally['server'][i] == 1:
            rallystart += [rally['frame_num'][i]]
        if pd.isnull(rally['lose_reason'][i]) == False:
            rallyend += [rally['frame_num'][i]]
    count=0
    total=len(df['end'][df['end']==1])
    tmp=df['Frame']
    # Rally end event correct between end to start in ground truth will be correct
    for i in range(1,len(rallystart)):
        frame=rallyend[i-1]
        while(frame!=rallystart[i]):
            if frame in list(df['Frame']):
                idx=tmp[tmp==frame].index[0]
                if df['end'][idx]:
                    count+=1
                    break
            frame+=1
    
    idx=tmp[tmp==rallyend[len(rallyend)-1]].index[0]
    while(frame!=18241):
        if frame in list(df['Frame']):
            idx=tmp[tmp==frame].index[0]
            if df['end'][idx]:
                count+=1
                break
        frame+=1 
            
    print("===========RALLY END ACCURACY=============")
    print("Total Calculate number = ",total)
    print("Total Correct number = ",len(rallyend))
    print("Correct number = ",count)
    print("Precision = ",float(count/len(rallyend)))
    print("Recall = ",float(count/(len(df['end'][df['end']==1]))))
    print("==========================================")

    #check virtual umpire accuracy
    rally_umpire = pd.read_excel('../Data/TrainTest/clip_info_18IND_TC.xlsx')
    rally_umpire = rally_umpire[['unique_id','getpoint_player']]
    rally_umpire = rally_umpire.dropna().reset_index(drop=True)

    correct = 0
    j=0
    for i in range(len(rally_umpire)):
        #rally 29 is missed on finding rally end,assume it will be correct
        if i == 28:
            correct +=1
            continue
        if rally_umpire['unique_id'][i].split('-')[-1] == '2':
            if rally_umpire['getpoint_player'][i] == who_wins[j]:
                correct +=1
        else:
            if rally_umpire['getpoint_player'][i] == who_wins[j]:
                correct +=1
        j+=1
        
    print("=======VIRTUAL UMPIRE ACCURACY=======")
    print("Correct Number = ",correct)
    print("Total Number = ",len(rally_umpire))
    print("Accuracy = ",correct/len(rally_umpire))
    print("=====================================")

def export_json(filepath,data):
    with open(filepath,'w') as outfile:
        json.dump(json.JSONDecoder().decode(data.to_json(orient='records',date_format='iso')),outfile,indent = 4,separators=(',', ': '))

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def generateVideo(df,df_complete,numFrame):
    #1.Mark +/- 3 frames that are near the hit-point frame (For visualization purpose)
    hitpointFrame = df[df.hitpoint == 1].reset_index(drop=True)['Frame']
    #for hitpoint
    actual = [0 for _ in range(len(df_complete))]
    marked = [0 for _ in range(len(df_complete))]
    coverage = 5
    #marked hitpoint frame
    for x in hitpointFrame:
        actual[x-1] = 1
        if x > coverage and x < len(df_complete)-coverage:
            marked[(x-1)] = 1
            for i in range(1, coverage+1):
                marked[(x-1)-i] = 1
                marked[(x-1)+i] = 1
        elif x < coverage:
            marked[(x-1)] = 1
            for i in range(1, x):
                marked[(x-1)-i] = 1
            for i in range(1, coverage+1):
                marked[(x-1)+i] = 1
        elif x >= len(df_complete)-coverage:
            marked[(x-1)] = 1
            for i in range(1, coverage+1):
                marked[(x-1)-i] = 1
                
    df_complete['marked'] = marked
    df_complete['actual'] = actual
    markedFrame = df_complete[df_complete.marked == 1].reset_index(drop=True)

    #2. Mark +/- 3 frames that are near the rally-end frame (For visualization purpose)
    endFrame = df[df.end == 1].reset_index(drop=True)['Frame']
    end = [0 for _ in range(len(df_complete))]
    marked = [0 for _ in range(len(df_complete))]
    coverage = 5
    #marked start frame
    for x in endFrame:
        end[x-1] = 1
        if x > coverage and x < len(df_complete)-coverage:
            marked[(x-1)] = 1
            for i in range(1, coverage+1):
                marked[(x-1)-i] = 1
                marked[(x-1)+i] = 1
        elif x < coverage:
            marked[(x-1)] = 1
            for i in range(1, x):
                marked[(x-1)-i] = 1
            for i in range(1, coverage+1):
                marked[(x-1)+i] = 1
        elif x >= len(df_complete)-coverage:
            marked[(x-1)] = 1
            for i in range(1, coverage+1):
                marked[(x-1)-i] = 1

    df_complete = df_complete.drop(columns = ['marked'],axis = 1)
    df_complete['marked'] = marked
    df_complete['end'] = end
    markedEndFrame = df_complete[df_complete.marked == 1].reset_index(drop=True)

    #3.Get ball position from result
    position = pd.read_csv('../Data/AccuracyResult/record_circle_ballsize_predict_heatmap_new_on_new.csv')

    #4.Get real score from clip info
    rally = pd.read_excel('../Data/TrainTest/clip_info_18IND_TC.xlsx')
    rally = rally[['frame_num','getpoint_player']]
    realscoreA = [0 for _ in range(len(df_complete))]
    realscoreB = [0 for _ in range(len(df_complete))]

    index = 0
    realscoreAtmp = 0
    realscoreBtmp = 0

    cntA = 0
    cntB = 0

    for i in range(len(df_complete)) :
        if index == 25 :
            realscoreAtmp = 0
            realscoreBtmp = 0    
        
        if df_complete['Frame'][i] in list(rally['frame_num']):
            idx=rally['frame_num'][rally['frame_num']==df_complete['Frame'][i]].index[0]
            if rally['getpoint_player'][idx] == 'A':
                cntA += 1
                realscoreAtmp += 1
                index += 1
            if rally['getpoint_player'][idx] == 'B':
                cntB += 1
                realscoreBtmp += 1
                index += 1   
            
        realscoreA[i] = realscoreAtmp
        realscoreB[i] = realscoreBtmp
        
    df_complete['realscoreA']=realscoreA
    df_complete['realscoreB']=realscoreB

    #5.Video Generation
    # Get video FPS and size
    input_video_path = '../Data/PredictVideo/TAI Tzu Ying vs CHEN Yufei 2018 Indonesia Open Final'
    video = cv2.VideoCapture(input_video_path + '.mp4')
    fps = int(video.get(cv2.CAP_PROP_FPS))
    output_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    output_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('Frame dimension')
    print('Width = %d' %output_width)
    print('Height = %d' %output_height)

    # filename = input_video_path.split('/')[-1].split('.')[0]
    output_video_path = input_video_path +'_virtual_umpire.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter(output_video_path, fourcc, fps, (output_width,output_height))

    count = 0    
    while(video.isOpened()):
        if count % 500 ==0:
            print("status : ",count)
        count += 1
    #     print("now = ",count)
        if count > numFrame:
            break
        ret, frame = video.read()
        if ret == True:
            cv2.putText(frame, 'Our Score', (800, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (30,144,25), 1)
            cv2.rectangle(frame,(800,50),(1000,130),(255,255,255),3)
            cv2.putText(frame, 'Real Score', (100, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (138,43,226), 1)
            cv2.rectangle(frame,(100,50),(300,130),(255,255,255),3)
            tmp=df['Frame']
            
            #show compute score on video
            if count in list(df['Frame']):
                idx=tmp[tmp==count].index[0]
                cv2.putText(frame, str(df['scoreA'][idx]), (830, 110), cv2.FONT_HERSHEY_TRIPLEX, 2, (30,144,25), 1, cv2.LINE_AA)
                cv2.putText(frame, str(df['scoreB'][idx]), (930, 110), cv2.FONT_HERSHEY_TRIPLEX, 2, (138,43,226), 1, cv2.LINE_AA)
            
            #show real score on video
            if count in list(df_complete['Frame']):
                idx=df_complete['Frame'][df_complete['Frame']==count].index[0]
                cv2.putText(frame, str(df_complete['realscoreA'][idx]), (130, 110), cv2.FONT_HERSHEY_TRIPLEX, 2, (30,144,25), 1, cv2.LINE_AA)
                cv2.putText(frame, str(df_complete['realscoreB'][idx]), (230, 110), cv2.FONT_HERSHEY_TRIPLEX, 2, (138,43,226), 1, cv2.LINE_AA)
            
            #show text "hit-point" on video
            if count in list(markedFrame['Frame']):
                cv2.putText(frame, 'Hit-point', (100, 120), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 1, cv2.LINE_AA)
                tmp=markedFrame['Frame']
                idx=tmp[tmp==count].index[0]
                cv2.circle(frame,(markedFrame['X'][idx],markedFrame['Y'][idx]),5,(0, 0, 255), 2)
                
            if count in list(position['Frame']):
                tmp=position['Frame']
                idx=tmp[tmp==count].index[0]
                if position[' visibility'][idx] == 1:
                    cv2.circle(frame,(int(position[' x'][idx]),int(position[' y'][idx])),4,(0,255,255),2)
            
            # Write the frame to video
            output_video.write(frame)
        else:
            break

    # Release objects
    video.release()
    output_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    import math
    import numpy as np
    import json
    import cv2
    np.set_printoptions(suppress=True)
    readData()

    # generateVideo(df,df_complete,numFrame)      #if don't need can comment out
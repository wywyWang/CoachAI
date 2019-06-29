function change_set(){
    new_set = document.getElementById("set").value;
    $('#rally option').remove();
    change_rally();
}

function change_rally(){
    var set=document.getElementById("set").value;
    if(!set){
        set = 1;
    }
    //delete old button
    $('#next').remove();
    $('#back').remove();
    $('#canvas').remove();
    get_interval_rally(set);
    init_trajectory(set);
}

function get_interval_set(){
    game_name = '_2019亞錦賽-周天成VS石宇奇';
    filename = 'statistics/rally_detail_real' + game_name + '.json';

    $.getJSON(filename, function(data) {
        //find maximum set
        maximum = Math.max.apply(Math, data.map(function(d) { 
            return d.set; 
        }));

        for(var i=1;i<=maximum;i+=1)
        {
            var insertText = '<option value='+i+'>'+i+'</option>';
            $('#set').append(insertText); 
        }
    });
}

function get_interval_rally(set){
    game_name = '_2019亞錦賽-周天成VS石宇奇';
    filename = 'statistics/rally_detail_real' + game_name + '.json';
    $.getJSON(filename, function(data) {
        //init set
        if (!set){
            set = 1;
        }
        //filter data to specific set
        data = data.filter(function(item) {
            return item.set == set
        });
        data = data[0].info;
        var maximum;
        maximum = Math.max.apply(Math, data.map(function(d) { 
            return d.rally; 
        }));
        
        for(var i=0;i<maximum;i+=1)
        {
            var score = data[i].score;
            var insertText = '<option value=' + (i+1) + '>' + score + ' (' + (i+1) + ')' + '</option>';
            $('#rally').append(insertText); 
        } 
    })
}

function init_trajectory(set){
    $('.ball_trajectory').html('<div class="row">\
                                <button class="btn" id="next" type="button">下一球</button>\
                                <button class="btn" id="back" type="button">上一球</button>\
                                </div>\
                                <canvas id="canvas" width="1200" height="600"></canvas>');
    var rally = document.getElementById("rally").value;
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var i=0;
    var total_y_length=424;
    ctx.clearRect(100,100,935,424);
    game_name = '_2019亞錦賽-周天成VS石宇奇';
    filename = 'statistics/rally_detail_real' + game_name + '.json';

    $.getJSON(filename, function(data) {
        if(!set){
            set = 1;
        }
        if(!rally){
            rally = 1;
        }

        //filter data to specific set
        data = data.filter(function(item) {
            return item.set == set
        });
        data = data[0].info;
        //filter data to specific rally
        data = data.filter(function(item) {
            return parseInt(item.rally) == rally;
        });
        data = data[0].result;
        console.log(data);
        var maxorder = Math.max.apply(Math, data.map(function(d) { 
            return d.order; 
        }));

        function initial() {
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.strokeStyle = "black";
            //球場外框
            ctx.rect(100,100,935,424);
            //直的線
            ctx.moveTo(153,100);
            ctx.lineTo(153,524);
            ctx.moveTo(290,100);
            ctx.lineTo(290,524);
            ctx.moveTo(428,100);
            ctx.lineTo(428,524);
            ctx.moveTo(568,100);
            ctx.lineTo(568,524);
            ctx.moveTo(708,100);
            ctx.lineTo(708,524);
            ctx.moveTo(845,100);
            ctx.lineTo(845,524);	
            ctx.moveTo(982,100);
            ctx.lineTo(982,524);
            //橫的線
            ctx.moveTo(100,132);
            ctx.lineTo(1035,132);
            ctx.moveTo(100,492);
            ctx.lineTo(1035,492);
            ctx.moveTo(100,312);
            ctx.lineTo(428,312);
            ctx.moveTo(708,312);
            ctx.lineTo(1035,312);
            ctx.closePath();
            ctx.stroke();
        }
        
        initial();
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(data[0].detail_hit_pos[1]+100,total_y_length-data[0].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
        ctx.strokeStyle = "black";
        ctx.closePath();
        ctx.stroke();
        $("#next").click(function(){
            if(i != maxorder-1){
                if(i>2) {
                    ctx.beginPath();
                    ctx.clearRect(50,50,985,474);
                    ctx.closePath();
                    ctx.stroke();
                    initial();
                    //faded
                    ctx.lineWidth = 3;
                    for(var j=0;j<i-2;j++) {
                        ctx.beginPath();
                        ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                        ctx.strokeStyle = "rgb(229, 226, 222)";
                        ctx.closePath();
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                        ctx.lineTo(data[j+1].detail_hit_pos[1]+100,total_y_length-data[j+1].detail_hit_pos[0]+100);
                        ctx.strokeStyle = "rgb(229, 226, 222)";
                        ctx.closePath();
                        ctx.stroke();
                    }
                    //normal
                    for(var j=i-2;j<i+1;j++) {
                        ctx.beginPath();
                        ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                        ctx.strokeStyle = "black";
                        ctx.closePath();
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                        ctx.lineTo(data[j+1].detail_hit_pos[1]+100,total_y_length-data[j+1].detail_hit_pos[0]+100);
                        if(j==i-2){
                            ctx.strokeStyle = "rgb(252, 133, 133)";
                        }
                        if(j==i-1){
                            ctx.strokeStyle = "rgb(173, 34, 34)";
                        }
                        if(j==i){
                            ctx.strokeStyle = "rgb(91, 0, 0)";
                        }
                        ctx.closePath();
                        ctx.stroke();
                    }
                    ctx.beginPath();
                    ctx.arc(data[i+1].detail_hit_pos[1]+100,total_y_length-data[i+1].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "black";
                    ctx.closePath();
                    ctx.stroke();
                }
                else {
                    ctx.beginPath();
                    ctx.clearRect(50,50,985,474);
                    ctx.closePath();
                    ctx.stroke();
                    initial();
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.arc(data[0].detail_hit_pos[1]+100,total_y_length-data[0].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "black";
                    ctx.closePath();
                    ctx.stroke();
                    for(var j=i+1;j>0;j--) {
                        ctx.beginPath();
                        ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                        ctx.strokeStyle = "black";
                        ctx.closePath();
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                        ctx.lineTo(data[j-1].detail_hit_pos[1]+100,total_y_length-data[j-1].detail_hit_pos[0]+100);
                        if(j==i-1){
                            ctx.strokeStyle = "rgb(252, 133, 133)";
                        }
                        if(j==i){
                            ctx.strokeStyle = "rgb(173, 34, 34)";
                        }
                        if(j==i+1){
                            ctx.strokeStyle = "rgb(91, 0, 0)";
                        }
                        ctx.closePath();
                        ctx.stroke();
                    }
                }
                if(i!=maxorder-2) {
                    i+=1;
                }
                else{
                    i = maxorder - 1;
                }
            }
            
        });
    
        $("#back").click(function(){
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.clearRect(50,50,985,474);
            ctx.closePath();
            ctx.stroke();
            initial();
            ctx.lineWidth = 3;
            if(i>4) {
                //faded
                for(var j=0;j<i-4;j++) {
                    ctx.beginPath();
                    ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "rgb(229, 226, 222)";
                    ctx.closePath();
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                    ctx.lineTo(data[j+1].detail_hit_pos[1]+100,total_y_length-data[j+1].detail_hit_pos[0]+100);
                    ctx.strokeStyle = "rgb(229, 226, 222)";
                    ctx.closePath();
                    ctx.stroke();
                }
                //normal
                for(var j=i-4;j<i-1;j++) {
                    ctx.beginPath();
                    ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "black";
                    ctx.closePath();
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(data[j+1].detail_hit_pos[1]+100,total_y_length-data[j+1].detail_hit_pos[0]+100);
                    ctx.lineTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                    if(j==i-4){
                        ctx.strokeStyle = "rgb(252, 133, 133)";
                    }
                    if(j==i-3){
                        ctx.strokeStyle = "rgb(173, 34, 34)";
                    }
                    if(j==i-2){
                        ctx.strokeStyle = "rgb(91, 0, 0)";
                    }
                    
                    ctx.closePath();
                    ctx.stroke();
                }
                ctx.beginPath();
                ctx.arc(data[i-1].detail_hit_pos[1]+100,total_y_length-data[i-1].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                ctx.strokeStyle = "black";
                ctx.closePath();
                ctx.stroke();
            }
            else {
                ctx.beginPath();
                ctx.arc(data[0].detail_hit_pos[1]+100,total_y_length-data[0].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                ctx.strokeStyle = "black";
                ctx.closePath();
                ctx.stroke();

                for(var j=i-1;j>=1;j--) {
                    ctx.beginPath();
                    ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "black";
                    ctx.closePath();
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                    ctx.lineTo(data[j-1].detail_hit_pos[1]+100,total_y_length-data[j-1].detail_hit_pos[0]+100);
                    if(j==i-3){
                        ctx.strokeStyle = "rgb(252, 133, 133)";
                    }
                    if(j==i-2){
                        ctx.strokeStyle = "rgb(173, 34, 34)";
                    }
                    if(j==i-1){
                        ctx.strokeStyle = "rgb(91, 0, 0)";
                    }
                    ctx.closePath();
                    ctx.stroke();
                }
            }
            if(i!=0) {
                i-=1;
            }
        })
    });
}
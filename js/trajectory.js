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
    //delete old canvas
    $('#canvas').remove();
    $('#balltype_table').remove();
    $('.btn').remove();

    get_interval_rally(set);
    init_trajectory(set);
}

function get_interval_set(){
    game_name = '_CS';
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
    var insertText = '<button id="interval-submit" type="button" class="btn btn-primary" onclick=change_rally()>查詢</button>';
    $('#dropdown').append(insertText); 
    var insertText = '<button class="btn btn-default" id="next" type="button">下一球</button>';
    $('#dropdown').append(insertText); 
    var insertText = '<button class="btn btn-default" id="back" type="button">上一球</button>';
    $('#dropdown').append(insertText); 

    game_name = '_CS';
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
    $('.ball_trajectory').html('<canvas id="canvas" width="1200" height="600"></canvas>');
    var rally = document.getElementById("rally").value;
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var current = 0;
    var currentTableIdx = 0;
    var total_y_length = 424;
    ctx.clearRect(100,100,935,424);
    game_name = '_CS';
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

        //balltype table initial
        $('#balltype_table').remove();
        var insertText = '<table class="table" id="balltype_table"><thead><tr><th>Balltpye</th></tr></thead><tbody class="tbody_detail"></tbody></table>';
        $('.ball_trajectory').append(insertText); 

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

        function CheckSmash(point){
            if(point.detail_type == '殺球'){
                return true;
            }
            return false;
        }
        
        initial();
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(data[0].detail_hit_pos[1]+100,total_y_length-data[0].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
        ctx.strokeStyle = "black";
        ctx.closePath();
        ctx.stroke();
        $("#next").click(function(){    
            //add next balltype to table
            if(currentTableIdx != maxorder-1){
                var insertText;
                if(CheckSmash(data[currentTableIdx])){
                    insertText = '<tr class="danger"><td><b>' + data[currentTableIdx].detail_type + '</b></td></tr>';
                }
                else{
                    insertText = '<tr><td>' + data[currentTableIdx].detail_type + '</td></tr>';
                }
                $('.tbody_detail').append(insertText); 
                currentTableIdx += 1;
            }

            if(current != maxorder-1){
                if(current>2) {
                    ctx.beginPath();
                    ctx.clearRect(50,50,1000,600);
                    ctx.closePath();
                    ctx.stroke();
                    initial();
                    //faded
                    ctx.lineWidth = 3;
                    for(var j=0;j<current-2;j++) {
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
                    for(var j=current-2;j<current+1;j++) {
                        ctx.beginPath();
                        ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                        ctx.strokeStyle = "black";
                        ctx.closePath();
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                        ctx.lineTo(data[j+1].detail_hit_pos[1]+100,total_y_length-data[j+1].detail_hit_pos[0]+100);
                        if(j==current-2){
                            if(CheckSmash(data[j])){
                                ctx.strokeStyle = "rgb(66, 245, 147)";
                            }
                            else{
                                ctx.strokeStyle = "rgb(252, 133, 133)";
                            }
                        }
                        if(j==current-1){
                            if(CheckSmash(data[j])){
                                ctx.strokeStyle = "rgb(66, 245, 147)";
                            }
                            else{
                                ctx.strokeStyle = "rgb(173, 34, 34)";
                            }
                        }
                        if(j==current){
                            if(CheckSmash(data[j])){
                                ctx.strokeStyle = "rgb(66, 245, 147)";
                            }
                            else{
                                ctx.strokeStyle = "rgb(91, 0, 0)";
                            }
                        }
                        ctx.closePath();
                        ctx.stroke();
                    }
                    ctx.beginPath();
                    ctx.arc(data[current+1].detail_hit_pos[1]+100,total_y_length-data[current+1].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "black";
                    ctx.closePath();
                    ctx.stroke();
                }
                else {
                    ctx.beginPath();
                    ctx.clearRect(50,50,1000,600);
                    ctx.closePath();
                    ctx.stroke();
                    initial();
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.arc(data[0].detail_hit_pos[1]+100,total_y_length-data[0].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "black";
                    ctx.closePath();
                    ctx.stroke();
                    for(var j=current+1;j>0;j--) {
                        ctx.beginPath();
                        ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                        ctx.strokeStyle = "black";
                        ctx.closePath();
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                        ctx.lineTo(data[j-1].detail_hit_pos[1]+100,total_y_length-data[j-1].detail_hit_pos[0]+100);
                        if(j==current-1){
                            if(CheckSmash(data[j])){
                                ctx.strokeStyle = "rgb(66, 245, 147)";
                            }
                            else{
                                ctx.strokeStyle = "rgb(252, 133, 133)";
                            }
                        }
                        if(j==current){
                            if(CheckSmash(data[j])){
                                ctx.strokeStyle = "rgb(66, 245, 147)";
                            }
                            else{
                                ctx.strokeStyle = "rgb(173, 34, 34)";
                            }
                        }
                        if(j==current+1){
                            if(CheckSmash(data[j])){
                                ctx.strokeStyle = "rgb(66, 245, 147)";
                            }
                            else{
                                ctx.strokeStyle = "rgb(91, 0, 0)";
                            }
                        }
                        ctx.closePath();
                        ctx.stroke();
                    }
                }
                if(current!=maxorder-2) {
                    current+=1;
                }
                else{
                    current = maxorder - 1;
                }
            }
            
        });
    
        $("#back").click(function(){
            //delete last table row
            var table = document.getElementById('balltype_table');
            var rowCount = table.rows.length;
            if(currentTableIdx > 0){
                table.deleteRow(-1);
                currentTableIdx -= 1;
            }

            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.clearRect(50,50,1000,600);
            ctx.closePath();
            ctx.stroke();
            initial();
            ctx.lineWidth = 3;
            if(current>4) {
                //faded
                for(var j=0;j<current-4;j++) {
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
                for(var j=current-4;j<current-1;j++) {
                    ctx.beginPath();
                    ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "black";
                    ctx.closePath();
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(data[j+1].detail_hit_pos[1]+100,total_y_length-data[j+1].detail_hit_pos[0]+100);
                    ctx.lineTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                    if(j==current-4){
                        if(CheckSmash(data[j])){
                            ctx.strokeStyle = "rgb(66, 245, 147)";
                        }
                        else{
                            ctx.strokeStyle = "rgb(252, 133, 133)";
                        }
                    }
                    if(j==current-3){
                        if(CheckSmash(data[j])){
                            ctx.strokeStyle = "rgb(66, 245, 147)";
                        }
                        else{
                            ctx.strokeStyle = "rgb(173, 34, 34)";
                        }
                    }
                    if(j==current-2){
                        if(CheckSmash(data[j])){
                            ctx.strokeStyle = "rgb(66, 245, 147)";
                        }
                        else{
                            ctx.strokeStyle = "rgb(91, 0, 0)";
                        }
                    }
                    
                    ctx.closePath();
                    ctx.stroke();
                }
                ctx.beginPath();
                ctx.arc(data[current-1].detail_hit_pos[1]+100,total_y_length-data[current-1].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
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

                for(var j=current-1;j>=1;j--) {
                    ctx.beginPath();
                    ctx.arc(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100,5,0,Math.PI*2,true);
                    ctx.strokeStyle = "black";
                    ctx.closePath();
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(data[j].detail_hit_pos[1]+100,total_y_length-data[j].detail_hit_pos[0]+100);
                    ctx.lineTo(data[j-1].detail_hit_pos[1]+100,total_y_length-data[j-1].detail_hit_pos[0]+100);
                    if(j==current-3){
                        if(CheckSmash(data[j])){
                            ctx.strokeStyle = "rgb(66, 245, 147)";
                        }
                        else{
                            ctx.strokeStyle = "rgb(252, 133, 133)";
                        }
                    }
                    if(j==current-2){
                        if(CheckSmash(data[j])){
                            ctx.strokeStyle = "rgb(66, 245, 147)";
                        }
                        else{
                            ctx.strokeStyle = "rgb(173, 34, 34)";
                        }
                    }
                    if(j==current-1){
                        if(CheckSmash(data[j])){
                            ctx.strokeStyle = "rgb(66, 245, 147)";
                        }
                        else{
                            ctx.strokeStyle = "rgb(91, 0, 0)";
                        }
                    }
                    ctx.closePath();
                    ctx.stroke();
                }
            }
            if(current!=0) {
                current-=1;
            }
        })
    });
}
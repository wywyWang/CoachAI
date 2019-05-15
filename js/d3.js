var set = 1;
function init_linechart(minrally,maxrally){
    $.getJSON("statistics/rally_count_real.json", function(data) {
        //filter data to specific set
        data = data.filter(function(item) {
            return item.set == set
        });
        data = data[0].result

        // init minrally and maxrally if are undefined,null,0,NaN,empty string,false
        if (!minrally){
            minrally = Math.min.apply(Math, data.map(function(d) { 
                return d.rally;
            }));
        }

        if (!maxrally){
            maxrally = Math.max.apply(Math, data.map(function(d) { 
                return d.rally
            }));
        }
        console.log(minrally)
        console.log(maxrally)

        var canv = document.createElement('canvas');
        canv.id = 'line_chart';
        canv.width = 800;
        canv.height = 600;
        document.getElementById("line").appendChild(canv);

        var chartRadarDOM;
        var chartRadarData;
        var chartRadarOptions;

        chartRadarDOM = document.getElementById("line_chart");
        //custormized options
        chartRadarOptions = 
        {
            legend:{
                display: false
            },
            scales:{
                xAxes: [{
                    scaleLabel:{
                        display: true,
                        labelString: '回合',
                        fontSize: 16
                    }
                }],
                yAxes: [{
                    ticks:{
                        beginAtZero: true,
                    },
                    scaleLabel:{
                        display: true,
                        labelString: '拍數',
                        fontSize: 16
                    }
                }]
            },
            elements: {
                line: {
                    tension: 0 // disables bezier curves
                }
            }
        };

        var labels = data.map(function(e) {
            return e.rally;
        });

        var datas = data.map(function(e) {
            return e.stroke;
        });

        var pointcolor = [];
        var datadown = [];
        var datainterval = [];
        var dataup = [];
        for (var i = 0;i<data.length;i++){
            // console.log(data[i])
            if (data[i].rally < minrally){
                datadown.push(data[i].stroke);
                datainterval.push(null);
                dataup.push(null);
            }
            else if (data[i].rally > maxrally){
                datadown.push(null);
                datainterval.push(null);
                dataup.push(data[i].stroke);
            }
            else{
                if (data[i].rally == minrally){
                    datadown.push(data[i].stroke);
                    datainterval.push(data[i].stroke);
                    dataup.push(null);
                }
                else if (data[i].rally == maxrally){
                    datadown.push(null);
                    datainterval.push(data[i].stroke);
                    dataup.push(data[i].stroke);
                }
                else{
                    datadown.push(null);
                    datainterval.push(data[i].stroke);
                    dataup.push(null);
                }
                
            }
                
            if (data[i].rally < minrally || data[i].rally > maxrally)
                pointcolor.push("rgb(216, 212, 212)");
            else if(data[i].winner == 'A')
                pointcolor.push("rgb(66,129,164)");
            else
                pointcolor.push("rgb(255,99,132)");
        }

        var chart = new Chart(chartRadarDOM, {
            type: 'line',
            data:{
                labels: labels,
                datasets: [
                    {
                        fill: false,
                        cubicInterpolationMode:"monotone",
                        backgroundColor: "rgba(66,129,164,0.2)",
                        borderColor: "rgb(216, 212, 212)",
                        pointBorderColor: "#fff",
                        pointBackgroundColor:pointcolor,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        data: datadown
                    },
                    {
                        fill: false,
                        cubicInterpolationMode:"monotone",
                        backgroundColor: "rgba(66,129,164,0.2)",
                        borderColor: "rgb(255, 210, 136)",
                        pointBorderColor: "#fff",
                        pointBackgroundColor:pointcolor,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        data: datainterval
                    },
                    {
                        fill: false,
                        cubicInterpolationMode:"monotone",
                        backgroundColor: "rgba(66,129,164,0.2)",
                        borderColor: "rgb(216, 212, 212)",
                        pointBorderColor: "#fff",
                        pointBackgroundColor:pointcolor,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        data: dataup
                    }
                ]
            },
            options: chartRadarOptions
        });

        //click point handling
        canv.onclick = function(evt){
            var activepoints = chart.getElementAtEvent(evt);
            if (activepoints[0]){
                var id = set + '-' + (activepoints[0]['_index']+1)
                console.log(id)
                $.getJSON("../statistics/rally_type.json", function(data2) {
                    document.getElementById("rallytitle").innerHTML = id + ' 球種分佈圖';
                    //get index from json file
                    index = data2.findIndex(function(item){
                        return id == item.rally;
                    });
    
                    var labels = data2.map(function(item) {
                        return item.result.map(function(e){
                            return e.balltype;            
                        })
                    });
    
                    var dataA = [];
                    for(var i = 0;i<data2[index].result.length;i++){
                        dataA.push(data2[index].result[i].count)
                    }
    
                    var dataB = [];
                    for(var i = 0;i<data2[index+1].result.length;i++){
                        dataB.push(data2[index+1].result[i].count)
                    }

                    console.log(dataA)
                    console.log(dataB)

                    $("#radarChart").show(function(event){
                        var modal = $(this);
                        var canvas = modal.find('.modal-body canvas');
                        var ctx = canvas[0].getContext("2d"); 
                        var chart = new Chart(ctx, {
                            type: "radar",
                            data: {
                                labels: labels[0],
                                datasets: [
                                    {
                                    label: "Player A",
                                    fill: true,
                                    backgroundColor: "rgba(66,129,164,0.2)",
                                    borderColor: "rgba(66,129,164,0.8)",
                                    pointBorderColor: "#fff",
                                    pointBackgroundColor: "rgba(66,129,164,1)",
                                    data: dataA
                                    }, {
                                    label: "Player B",
                                    fill: true,
                                    backgroundColor: "rgba(255,99,132,0.2)",
                                    borderColor: "rgba(255,99,132,1)",
                                    pointBorderColor: "#fff",
                                    pointBackgroundColor: "rgba(255,99,132,1)",
                                    pointBorderColor: "#fff",
                                    data: dataB
                                    }
                                ]
                            },
                            options: {
                                scale:{
                                    ticks:{
                                        min:0,
                                        stepSize:1
                                    },
                                    pointLabels: { 
                                        fontSize:14 
                                    }
                                },
                                legend:{
                                    labels:{
                                        fontColor: 'rgba(248, 184, 82, 1)',
                                        fontSize: 16
                                    }
                                }
                            }
                        });
                    });

                    //close modal chart
                    $(function() {
                        $('.close').click(function() {
                            $('#radarChart').hide(function(event){
                                var modal = $(this);
                                var canvas = modal.find('.modal-body canvas');
                                var ctx = canvas[0].getContext("2d"); 
                                $(".modal-body canvas").remove();
                                $(".modal-body").html('<canvas id="canvas" width="1000" height="800"></canvas>');
                            });
                        });
                    });
                })
            }
            
        }
    });
}

function init_on_off_court(minrally,maxrally){
    var chartRadarDOM;
    var chartRadarData;
    var chartRadarOptions;

    // Chart.defaults.global.responsive = false;
    chartRadarDOM = document.getElementById("on_off_court_chart");
    //custormized options
    chartRadarOptions = 
    {
        legend:{
            labels:{
                fontColor: 'rgba(248, 184, 82, 1)',
                fontSize: 16,
                fontStyle: "bold"
            }
        }
        // responsive:false
    };

    $.getJSON("statistics/on_off_court.json", function(data) {
        // init minrally and maxrally if are undefined,null,0,NaN,empty string,false
        if (!minrally){
            minrally = Math.min.apply(Math, data.map(function(d) { 
                return d.rally; 
            }));
        }
        if (!maxrally){
            maxrally = Math.max.apply(Math, data.map(function(d) { 
                return d.rally; 
            }));
        }

        //count each reason
        var group_data = Object.keys(_.groupBy(data,"on_off_court"))
        var sum_data = new Array(group_data.length).fill(0);
        for(var i = parseInt(minrally);i<=parseInt(maxrally);i++){
            sum_data[data[i-1].on_off_court] += 1;
        }
        console.log(sum_data)
        
        var labels = ["球場內","球場外","掛網"]

        //random color generator
        color = new Array();
        for(var i = 0;i<data.length;i++){
            r = Math.floor(Math.random() * 256);
            g = Math.floor(Math.random() * 256);
            b = Math.floor(Math.random() * 256);
            color.push('rgb(' + r + ', ' + g + ', ' + b + ')');
        }
        
        var chart = new Chart(chartRadarDOM, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    backgroundColor: color,
                    pointBorderColor: "rgba(0,0,0,0)",
                    borderColor: 'rgb(17, 16, 17)',
                    borderWidth: 1,
                    data: sum_data
                }]
            },
            options: chartRadarOptions
        });
    });
}

function init_total_balltype(minrally,maxrally){
    $.getJSON("../statistics/rally_type.json", function(data) {
        var labels = data.map(function(item) {
            return item.result.map(function(e){
                return e.balltype;            
            })
        });

        var total = data.map(function(item){
            return item.result
        });

        var dataA = new Array(data[0].result.length).fill(0);
        var dataB = new Array(data[0].result.length).fill(0);
        for(var i = 0;i<data.length;i+=2){
            rally = parseInt(data[i].rally.split("-")[1]);
            if (rally < minrally || rally > maxrally)
                continue
            for(var j = 0;j<data[i].result.length;j++){
                dataA[j] += data[i].result[j].count;
                dataB[j] += data[i+1].result[j].count
            }
        };

        var canv = document.createElement('canvas');
        canv.id = 'total_balltype_chart';
        canv.width = 800;
        canv.height = 600;
        document.getElementById("total_balltype").appendChild(canv);

        var chartRadarDOM;
        var chartRadarData;
        var chartRadarOptions;

        // Chart.defaults.global.responsive = false;
        chartRadarDOM = document.getElementById("total_balltype_chart");
        //custormized options
        chartRadarOptions = 
        {
            scale:{
                ticks:{
                    min:0,
                    // stepSize:10
                },
                pointLabels: { 
                    fontSize:14 
                }
            },
            legend:{
                labels:{
                    fontColor: 'rgba(248, 184, 82, 1)',
                    fontSize: 16
                }
            }
        };
        
        var chart = new Chart(chartRadarDOM, {
            type: 'radar',
            data:{
                labels: labels[0],
                datasets: [
                    {
                    label: "Player A",
                    fill: true,
                    cubicInterpolationMode:"monotone",
                    backgroundColor: "rgba(66,129,164,0.2)",
                    borderColor: "rgba(66,129,164,1)",
                    pointBorderColor: "#fff",
                    pointBackgroundColor: "rgba(66,129,164,1)",
                    data: dataA
                    }, {
                    label: "Player B",
                    fill: true,
                    cubicInterpolationMode:"monotone",
                    backgroundColor: "rgba(255,99,132,0.2)",
                    borderColor: "rgba(255,99,132,1)",
                    pointBorderColor: "#fff",
                    pointBackgroundColor: "rgba(255,99,132,1)",
                    pointBorderColor: "#fff",
                    data: dataB
                    }
                ]
            },
            options: chartRadarOptions
        });
    });
}

function change_interval(){
    //get interval when clicking submit
    var minrally = document.getElementById("down").value;
    var maxrally = document.getElementById("up").value;

    //delete old linechart
    $('#line_chart').remove();
    init_linechart(minrally, maxrally);

    //delete old doughnut
    $('#on_off_court_chart').remove();
    $('#on_off_court').html('<div class="subtitle">全場失分比例</div>\
    <canvas id="on_off_court_chart" width="800" height="600"></canvas>'); 
    init_on_off_court(minrally,maxrally);

    //delete old radar
    $('#total_balltype_chart').remove();
    $('#total_balltype').html('<div class="subtitle">全場球種統計</div>'); 
    init_total_balltype(minrally,maxrally);
}

function get_interval_up(){
    $.getJSON("statistics/rally_count_real.json", function(data) {
        //filter data to specific set
        data = data.filter(function(item) {
            return item.set == set
        });
        data = data[0].result
        maximum = Math.max.apply(Math, data.map(function(d) { 
            return d.rally;
        }));  
        for(var i=1;i<=maximum;i+=1)
        {
            var insertText = '<option value='+i+'>'+i+'</option>';
            //document.getElementById("up").appendChild=insertText;
            $('#up').append(insertText); 
        }
    })
}
function get_interval_down(){
    $.getJSON("statistics/rally_count_real.json", function(data) {
        //filter data to specific set
        data = data.filter(function(item) {
            return item.set == set
        });
        data = data[0].result
        maximum = Math.max.apply(Math, data.map(function(d) { 
            return d.rally;
        }));  
        for(var i=1;i<=maximum;i+=1)
        {
            var insertText = '<option value='+i+'>'+i+'</option>';
            //document.getElementById("up").appendChild=insertText;
            $('#down').append(insertText); 
        }
    })
}
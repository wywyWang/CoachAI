
function init_linechart(minrally,maxrally,set){
    $.getJSON("statistics/rally_count_real.json", function(data) {
        //init svg legend
        d3.selectAll("svg").remove();

        //init set
        if (!set){
            set = 1;
        }
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
        console.log(set);
        console.log(minrally);
        console.log(maxrally);

        // handmade legend
        var svg_legend = d3.select("#line").append("svg")
                            .attr("width", 740)
                            .attr("height", 30)

        svg_legend.append("circle").attr("cx",190).attr("cy",20).attr("r", 6).style("fill", "rgb(66,129,164)")
        svg_legend.append("circle").attr("cx",470).attr("cy",20).attr("r", 6).style("fill", "rgb(255,99,132)")
        svg_legend.append("text").attr("class", "d3_legend").attr("x", 200).attr("y", 20)
                    .text("Player A Win").style("fill","rgb(66,129,164)").attr("alignment-baseline","middle")
        svg_legend.append("text").attr("class", "d3_legend").attr("x", 480).attr("y", 20)
                    .text("Player B Win").style("fill","rgb(255,99,132)").attr("alignment-baseline","middle")

        var canv = document.createElement('canvas');
        canv.id = 'line_chart';
        canv.width = 640;
        canv.height = 360;
        document.getElementById("line").appendChild(canv);

        var chartRadarDOM;
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
            },
            animation: {
              duration: 1,
              onComplete: function() {
                var chartInstance = this.chart,
                ctx = chartInstance.ctx;

                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                ctx.textAlign = 'center';
                ctx.textBaseline = 'bottom';
                ctx.fillStyle = 'rgba(0,0,0,1)';

                this.data.datasets.forEach(function(dataset, i) {
                  var meta = chartInstance.controller.getDatasetMeta(i);
                  meta.data.forEach(function(bar, index) {
                    var data = dataset.data[index];
                    ctx.fillText(data, bar._model.x, bar._model.y - 5);
                  });
                });
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
                $.getJSON("../statistics/rally_type_real.json", function(data2) {
                    document.getElementById("rallytitle").innerHTML = id + ' 球種分佈圖';
                    //filter data to specific set
                    data2 = data2.filter(function(item) {
                        return item.set == set
                    });
                    data2 = data2[0].info;

                    //get index from json file
                    index = data2.findIndex(function(item){
                        return id.split('-')[1] == item.rally;
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

function init_on_off_court(minrally,maxrally,set){
    //create player info radar
    $('#on_off_court .playerA').html('<div class="subtitle">選手A失分比例</div>\
    <canvas id="on_off_court_chartA" width="800" height="600"></canvas>'); 

    var canvtitle = document.createElement('div');
    canvtitle.className = 'subtitle';
    canvtitle.innerHTML = "選手B失分比例";
    tmp = document.getElementById("on_off_court").getElementsByClassName("playerB")[0].appendChild(canvtitle);
    var canv = document.createElement('canvas');
    canv.id = 'on_off_court_chartB';
    canv.width = 800;
    canv.height = 600;
    document.getElementById("on_off_court").getElementsByClassName("playerB")[0].appendChild(canv);

    var chartRadarDOMA;
    var chartRadarDOMB;
    var chartRadarOptions;

    // Chart.defaults.global.responsive = false;
    chartRadarDOMA = document.getElementById("on_off_court_chartA");
    chartRadarDOMB = document.getElementById("on_off_court_chartB");
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

    $.getJSON("statistics/rally_count_real.json", function(data) {
        //init set
        if (!set){
            set = 1;
        }

        //filter data to specific set
        data = data.filter(function(item) {
            return item.set == set
        });
        data = data[0].result;

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

        //filter data to specific interval
        data = data.filter(function(item) {
            return item.rally >= minrally && item.rally <= maxrally
        });

        //filter winners
        dataB = data.filter(function(item){
            return item.winner == 'A'
        });
        dataA = data.filter(function(item){
            return item.winner == 'B'
        });

        console.log(set);
        console.log(minrally);
        console.log(maxrally);
        
        //count each reason
        var group_data = Object.keys(_.groupBy(data,"on_off_court"));
        var sum_dataA = new Array(group_data.length).fill(0);
        var sum_dataB = new Array(group_data.length).fill(0);
        for(var i = 0;i<dataA.length;i++){
            if (dataA[i].on_off_court == group_data[0])
                sum_dataA[0] +=1;
            else if (dataA[i].on_off_court == group_data[1])
                sum_dataA[1] +=1;
            else
                sum_dataA[2] +=1;
        }
        for(var i = 0;i<dataB.length;i++){
            if (dataB[i].on_off_court == group_data[0])
                sum_dataB[0] +=1;
            else if (dataB[i].on_off_court == group_data[1])
                sum_dataB[1] +=1;
            else
                sum_dataB[2] +=1;
        }

        console.log(sum_dataA);
        console.log(sum_dataB);
        
        
        var labels = group_data;

        //random color generator
        color = new Array();
        for(var i = 0;i<data.length;i++){
            r = Math.floor(Math.random() * 256);
            g = Math.floor(Math.random() * 256);
            b = Math.floor(Math.random() * 256);
            color.push('rgb(' + r + ', ' + g + ', ' + b + ')');
        }
        
        var chart = new Chart(chartRadarDOMA, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    backgroundColor: color,
                    pointBorderColor: "rgba(0,0,0,0)",
                    borderColor: 'rgb(17, 16, 17)',
                    borderWidth: 1,
                    data: sum_dataA
                }]
            },
            options: chartRadarOptions
        });

        var chart = new Chart(chartRadarDOMB, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    backgroundColor: color,
                    pointBorderColor: "rgba(0,0,0,0)",
                    borderColor: 'rgb(17, 16, 17)',
                    borderWidth: 1,
                    data: sum_dataB
                }]
            },
            options: chartRadarOptions
        });
    });
}

function init_total_balltype(minrally,maxrally,set){
    $('#total_balltype .playerA').html('<div class="subtitle">選手A獲勝球種</div>'); 
    var canv = document.createElement('canvas');
    canv.id = 'total_balltype_chartA';
    canv.width = 800;
    canv.height = 600;
    document.getElementById("total_balltype").getElementsByClassName("playerA")[0].appendChild(canv);

    var canvtitle = document.createElement('div');
    canvtitle.className = 'subtitle';
    canvtitle.innerHTML = "選手B獲勝球種";
    document.getElementById("total_balltype").getElementsByClassName("playerB")[0].appendChild(canvtitle);
    var canv = document.createElement('canvas');
    canv.id = 'total_balltype_chartB';
    canv.width = 800;
    canv.height = 600;
    document.getElementById("total_balltype").getElementsByClassName("playerB")[0].appendChild(canv);

    var canvtitle = document.createElement('div');
    canvtitle.className = 'subtitle';
    canvtitle.innerHTML = "全場球種分析";
    document.getElementById("total_balltype").appendChild(canvtitle);
    var canv = document.createElement('canvas');
    canv.id = 'total_balltype_chart';
    canv.width = 600;
    canv.height = 300;
    document.getElementById("total_balltype").appendChild(canv);
    $.getJSON("../statistics/rally_type_real.json", function(data) {
        //init set
        if (!set){
            set = 1;
        }

        //filter data to specific set
        data = data.filter(function(item) {
            return item.set == set
        });
        data = data[0].info;

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

        //filter data to specific interval
        data = data.filter(function(item) {
            return parseInt(item.rally) >= minrally && parseInt(item.rally) <= maxrally;
        });

        console.log(set);
        console.log(minrally);
        console.log(maxrally);

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
            rally = parseInt(data[i].rally);
            for(var j = 0;j<data[i].result.length;j++){
                dataA[j] += data[i].result[j].count;
                dataB[j] += data[i+1].result[j].count
            }
        };

        console.log(dataA);
        console.log(dataB);

        //custormized options
        var chartRadarOptions = 
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

        //rendering each player win balltype
        $.getJSON("statistics/rally_count_real.json", function(data2) {
            //init set
            if (!set){
                set = 1;
            }

            //filter data to specific set
            data2 = data2.filter(function(item) {
                return item.set == set
            });
            data2 = data2[0].result;

            // init minrally and maxrally if are undefined,null,0,NaN,empty string,false
            if (!minrally){
                minrally = Math.min.apply(Math, data2.map(function(d) { 
                    return d.rally; 
                }));
            }
            if (!maxrally){
                maxrally = Math.max.apply(Math, data2.map(function(d) { 
                    return d.rally; 
                }));
            }

            //filter data to specific interval
            data2 = data2.filter(function(item) {
                return item.rally >= minrally && item.rally <= maxrally
            });

            //filter winners
            data2A = data2.filter(function(item){
                return item.winner == 'A'
            });
            data2B = data2.filter(function(item){
                return item.winner == 'B'
            });

            var dataA = new Array(data[0].result.length).fill(0);
            var dataB = new Array(data[0].result.length).fill(0);

            for(var i = 0;i<data2A.length;i++){
                for(var j = 0;j<labels[0].length;j++){
                    if (data2A[i].balltype == labels[0][j])
                        dataA[j] += 1;
                }
            };

            for(var i = 0;i<data2B.length;i++){
                for(var j = 0;j<labels[0].length;j++){
                    if (data2B[i].balltype == labels[0][j])
                        dataB[j] += 1;
                }
            };

            console.log(dataA);
            console.log(dataB);

            var chartRadarOptionsPlayer = 
            {
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
            };

            //create player info radar            
            chartRadarDOMA = document.getElementById("total_balltype_chartA");
            var chart = new Chart(chartRadarDOMA, {
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
                        }
                    ]
                },
                options: chartRadarOptionsPlayer
            });

            //rendering winner B balltype
            chartRadarDOMB = document.getElementById("total_balltype_chartB");
            var chart = new Chart(chartRadarDOMB, {
                type: 'radar',
                data:{
                    labels: labels[0],
                    datasets: [{
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
                options: chartRadarOptionsPlayer
            });
        })
        .done(function(){
            //rendering total balltype
            var chartRadarDOM = document.getElementById("total_balltype_chart");
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
    });
}

function change_interval(){
    //get interval when clicking submit
    var minrally = document.getElementById("down").value;
    var maxrally = document.getElementById("up").value;
    var set = document.getElementById("set").value;

    //delete old linechart
    $('#line_chart').remove();
    init_linechart(minrally,maxrally,set);

    //delete old doughnut
    $('#on_off_court .subtitle').remove();
    $('#on_off_court_chartA').remove();
    $('#on_off_court_chartB').remove();
    init_on_off_court(minrally,maxrally,set);

    //delete old radar
    $('#total_balltype .subtitle').remove();
    $('#total_balltype_chartA').remove();
    $('#total_balltype_chartB').remove();
    $('#total_balltype_chart').remove();
    init_total_balltype(minrally,maxrally,set);
}

function change_set() {
    new_set = document.getElementById("set").value;
    $('#down option').remove();
    $('#up option').remove();
    get_interval_updown(new_set);

    //delete old and refresh new linechart
    $('#line_chart').remove();
    init_linechart(null,null,new_set);

    //delete old doughnut
    $('#on_off_court .subtitle').remove();
    $('#on_off_court_chartA').remove();
    $('#on_off_court_chartB').remove();
    init_on_off_court(null,null,new_set);

    //delete old radar
    $('#total_balltype .subtitle').remove();
    $('#total_balltype_chartA').remove();
    $('#total_balltype_chartB').remove();
    $('#total_balltype_chart').remove();
    init_total_balltype(null,null,new_set);
}

function get_interval_set(){
    $.getJSON("statistics/rally_count_real.json", function(data) {
        //find max set
        var maximum = 0;
        for (var i=0 ; i<data.length ; i++) {
            if (data[i].set > maximum)
                maximum = data[i].set;
        }

        for(var i=1;i<=maximum;i+=1)
        {
            var insertText = '<option value='+i+'>'+i+'</option>';
            //document.getElementById("up").appendChild=insertText;
            $('#set').append(insertText); 
        }
    });
}

function get_interval_updown(set){
    $.getJSON("statistics/rally_count_real.json", function(data) {
        //init set
        if (!set){
            set = 1;
        }

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
            $('#down').append(insertText); 
            $('#up').append(insertText); 
        }
    })
}

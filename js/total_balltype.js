function init_total_balltype(minrally,maxrally){
    $.getJSON("../statistics/rally_type_real.json", function(data) {
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
                    stepSize:10
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
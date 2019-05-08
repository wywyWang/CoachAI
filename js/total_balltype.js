$.getJSON("../statistics/rally_type.json", function(data) {
    var count=1;

    var labels = new Array(data.length/2);
    for(var i=0;i<data.length/2;i+=1){
      labels[i]=count;
      count++;
    }
    var dataA = new Array(data.length/2);
    var countA = 0;
    for(var i=0;i<data.length;i+=2){
      for(var j=0;j<data[i].result.length;j++){
        if(data[i].result[j].balltype=="長球"){
          dataA[countA]=data[i].result[j].count;
          countA++;
        }        
      }
    }
    var dataB = new Array(data.length/2);
    var countB = 0;
    for(var i=1;i<data.length;i+=2){
      for(var j=0;j<data[i].result.length;j++){
        if(data[i].result[j].balltype=="長球"){
          dataB[countB]=data[i].result[j].count;
          countB++;
        }        
      }
    }  

    // }
    // var dataB = data.map(function(item){
    //   if (item.player=='A'){
    //     count+=1;
    //   }
    //   return count;      
    // });
    // var dataA = new Array(data[0].result.length).fill(0);
    // var dataB = new Array(data[0].result.length).fill(0);
    // for(var i = 0;i<data.length;i+=2){
    //     for(var j = 0;j<data[i].result.length;j++){
    //         dataA[j] += data[i].result[j].count;
    //         dataB[j] += data[i+1].result[j].count
    //     }
    // };
    console.log(labels)
    console.log(dataA)
    console.log(dataB)

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
        type: 'line',
        data:{
            labels: labels,
            datasets: [
                {
                  label: "Player A",
                  fill: false,
                  cubicInterpolationMode:"monotone",
                  backgroundColor: "rgba(66,129,164,0.2)",
                  borderColor: "rgba(66,129,164,1)",
                  pointBorderColor: "#fff",
                  pointBackgroundColor: "rgba(66,129,164,1)",
                  data: dataA
                }, {
                  label: "Player B",
                  fill: false,
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
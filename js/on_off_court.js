var canv = document.createElement('canvas');
canv.id = 'on_off_court';
canv.width = 640;
canv.height = 360;
document.body.appendChild(canv);

var chartRadarDOM;
var chartRadarData;
var chartRadarOptions;

//載入雷達圖
Chart.defaults.global.legend.display = false;
Chart.defaults.global.defaultFontColor = 'rgba(0,0,74, 1)';
chartRadarDOM = document.getElementById("on_off_court");
chartRadarOptions = 
{
    scale: 
    {
        ticks: 
        {
            fontSize: 16,
            beginAtZero: true,
            maxTicksLimit: 7,
            min:0,
            max:100
        },
        pointLabels: 
        {
            fontSize: 25,
            color: '#0044BB'
        },
        gridLines: 
        {
            color: '#009FCC'
        }
    },
    responsive: 'true'
};

console.log("---------Rader Data--------");
// https://stackoverflow.com/questions/45273313/use-json-file-with-chart-js
$.getJSON("statistics/on_off_court_sum.json", function(data) {
    console.log(data[0].balltype)
    var forEachIt = data.forEach(function(item, index, array){
        console.log(item, index, array); // 物件, 索引, 全部陣列
    });
    console.log(forEachIt);            // undefined

    var labels = data.map(function(e) {
        return e[0];
    });
    var data = data.map(function(e) {
        return e[1];
    });

    //    var ctx = document.getElementById('myChart').getContext('2d');
    // var chart = new Chart(chartRadarDOM, {
    //     type: 'radar',
    //     data: {
    //         labels: labels,
    //         datasets: [{
    //         backgroundColor: 'rgb(129, 198, 2228)',
    //         borderColor: 'rgb(0, 150, 215)',
    //         data: data
    //         }]
    //     },
    //     options: chartRadarOptions
    // });
});

var graphData =new Array();
graphData.push(100);
graphData.push(40);
graphData.push(65);
graphData.push(20);
graphData.push(97);


console.log("--------Rader Create-------------");
console.log(graphData);
    
//CreateData
chartRadarData = {
    labels: ['STR', 'CON', 'INT', 'WIS', 'CHA'],
    datasets: [{
        label: "Skill Level",
        backgroundColor: "rgba(17, 34, 51,0.8)",
        borderColor: "rgba(63,63,74,.8)",
        pointBackgroundColor: "rgba(63,63,74,1)",
        pointBorderColor: "rgba(0,0,0,0)",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(0,0,0,0.3)",
        pointBorderWidth: 5,
        data: graphData}]
};
    
//Draw
var chartRadar = new Chart(chartRadarDOM, {
    type: 'radar',
    data: chartRadarData,
    options: chartRadarOptions
});
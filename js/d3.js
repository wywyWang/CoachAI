d3.json("../statistics/rally_count.json",function(error,data){
    if (error)
        throw error;
    var width = 640;
    var height = 360;

    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    var xAxis = d3.axisBottom()
        .scale(x)
        .ticks(10);             //ticks : # of label 

    var yAxis = d3.axisLeft()
        .scale(y)
        .ticks(5);

    var valueline = d3.line()
        .x(function (d) {
            return x(d.rally);
        })
        .y(function (d) {
            return y(d.stroke);
        });

    var svg = d3.select("#line_chart")
        .append("svg")
        .attr("width", width+100)
        .attr("height", height+100)
        .append("g");

    // Scale the range of the data
    x.domain(d3.extent(data,
        function (d) {
            return d.rally;
        }));
    y.domain([
        0, d3.max(data,
            function (d) {
                return d.stroke;
            })
    ]);

    var axisXGrid = d3.axisTop()
        .scale(x)
        .ticks(10)
        .tickFormat("")
        .tickSize(-height,0);
    
    var axisYGrid = d3.axisLeft()
      .scale(y)
      .ticks(10)
      .tickFormat("")
      .tickSize(-width,0);
    
    svg.append('g')
     .call(axisXGrid)
     .attr("class", "y gridaxis")
     .attr("fill","none")
     .attr("transform", "translate(30,30)");
    
    svg.append('g')
     .call(axisYGrid)
     .attr("fill","none")
     .attr("class", "y gridaxis")
     .attr("transform", "translate(30,30)");

    svg.append("path") // Add the valueline path.
        .attr("transform", "translate(30,30)")
        .attr("d", valueline(data));

    //draw circle points
    var circles = svg.selectAll("circle")
                                .data(data)
                                .enter()
                                .append("circle");
    
    //Add the circle attributes
    var circleAttributes = circles
                            .attr("id",function(d,i) { return (d.set + '-' + d.rally)})
                            .attr("cx", function (d) { return x(d.rally); })
                            .attr("cy", function (d) { return y(d.stroke); })
                            .attr("r", function (d) { return 3.5; })
                            .attr("transform", "translate(30,30)")
                            .style("fill", function (d) { 
                                if (d.winner == "A")
                                    return "rgb(66,129,164)";
                                else
                                    return "rgb(255,99,132)";
                            })
                            .on("mouseover",handleMouseOver)
                            .on("mouseout",handleMouseOut)
                            .on("click",handleMouseClick)
                            .append("a")
                            .attr("data-toggle","modal")
                            .attr("href","#radarChart");

    function handleMouseClick(d,i){
        var coords = d3.mouse(this);
        console.log(coords);

        //get index from json file
        var id = this.id;
        console.log(id)
        $.getJSON("../statistics/rally_type.json", function(data2) {
            //get index from json file
            index = data2.findIndex(function(item){
                return id == item.rally;
            });

            var labels = data2.map(function(item) {
                return item.result.map(function(e){
                    return e.balltype;            
                })
            });

            var dataA = []
            for(var i = 0;i<data2[index].result.length;i++){
                dataA.push(data2[index].result[i].count)
            }

            var dataB = []
            for(var i = 0;i<data2[index+1].result.length;i++){
                dataB.push(data2[index+1].result[i].count)
            }

            // console.log(dataA)
            // console.log(dataB)

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

        });
    }

    //handleMouseOver & handleMouseOut not working yet
    function handleMouseOver(d,i){
        d3.select(this).attr("r",7);
        console.log("OVER");
    }

    function handleMouseOut(d,i){
        d3.select(this).attr("r",4);
        // console.log("LOO");
    }

    // text value on each points
    for (var i in data){
        svg.append("text")
            .data(data)
            .attr("x", x(data[i]["rally"])-3)
            .attr("y", y(data[i]["stroke"])-5)
            .text(data[i]["stroke"])
            .attr("transform", "translate(30,30)")
            .attr("font-size", "15px")
            .attr("fill","blue");
    }    

    svg.append("g") // Add the X Axis
        .attr("class", "x axis")
        .attr("transform", "translate(30," + String(height+30) + ")")
        .call(xAxis);

    svg.append("g") // Add the Y Axis
        .attr("class", "y axis")
        .attr("transform", "translate(30,30)")
        .call(yAxis);

    //close modal chart
    $(function() {
        $('.close').click(function() {
            $('#radarChart').hide(function(event){
                var modal = $(this);
                var canvas = modal.find('.modal-body canvas');
                var ctx = canvas[0].getContext("2d"); 
                $(".modal-body canvas").remove();
                $(".modal-body").html('<canvas id="canvas" width="1000" height="800"></canvas>');
                console.log("CLOSE")
            });
        });
     });
})

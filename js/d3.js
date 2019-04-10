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

    var svg = d3.select("body")
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
        .attr("d", valueline(data))
        .attr("stroke-dasharray","2.5");

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
                            .style("fill", function (d) { return "black"; })
                            .on("mouseover",handleMouseOver)
                            .on("mouseout",handleMouseOut)
                            .on("click",handleMouseClick)
                            .append("a")
                            .attr("data-toggle","modal")
                            .attr("href","#radarChart");

    function handleMouseClick(d,i){
        var coords = d3.mouse(this);
        console.log(coords);

        // test json file
        var rallydata = [
            {
                "rally":"1-1",
                "result":
                [

                    {
                        "playerA":
                        [
                            {
                                "balltype":"挑球",
                                "count":6
                            },
                            {
                                "balltype":"放小球",
                                "count":5
                            },
                            {
                                "balltype":"挑球",
                                "count":0
                            },
                            {
                                "balltype":"挑球",
                                "count":6
                            },
                            {
                                "balltype":"挑球",
                                "count":7
                            },
                            {
                                "balltype":"挑球",
                                "count":6
                            },
                            {
                                "balltype":"挑球",
                                "count":3
                            }
                        ],
                        "playerB":
                        [
                            {
                                "balltype":"挑球",
                                "count":0
                            },
                            {
                                "balltype":"挑球",
                                "count":4
                            },
                            {
                                "balltype":"挑球",
                                "count":6
                            },
                            {
                                "balltype":"挑球",
                                "count":1
                            },
                            {
                                "balltype":"挑球",
                                "count":5
                            },
                            {
                                "balltype":"挑球",
                                "count":3
                            },
                            {
                                "balltype":"挑球",
                                "count":5
                            }
                        ]
                    }
                ]
            },
            {
                "rally":"1-2",
                "result":
                [
                    {
                        "playerA":
                        [
                            {
                                "balltype":"挑球",
                                "count":7
                            },
                            {
                                "balltype":"放小球",
                                "count":5
                            },
                            {
                                "balltype":"挑球",
                                "count":8
                            },
                            {
                                "balltype":"挑球",
                                "count":9
                            },
                            {
                                "balltype":"挑球",
                                "count":5
                            },
                            {
                                "balltype":"挑球",
                                "count":4
                            },
                            {
                                "balltype":"挑球",
                                "count":3
                            }
                        ],
                        "playerB":
                        [
                            {
                                "balltype":"挑球",
                                "count":2
                            },
                            {
                                "balltype":"挑球",
                                "count":5
                            },
                            {
                                "balltype":"挑球",
                                "count":4
                            },
                            {
                                "balltype":"挑球",
                                "count":2
                            },
                            {
                                "balltype":"挑球",
                                "count":8
                            },
                            {
                                "balltype":"挑球",
                                "count":9
                            },
                            {
                                "balltype":"挑球",
                                "count":5
                            }
                        ]
                    }
                ]
            }
        ];

        //get index from json file
        var id = this.id;
        result = rallydata.findIndex(function(item){
            return id == item.rally;
        });

        var playerA=[];
        playerA = rallydata.map(function(item){
            return item.result[0].playerA.map(function(e){
                return e.count;            
            })
        });
        var playerB=[];
        playerB = rallydata.map(function(item){
            return item.result[0].playerB.map(function(e){
                return e.count;            
            })
        });
        // console.log(playerA[result])
        // console.log(playerB[result])

        $("#radarChart").show(function(event){
            var modal = $(this);
            var canvas = modal.find('.modal-body canvas');
        
            // Chart initialisieren
            var ctx = canvas[0].getContext("2d");

            var chart = new Chart(ctx, {
                type: "radar",
                data: {
                    labels: ["切球", "平球", "挑球", "長球", "小球", "撲球", "殺球"],
                    datasets: [
                        {
                          label: "Player A",
                          fill: true,
                          backgroundColor: "rgba(179,181,198,0.2)",
                          borderColor: "rgba(179,181,198,1)",
                          pointBorderColor: "#fff",
                          pointBackgroundColor: "rgba(179,181,198,1)",
                          data: playerA[result]
                        }, {
                          label: "Player B",
                          fill: true,
                          backgroundColor: "rgba(255,99,132,0.2)",
                          borderColor: "rgba(255,99,132,1)",
                          pointBorderColor: "#fff",
                          pointBackgroundColor: "rgba(255,99,132,1)",
                          pointBorderColor: "#fff",
                          data: playerB[result]
                        }
                    ]
                },
                options: {
                    scale:{
                        ticks:{
                            min:0
                        }
                    }
                }
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
                console.log("CLOSE")
            });
        });
     });
})

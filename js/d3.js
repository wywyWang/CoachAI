d3.json("../statistics/rally_count.json",function(error,data){
    if (error)
        throw error;
    var width = 1280;
    var height = 720;

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

    // Get the data

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
                            .attr("cx", function (d) { return x(d.rally); })
                            .attr("cy", function (d) { return y(d.stroke); })
                            .attr("r", function (d) { return 2; })
                            .attr("transform", "translate(30,30)")
                            .style("fill", function (d) { return "black"; });

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

    
})


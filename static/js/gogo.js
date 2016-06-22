function draw_his(myjson) {
	myjson_text = JSON.stringify(myjson);	
	//console.log(myjson_text);

	var my_data = JSON.parse(myjson_text);
	//console.log(my_data.length)
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            return "<strong>(" + Math.sqrt(d.x * d.x + d.y * d.y) + ")</strong>";
        });
    var width = 1200;
    var height = 300;
    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g");

    svg.call(tip);
    
    var x = d3.scale.linear()
        .range([0, width])
        .domain([0, 21]);

    var y = d3.scale.linear()
        .range([height, 0])
        .domain([0, d3.max(my_data, function(d) { return Math.sqrt(d.x * d.x + d.y * d.y);})]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    svg.append("g")
        .attr("class", "x_axis")
        .attr("transform", "translate(0, " + height + ")")
        .call(xAxis);
    
    svg.append("g")
        .attr("class", "y_axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Hist");

    svg.selectAll(".bar")
        .data(my_data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.i); })
        .attr("y", function(d) { return y(Math.sqrt(d.x * d.x + d.y * d.y)); })
        .attr("width", width/21) 
        .attr("height", function(d) { return height - y(Math.sqrt(d.x * d.x + d.y * d.y)); })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
}

function draw_contour(myjson, color, line_width) {

	myjson_text = JSON.stringify(myjson);	
	//console.log(myjson_text);

	var my_data = JSON.parse(myjson_text);
	//console.log(my_data.length)
	var ary_length = my_data.length;
	//console.log(my_data[0]['x'])

	var canvas = d3.select("svg")
		.attr("width", 800)
		.attr("height", 400)
		.attr("border", "black")

	var group = canvas.append("g")

	var linef = d3.svg.line()
		.x(function(d) {
			return d.x;	
		})
		.y(function(d) {
			return d.y;
		})
		.interpolate("linear");
	var my_path = group.append("path")

	//var lineGraph = d3.select("path")
	var lineGraph = my_path
		.attr("d", linef(my_data))
		.attr("fill", "none")
		.attr("stroke", color)
		.attr("stroke-width", line_width);
}

$(function(){
	$('#press_run').click(function() {
	    	
		$.ajax({
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				"index": $('#my_combobox').val()
				}),
				dataType: 'json',
				url: '/extract',
				success: function(chartData) {
					//console.log(JSON.stringify(chartData));
					myjson = chartData['data'];
					draw_contour(myjson, "green", 3);
					
					myjson1 = chartData['final'];
					draw_contour(myjson1, "red", 1);

                    draw_his(chartData['fd']);

				},
				error: function(error) {
					console.log('error');
					console.log(eval(error));
				}
		});
	});
	
});

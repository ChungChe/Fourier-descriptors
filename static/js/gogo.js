function draw_contour(myjson, color, line_width) {

	myjson_text = JSON.stringify(myjson);	
	//console.log(myjson_text);

	var my_data = JSON.parse(myjson_text);
	//console.log(my_data.length)
	var ary_length = my_data.length;
	//console.log(my_data[0]['x'])

	var canvas = d3.select("svg")
		.attr("width", 800)
		.attr("height", 800)
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


				},
				error: function(error) {
					console.log('error');
					console.log(eval(error));
				}
		});
	});
	
});

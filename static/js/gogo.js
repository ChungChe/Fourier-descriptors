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
					/*
					$("#algorithmChart").empty();
					machines = []
					labels = []
					var morrisChart = Morris.Line({
						element: 'algorithmChart',
						data: chartData['data'],
						xkey: 'datetime',
						parseTime: true,
						ykeys: machines,
						labels: labels,
						lineWidth: 1,
						smooth: true,
						goals: [120],
						goalStrokeWidth: 5
					});
					*/
					myjson = chartData['data'];
					myjson_text = JSON.stringify(myjson);	
					console.log(myjson_text);

					var my_data = JSON.parse(myjson_text);
					console.log(my_data.length)
					var ary_length = my_data.length;
					console.log(my_data[0]['x'])

					var canvas = d3.select("body").append("svg")
						.attr("width", 500)
						.attr("height", 500)
						.attr("border", "black")
					var group = canvas.append("g")
						.attr("transform", "translate(100, 10)")
					var line = d3.svg.line()
						.x(function(d, i) {
							return d.x;	
						})
						.y(function(d, i) {
							return d.y;
						});

					group.selectAll("path")
						.data(my_data).enter()
						.append("path")
						.attr("d", function(d){ return line(d) })
						.attr("fill", "none")
						.attr("stroke", "green")
						.attr("stroke-width", 3);



					/*
					var p = path();
					for (var i = 0; i < ary_length - 1; ++i) {
						p.moveTo(data[i]['x'], data[i]['y'])
						p.lineTo(data[i+1]['x'], data[i+1]['y'])
					}
					p.closePath();
					*/

				},
				error: function(error) {
					console.log('error');
					console.log(eval(error));
				}
		});
	});
	
});

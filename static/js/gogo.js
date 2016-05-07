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
					console.log(JSON.stringify(chartData));
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
				},
				error: function(error) {
					console.log('error');
					console.log(eval(error));
				}
		});
	});
	
});

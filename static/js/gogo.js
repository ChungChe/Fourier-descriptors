
function get_machine_list() {
	mylist = [];
	for (i = 1; i <= 25; ++i) {
		if (document.getElementById("check_machine_" + i).checked) {
			mylist.push(i);
		}
	}
	return mylist;
}

function select(flag) {
	for (i = 1; i <= 25; ++i) {
		document.getElementById("check_machine_" + i).checked = flag;
	}
}

function set_start_time(value) {
	if (typeof value == 'undefined') {
		return;
	}
	$('#date_timepicker_start').val(value);
}

function set_end_time(value) {
	if (typeof value == 'undefined') {
		return;
	}
	$('#date_timepicker_end').val(value);
}

function get_min_datetime(chartData) {
	var data_size = chartData['data'].length;
	var min_time = chartData['data'][0]['datetime'];
	for (i = 1; i < data_size; ++i) {
		if (chartData['data'][i]['datetime'] < min_time) {
			min_time = chartData['data'][i]['datetime'];
		}
	}
	return min_time
}

function get_max_datetime(chartData) {
	var data_size = chartData['data'].length;
	var max_time = chartData['data'][0]['datetime'];
	for (i = 1; i < data_size; ++i) {
		if (chartData['data'][i]['datetime'] > max_time) {
			max_time = chartData['data'][i]['datetime'];
		}
	}
	return max_time
}

$(function(){
	var min_datetime, max_datetime;
	jQuery.datetimepicker.setLocale('zh-TW');
	$('#date_timepicker_start').datetimepicker({format: 'Y-m-d H:i:s'});
	$('#date_timepicker_end').datetimepicker({format: 'Y-m-d H:i:s'});
	$('#start_button').click(function() {
		set_start_time(min_datetime);
	});
	$('#end_button').click(function() {
		set_end_time(max_datetime);
	});
	$('#press_go').click(function() {
		var machine_list = get_machine_list();	
	    	
		$.ajax({
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				"datetime_start" : $('#date_timepicker_start').val(),
				"datetime_end" : $('#date_timepicker_end').val(),
				"mlist" : machine_list
				}),
				dataType: 'json',
				url: '/draw_chart',
				success: function(chartData) {
					var data_size = chartData['data'].length;
					min_datetime = get_min_datetime(chartData);
					max_datetime = get_max_datetime(chartData);
					
					$("#result").html("共有" +  data_size + "筆資料，起始時間：" + min_datetime + "，結束時間：" + max_datetime);
					
					$("#algorithmChart").empty();
					machines = []
					labels = []
					machine_list.forEach(function(m_id) {
						machines.push("M" + m_id);
						labels.push("M" + m_id);
					});
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
				},
				error: function(error) {
					console.log('error');
					console.log(eval(error));
				}
		});
	});
	
});

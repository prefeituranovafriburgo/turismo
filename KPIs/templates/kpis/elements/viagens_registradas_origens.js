google.charts.setOnLoadCallback(drawBasicOrigens);

function drawBasicOrigens() {

      var data = google.visualization.arrayToDataTable([
        ['Origens', 'Registros',],
        ['Nova Friburgo, RJ', 8175000],
      ]);

      var options = {
        legend: 'none',
        title: 'Principais origens registradas',        
        chartArea: {width: '50%'},
        hAxis: {
          title: '',
          minValue: 0
        },
        vAxis: {
          title: 'Origens'
        }
      };

      var chart_origens = new google.visualization.BarChart(document.getElementById('chart_div_origens'));

      chart_origens.draw(data, options);
    }
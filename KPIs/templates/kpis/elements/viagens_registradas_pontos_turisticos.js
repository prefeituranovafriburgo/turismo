google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {

      var data = google.visualization.arrayToDataTable([
        ['Origens', 'Registros',],
        ['Cão Sentado', 8175000],
      ]);

      var options = {
        legend: 'none',
        title: 'Principais pontos turisticos registradas',        
        chartArea: {width: '50%'},
        hAxis: {
          title: '',
          minValue: 0
        },
        vAxis: {
          title: 'Pontos turisticos'
        }
      };

      var chart2 = new google.visualization.BarChart(document.getElementById('chart_div_pontos_turisticos'));

      chart2.draw(data, options);
    }
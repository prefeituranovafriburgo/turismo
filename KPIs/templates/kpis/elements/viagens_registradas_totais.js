google.charts.setOnLoadCallback(drawChart);

  // Callback that creates and populates a data table,
  // instantiates the pie chart, passes in the data and
  // draws it.
  
  function drawChart() {

    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Topping');
    data.addColumn('number', 'Slices');
    data.addRows([
      ['Turismo e Compras', {{total_turismo}}],
      ['Exclusivamente Compras', {{total_compras}}],

    ]);

    // Set chart options
    var options = {'title':'',
                   'width':600,
                   'height':300};

    // Instantiate and draw our chart, passing in some options.
    var chart_viagens = new google.visualization.PieChart(document.getElementById('chart_div_viagens'));
    chart_viagens.draw(data, options);
  }

  
google.charts.setOnLoadCallback(drawBasic0);

function drawBasic0() {
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'X');
    data.addColumn('number', 'Cadastros');

    data.addRows([
      {% for i in date_usuarios %}
      [{{forloop.counter}}, {{i}}],
      {% endfor %}
    ]);

    var options = {
      legend: 'none',
      title: 'Usuários cadastrados neste mês',
      Width: '100%',
      height: 'auto',
      hAxis: {
        title: '',
        format: '0'
      },
      vAxis: {
        title: '',
        format: '0'
      }
    };

    var chart_usuarios = new google.visualization.LineChart(document.getElementById('chart_div_usuarios'));

    chart_usuarios.draw(data, options);
  }

  google.charts.setOnLoadCallback(drawBasic2);

function drawBasic2() {
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'X');
    data.addColumn('number', 'Cadastros');

    data.addRows([
      [0, 0],
      {% for i  in date_usuarios_anual %}
      [{{forloop.counter}}, {{i}}],
      {% endfor %}
      [9, 0],
      [12, 0],
    ]);

    var options = {
      legend: 'none',
      title: 'Usuários cadastrados neste ano',    
      Width: '100%',
      height: 'auto',
      hAxis: {
        title: '',
        format: '0'
      },
      vAxis: {
        title: '',
        format: '0'
      }, 
      series: {
        0: { color: '#6f9654' },
      }     
    };

    var chart_usuarios_anual = new google.visualization.LineChart(document.getElementById('chart_div_usuarios_anual'));

    chart_usuarios_anual.draw(data, options);
  }
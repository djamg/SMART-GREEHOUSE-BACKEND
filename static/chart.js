var jsonfile;
    var xmlhttp = new XMLHttpRequest();
    var url2 = "/api/list_sensor/30";
    xmlhttp.open("GET",url2,true);
    xmlhttp.send();
    xmlhttp.onreadystatechange = function(){
      if(this.readyState == 4 && this.status == 200){
        var jsonfile = JSON.parse(this.responseText);
        console.log(jsonfile.reverse());

      var labels = jsonfile.map(function(e) {
      return e.time_stamp;
    });

    var labels = jsonfile.map(function(e) {
      return e.time_stamp;
    });

    var data1 = jsonfile.map(function(e) {
      return e.soil_humidity;
    });

    var data2 = jsonfile.map(function(e) {
      return e.temperature;
    });

    var data3 = jsonfile.map(function(e) {
      return e.humidity;
    });

    const data = {
      labels: labels,
      datasets: [{
        label: 'Soil Moisture',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: data1
      },
      {
        label: 'Temperature',
        backgroundColor: 'rgb(55, 9, 152)',
        borderColor: 'rgb(55, 9, 152)',
        data: data2
      },
      {
        label: 'Humidity',
        backgroundColor: 'rgb(155, 19, 52)',
        borderColor: 'rgb(155, 19, 52)',
        data: data3
      }
    ]
    };

    const config = {
      type: 'line',
      data,
      options: {
        lineTension: 0.5,
        pointRadius:1.5,
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 10
                    }
                }
            }
        },
        maintainAspectRatio: false,
        animation: {
            duration: 2000, // general animation time
        },
        hover: {
            animationDuration: 2000, // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 2000, // animation duration after a resize
        
      },
        scales: {
          
          x: {
            ticks: {
              display: false,
            },
            grid: {
                display: false
              },
            
          },
        }
        
      }
    };
    // === include 'setup' then 'config' above ===
  
    var myChart = new Chart(
      document.getElementById('myChart'),
      config
    );
    
  }
    
    

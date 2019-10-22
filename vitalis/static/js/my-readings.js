var ctx = document.getElementById('chart_oximetro_pulso').getContext('2d');
// var ctx_temperature = document.getElementById('chart_temperatura').getContext('2d');

var chart = new Chart(ctx, {
  type: 'line',
  data: {
    datasets: [{
      label: "Vermelho",
      borderColor: 'rgba(255, 0, 0, 0.6)',
      backgroundColor: 'rgba(255, 0, 0, 0.1)',
      data: []
    }, {
      label: "InfraVermelho",
      borderColor: 'rgba(138, 43, 226, 0.6)',
      backgroundColor: 'rgba(138, 43, 226, 0.1)',
      data: []
    }]
  },
  labels: ['lorem', 'lorem'],

  options: {
    scales: {
      xAxes: [{
        realtime: {
          onRefresh: function(chart) {
            chart.data.datasets.forEach(function(dataset) {
              dataset.data.push({
                x: Date.now(),
                y: Math.random()
              });
            });
          }
        },

        label: 'lorem lorem',

        type: 'realtime'
      }]
    }
  }
});


// var chart_temperatura = new Chart(ctx_temperature, {
//   type: 'line',
//   data: {
//     datasets: [{
//       data: []
//     }, {
//       data: []
//     }]
//   },
//
//   options: {
//     scales: {
//       xAxes: [{
//         realtime: {
//           onRefresh: function(chart) {
//             chart.data.datasets.forEach(function(dataset) {
//               dataset.data.push({
//                 x: Date.now(),
//                 y: 36.5 + Math.random() * 2
//               });
//             });
//           }
//         },
//
//         label: 'lorem lorem',
//
//         type: 'realtime'
//       }]
//     }
//   }
// });

$(document).ready(function() {
  var last_buffer_red;
  var last_buffer_ir;

  var ctx = document.getElementById('chart_oximetro_pulso').getContext('2d');
  // var ctx_temperature = document.getElementById('chart_temperatura').getContext('2d');

  var oiias = true;
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
            duration: 5000, //ms
            refresh: 1000,      // onRefresh callback will be called every 1000 ms
            delay: 2000,        // delay of 1000 ms, so upcoming values are known before plotting a line
            pause: false,       // chart is not paused
            ttl: undefined,     // data will be automatically deleted as it disappears off the chart
            onRefresh: function(chart) {
              var data;
              $.getJSON("/bpm_data", {data}, function(data, textStatus){
                // handle your JSON results
                handle_oxymetry_value(data);

                // chart.data.datasets[0].data = data['buffer_red'];
                // chart.data.datasets[1].data = data['buffer_ir'];

                // NOTE: Buffer RED
                data['buffer_red'].forEach(function(item, index, arr){
                  chart.data.datasets[0].data.push({
                    x: Date.now()-((arr.length-index)*10),
                    y: item,
                  });
                  // if (chart.data.datasets[0].data.length > 500) {
                  //   chart.data.datasets[0].data.shift();
                  // }
                });
                // // NOTE: Buffer IR
                data['buffer_ir'].forEach(function(item, index, arr){
                  chart.data.datasets[1].data.push({
                    x: Date.now()-((arr.length-index)*10),
                    y: item,
                  });
                  // if (chart.data.datasets[1].data.length > 500) {
                  //   chart.data.datasets[1].data.shift();
                  // }
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

  function update_chart_data(ir_data, red_data) {
    chart.data.datasets[0].data = red_data;
    chart.data.datasets[1].data = ir_data;
    // console.log(chart);
    // last_buffer_red = red_data;
  }

  function handle_temperature_value(data) {
    $("#id_salva_temperatura").text(
      data['temperature'].toFixed(2) + " ºC"
    );

    var extra_text = "";
    var med_status = "";

    if (data['temperature'] >= 44) {
      $("#id_salva_temperatura").css("color", "#FF0EF0");
      med_status = "MEDICAL EMERGENCY";
      extra_text = "Almost certainly death will occur; however, people have been known to survive up to 46.5 °C";
    } else if (data['temperature'] >= 43) {
      $("#id_salva_temperatura").css("color", "#FF03F0");
      med_status = "MEDICAL EMERGENCY";
      extra_text = "Normally death, or there may be serious brain damage, continuous convulsions and shock. Cardio-respiratory collapse will likely occur.";
    } else if (data['temperature'] >= 42) {
      $("#id_salva_temperatura").css("color", "#FF0090");
      med_status = "MEDICAL EMERGENCY";
      extra_text = "Subject may turn pale or remain flushed and red. They may become comatose, be in severe delirium, vomiting, and convulsions can occur. Blood pressure may be high or low and heart rate will be very fast.";
    } else if (data['temperature'] >= 41) {
      $("#id_salva_temperatura").css("color", "#FF0000");
      med_status = "MEDICAL EMERGENCY";
      extra_text = "Fainting, vomiting, severe headache, dizziness, confusion, hallucinations, delirium and drowsiness can occur. There may also be palpitations and breathlessness.";
    } else if (data['temperature'] >= 40) {
      $("#id_salva_temperatura").css("color", "#FF3c00");
      med_status = "Hot";
      extra_text = "Fainting, dehydration, weakness, vomiting, headache, breathlessness and dizziness may occur as well as profuse sweating. Starts to be life-threatening.";
    } else if (data['temperature'] >= 39) {
      $("#id_salva_temperatura").css("color", "#FF9600");
      med_status = "Hot";
      extra_text = "Severe sweating, flushed and red. Fast heart rate and breathlessness. There may be exhaustion accompanying this. Children and people with epilepsy may be very likely to get convulsions at this point.";
    } else if (data['temperature'] >= 38) {
      $("#id_salva_temperatura").css("color", "#FFf000");
      med_status = "Hot";
      extra_text = "(Classed as hyperthermia if not caused by a fever) – Feeling hot, sweating, feeling thirsty, feeling very uncomfortable, slightly hungry. If this is caused by fever, there may also be chills.";
    } else if (data['temperature'] >= 37.5) {
      $("#id_salva_temperatura").css("color", "#d7ff00");
      med_status = "Febre";
      extra_text = "Temperature over 37.5 ºC.";
    } else if (data['temperature'] >= 36.5) {
      $("#id_salva_temperatura").css("color", "#17ff00");
      med_status = "Normal";
      extra_text = "A typically reported range for normal body temperature";
    } else if (data['temperature'] >= 36) {
      $("#id_salva_temperatura").css("color", "#00ffa8");
      med_status = "Normal in sleep";
      extra_text = "Feeling cold, mild to moderate shivering. Body temperature may drop this low during sleep. May be a normal body temperature.";
    } else if (data['temperature'] >= 35) {
      $("#id_salva_temperatura").css("color", "#00e4ff");
      med_status = "Hypothermia";
      extra_text = "Intense shivering, numbness and bluish/grayness of the skin. There is the possibility of heart irritability.";
    } else if (data['temperature'] >= 34) {
      $("#id_salva_temperatura").css("color", "#00b4ff");
      med_status = "Hypothermia";
      extra_text = "Severe shivering, loss of movement of fingers, blueness and confusion. Some behavioural changes may take place.";
    } else if (data['temperature'] >= 33) {
      $("#id_salva_temperatura").css("color", "#0084ff");
      med_status = "Hypothermia";
      extra_text = "Moderate to severe confusion, sleepiness, depressed reflexes, progressive loss of shivering, slow heart beat, shallow breathing. Shivering may stop. Subject may be unresponsive to certain stimuli.";
    } else if (data['temperature'] >= 32) {
      $("#id_salva_temperatura").css("color", "#0054ff");
      med_status = "MEDICAL EMERGENCY";
      extra_text = "Hallucinations, delirium, complete confusion, extreme sleepiness that is progressively becoming comatose. Shivering is absent (subject may even think they are hot). Reflex may be absent or very slight.";
    } else if (data['temperature'] >= 31) {
      $("#id_salva_temperatura").css("color", "#0022ff");
      med_status = "MEDICAL EMERGENCY";
      extra_text = "Comatose, very rarely conscious. No or slight reflexes. Very shallow breathing and slow heart rate. Possibility of serious heart rhythm problems.";
    } else if (data['temperature'] >= 28) {
      $("#id_salva_temperatura").css("color", "#0000ff");
      med_status = "MEDICAL EMERGENCY";
      extra_text = "Severe heart rhythm disturbances are likely and breathing may stop at any time. Patient may appear to be dead.";
    } else if (data['temperature'] >= 24) {
      $("#id_salva_temperatura").css("color", "#0200ff");
      med_status = "MEDICAL EMERGENCY";
      extra_text = "Death usually occurs due to irregular heart beat or respiratory arrest; however, some patients have been known to survive with body temperatures as low as 14.2 °C";
    } else {
      $("#id_salva_temperatura").css("color", "#000000");
      med_status = "-";
      extra_text = "Paciente não detectado.";
    }

    if (data['connected'] == 0) {
      $("#id_salva_temperatura").css("color", "grey");
      $("#id_salva_temperatura").attr('title', data['error_msg']);
    } else {
      $("#id_salva_temperatura").attr('title', med_status);
    }

    $("#id_p_status").text(
      "Status: " + med_status
    );
    $("#id_p_cad").text(
      "CAD (Ajuda ao Diagnóstico): " + extra_text
    );
  }

  function handle_oxymetry_value(data) {
    var extra_text_bpm = "";
    var extra_text_spo2 = "";
    var med_status_bpm = "";
    var med_status_spo2 = "";

    if (data['connected_bpm'] == 0) {
      $("#id_salva_freq_cardiaca").css("color", "grey");
      $("#id_salva_spo2").css("color", "grey");
      $("#id_salva_freq_cardiaca").attr('title', data['error_bpm']);
      $("#id_salva_spo2").attr('title', data['error_bpm']);
    } else {
      $("#id_salva_freq_cardiaca").attr('title', med_status_bpm);
      $("#id_salva_spo2").attr('title', med_status_spo2);
    }

    $("#id_salva_freq_cardiaca").text(
      data['bpm'] + " bpm"
    );

    $("#id_p_status_heart").text(
      "Status: " + med_status_bpm
    );
    $("#id_p_cad_heart").text(
      "CAD (Ajuda ao Diagnóstico): " + extra_text_bpm
    );


    $("#id_salva_spo2").text(
      data['spo2'] + " %"
    );

    $("#id_p_status_spo2").text(
      "Status: " + med_status_spo2
    );
    $("#id_p_cad_spo2").text(
      "CAD (Ajuda ao Diagnóstico): " + extra_text_spo2
    );

    // update_chart_data(data['buffer_ir'], data['buffer_red'])
  }

  function get_temperature_timer() {
      var data;
      $.getJSON("/tmp_data", {data}, function(data, textStatus){
        // handle your JSON results
        handle_temperature_value(data);
        // Call the timeout at the end of the AJAX response
        // This prevents your race condition
        setTimeout(function(){
            get_temperature_timer();
        }, 1000);
      });
  }

  function get_oximetry_timer() {
      var data;
      $.getJSON("/bpm_data", {data}, function(data, textStatus){
        // handle your JSON results
        handle_oxymetry_value(data);
        // Call the timeout at the end of the AJAX response
        // This prevents your race condition
        setTimeout(function(){
            get_oximetry_timer();
        }, 1000);
      });
  }

  setTimeout(function(){
      get_temperature_timer();
  }, 1000);

  setTimeout(function(){
      get_oximetry_timer();
  }, 1000);
});

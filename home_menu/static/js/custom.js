$(document).ready(function(){
    $( function() {
        $( "#slider-range" ).slider({
          range: true,
          min: 1,
          max: 100,
          values: [ 1, 100 ],

          slide: function( event, ui ) {
            $( "#amount" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
          },
          change: function( event, ui ) {
            $('#id_age1').val(ui.values[0])
            $('#id_age2').val(ui.values[1]);
          }
        });
        $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) +
          " - " + $( "#slider-range" ).slider( "values", 1 ) );
    });

    $( function() {
      $( ".controlgroup" ).controlgroup()
      $( ".controlgroup-vertical" ).controlgroup({
        "direction": "vertical"
      });
  } );

  $(".ui-spinner-input").spinner({
          min: 0,
          max: 2,
          step: 0.01,


          change: function( event, ui ) {
            var min_val = - $( "#eventTmin" ).spinner( "value" );
            var max_val = $( "#eventTmax" ).spinner( "value" );
            $( "#slider-range-baseline" ).slider({
              min: min_val
              });
            $('#id_event_tmin').val(min_val);
            $('#id_event_tmax').val(max_val);


          }

    }).on('input', function () {
    if ($(this).data('onInputPrevented')) return;
    var val = this.value,
        $this = $(this),
        max = $this.spinner('option', 'max'),
        min = $this.spinner('option', 'min');
    // We want only number, no alpha.
    // We set it to previous default value.
    if (!val.match(/^[+-(0/.)/.]?[\d]{0,}$/)) val = $(this).data('defaultValue');
    this.value = val > max ? max : val < min ? min : val;
}).on('keydown', function (e) {
    // we set default value for spinner.
    if (!$(this).data('defaultValue')) $(this).data('defaultValue', this.value);
    // To handle backspace
    $(this).data('onInputPrevented', e.which === 8 ? true : false);
});


    $( function() {
        $( "#slider-range-baseline" ).slider({
          range: true,
          step: 0.01,
          min: -1,
          max: 0,
          values: [ 0, 0 ],

          slide: function( event, ui ) {
            $( "#baseline-amount" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
          },
          change: function( event, ui ) {
            $('#id_baseline_tmin').val(ui.values[0]);
            $('#id_baseline_tmax').val(ui.values[1]);
          }
        });
        $( "#baseline-amount" ).val( $( "#slider-range-baseline" ).slider( "values", 0 ) +
          " - " + $( "#slider-range-baseline" ).slider( "values", 1 ) );
    });




$( function() {
    $('.jq-radio-input, .jq-checkbox-input').checkboxradio({
      icon: false
    });
  } );


$( function() {
    $( "#dialog" ).dialog({
      autoOpen: false,
      show: {
        effect: "clip",
        duration: 500
      },
      hide: {
        effect: "clip",
        duration: 500
      }
    });


    $( "#allWords" ).on( "click", function() {
      $( "#dialog" ).dialog( "close" );
      $('input[name="catCheck"]').each(function() {
            this.checked = false;
        });
      $('input[name="wordsCheck"]').each(function() {
            this.checked = false;
        });
      $('#cat-selector').val("all");
      $('#words-selector').val("");
      console.log($('#cat-selector').val())
      console.log($('#words-selector').val())

    });

    $( "#openerSpeCat" ).on( "click", function() {
      $( "#dialog" ).dialog( "open" );
      $('#dialogContent1').css('display', 'block') ;
      $('#dialogContent2').css('display', 'none') ;
      $('input[name="catCheck"]').each(function() {
            this.checked = false;
        });
      $('input[name="catCheck"]').checkboxradio( "refresh" );
      $('#cat-selector').val("");
      $('#words-selector').val("");

    });

    $( "#openerSpeWords" ).on( "click", function() {
      $( "#dialog" ).dialog( "open" );
      $('#dialogContent1').css('display', 'none') ;
      $('#dialogContent2').css('display', 'block') ;
      $('input[name="wordsCheck"]').each(function() {
            this.checked = false;
        });
      $('input[name="wordsCheck"]').checkboxradio( "refresh" );
      $('#words-selector').val("");
      $('#cat-selector').val("");


    });

    $('#select-all').on("click", function(){
      var ch_list = []
      if (this.checked){
        $('input[name="channels_list"]').each(function() {
          if (this.id.length < 4) {
            ch_list += this.id + ","
          }
          this.checked = true;
        });
        $('#ch-list').val(ch_list);
      } else {
        $('input[name="channels_list"]').each(function() {
            this.checked = false;
        });
        $('#ch-list').val("");
      }
      console.log($('#ch-list').val())
    });

  } );



});

function changeThis(sender, id) {
  if(document.getElementById(id).checked){
    document.getElementById('sett-opt').style.display= 'block' ;
    document.getElementById('deleteSett').href = '/delete_dataset/' + id.toString();
    document.getElementById('buildSett').href = '/build_dataset/' + id.toString();

  }

}

function downloadZip(sender, id) {
  if(document.getElementById(id).checked){
  document.getElementById('download-display').style.display= 'block' ;
    document.getElementById('download-data').href = '/download-eeglab-data/' + id.toString();
  }

}

function checkboxListing(sender, stim_input, list_id) {
  if(stim_input.checked){
    document.getElementById(list_id).value += stim_input.id.toString() + ",";
    console.log(document.getElementById(list_id).value)
  } else {
    document.getElementById(list_id).value = document.getElementById(list_id).value.replace(stim_input.id +",", "");
    console.log(document.getElementById(list_id).value)
  }
}
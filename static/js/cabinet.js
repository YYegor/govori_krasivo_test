
function config_load()
{
 console.log("config_load start") 
 var cfg = JSON.parse(cfgdata);
 console.log("config_load "+cfg[0].app_server)
}

function load_lib()
{
  console.log("load_lib start")
  
  url = '/logo_text';
  $.get( url, function( data ) {
    $( "#libtext_div" ).html( data );
    console.log( "load_lib success" );
});
}


function save_config(e)
{	
	console.log("save config start");
	//console.log($("#module1_text").val());
	//console.log($("#module1_video").val());
	//console.log($("#module1_uaction").val());
	
  	

  url = '/save_week';
  
	
  	function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}
	
	
	var datas = getFormData($("#form"));

  	
  	$.ajax(url, {
    data : JSON.stringify(datas),
    contentType : 'application/json',
    type : 'POST',
    success: function (data) {
      	console.log("week save success");
  
	},
    error: function() {
    	console.log("week save failed");
    }
        
  });
};	

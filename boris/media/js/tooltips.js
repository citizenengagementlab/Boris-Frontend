/* JS for Tooltip behavior */


// State Requirements forms

$("document").ready(function() {

//Hide tooltips on ready

	$("#tooltip_text_email").hide();
	$("#tooltip_text_zip_code").hide();
	

	$("#tooltip_email").toggle(function() {
	
		$("#tooltip_text_email").show();
		}, function() { 
		
		$("#tooltip_text_email").hide(); 
		
		
	});
	
	$("#tooltip_zip_code").toggle(function() {
	
		$("#tooltip_text_zip_code").show();
		
		}, function() { 
		
		$("#tooltip_text_zip_code").hide(); 
		
		
	});
	
	});
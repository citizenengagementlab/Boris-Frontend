/* JS for Tooltip behavior */


// State Requirements forms

$("document").ready(function() {

//Hide tooltips on ready

	$("#tooltip_text_email").hide();
	$("#tooltip_text_zip_code").hide();
	$("#tooltip_text_address").hide();
	$("#tooltip_text_personal").hide();
	$("#tooltip_text_dob").hide();
	$("#tooltip_text_change_of_name").hide();
	$("#tooltip_text_has_different_address").hide();
	$("#tooltip_text_change_of_address").hide();

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
		
	$("#tooltip_address").toggle(function() {
		$("#tooltip_text_address").show();
		}, function() { 
		$("#tooltip_text_address").hide(); 
	});
	
	$("#tooltip_has_different_address").toggle(function() {
		$("#tooltip_text_has_different_address").show();
		}, function() { 
		$("#tooltip_text_has_different_address").hide(); 
	});
	
	$("#tooltip_change_of_address").toggle(function() {
		$("#tooltip_text_change_of_address").show();
		}, function() { 
		$("#tooltip_text_change_of_address").hide(); 
	});
	
	$("#tooltip_personal").toggle(function() {
		$("#tooltip_text_personal").show();
		}, function() { 
		$("#tooltip_text_personal").hide(); 
	});
	
	$("#tooltip_change_of_name").toggle(function() {
		$("#tooltip_text_change_of_name").show();
		}, function() { 
		$("#tooltip_text_change_of_name").hide(); 
	});
	
	$("#tooltip_id_number").toggle(function() {
		$("#tooltip_text_id_number").show();
		}, function() { 
		$("#tooltip_text_id_number").hide(); 
	});
	
	$("#tooltip_id_number").toggle(function() {
		$("#tooltip_text_id_number").show();
		}, function() { 
		$("#tooltip_text_id_number").hide(); 
	});
	
	$("#tooltip_dob").toggle(function() {
		$("#tooltip_text_dob").show();
		}, function() { 
		$("#tooltip_text_dob").hide(); 
	});
	
	$("#tooltip_phone").toggle(function() {
		$("#tooltip_text_phone").show();
		}, function() { 
		$("#tooltip_text_phone").hide(); 
	});
	
	$("#tooltip_race").toggle(function() {
		$("#tooltip_text_race").show();
		}, function() { 
		$("#tooltip_text_race").hide(); 
	});
	
	$("#tooltip_party").toggle(function() {
		$("#tooltip_text_party").show();
		}, function() { 
		$("#tooltip_text_party").hide(); 
	});
});
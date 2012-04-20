var api_url = "/rtv";

(function( $ ){
	$.fn.serializeJSON=function() {
		var json = {};
		jQuery.map($(this).serializeArray(), function(n, i){
			//convert checkbox state to boolean
			if (n['value']==="on") { 	n['value']=1; }
			if (n['value']==="off") { n['value']=0; }
			json[n['name']] = n['value'];
		});
		return json;
	};
})( jQuery );

function zipLookup(zip) {
	var response = null;
	$.ajax({
		type:"get",
		url:"/usps/zip_lookup",
		data:{'zip':zip},
		success:function(data) {
			$('#home_zip_code').val(data.zip);
			$('#home_city').val(data.city);
			$('#home_state_id').val(data.state);
		},
	});
}



$(document).ready(function() {

	//hide optional fields
		$(".mailing").hide();
		$(".name-change").hide();
		$(".address-change").hide();
		
	// Hide second page of registration form - swap sections when state requirements is done.
		
		$("#registration_form").hide();
		
		$("input#get_started").click(function() {
	 			$('#state_form').hide();
	 			$('#registration_form').show();
	  	});	
	
	//hide "start over" link until "get started" button is clicked
	
		$("input#get_started").click(function() {
			$("#top_link").show();
		});
	
	// Reveal optional fields when checkbox is checked - otherwise, hide.	
	$("#has_different_address").click(function() {
	 		if($("#has_different_address").is(":checked")) {
	 			$('.mailing').fadeIn();
	 		} else {
	 			$('.mailing').fadeOut();
	 		}	
	 	});	
	 	
	 	$("#change_of_name").click(function() {
	 		if($("#change_of_name").is(":checked")) {
	 			$('.name-change').fadeIn();
	 		} else {
	 			$('.name-change').fadeOut();
	 		}
	 	});	
	 	
	 	$("#change_of_address").click(function() {
	 		if($("#change_of_address").is(":checked")) {
	 			$('.address-change').fadeIn();
	 		} else {
	 			$('.address-change').fadeOut();
	 		}
	 	});

	//first api hit, get state requirements
	$("input#get_started").click(function(event){
		event.preventDefault();
		$.ajax({
			type:"get",
			url:api_url+"/api/v1/state_requirements.json",
			data:{'home_zip_code':$("#pre_zip_code").val(),
						'lang':'en'},
			success:function(response){
				//load state-specific values
				
				//valid political parties
				for (i in response.party_list) {
					var party = response.party_list[i];
				}
				
				//required fields
				
				//id validation
				
				//sos contact info
				
				//do city, state lookup
				usps = zipLookup($('#pre_zip_code').val());
				
				//copy entered info over
				$('form#ovr #first_name').val($('form#get_started #first_name').val());
				$('form#ovr #last_name').val($('form#get_started #last_name').val());
				//$('form#ovr #home_zip_code').val($('form#get_started #zip_code').val());
				$('form#ovr #email_address').val($('form#get_started #email_address').val());
			},
			error:function(response){ console.log(response); }
		});
});

	//second api hit, send off registration
	$("input#register").click(function(event) {
		event.preventDefault();
		form_data = $('form#ovr').serializeJSON();
		
		//add data that doesn't yet have inputs
		form_data.lang='en';
		form_data.partner_id='1';
		form_data.home_state_id='1'; //need to determine this from the zipcode...
		
		//check required booleans
		var required_booleans = ['opt_in_email','opt_in_sms','us_citizen'];
		//and set unchecked fields to zero
		for (i in required_booleans) {
			field = required_booleans[i];
			if (form_data[field] == null) {
				form_data[field] = 0;
			}
		}
		
		console.log(form_data);
		
		$.ajax({
			type:"POST",
			url:api_url+"/api/v1/registrations.json",
			data:{'registration':form_data},
			cache:'false',
			success:function(response) {
				console.log(response);
			},
			complete:function() {
				console.log('complete');
			}
		});
	});

//setup dummy data, so we don't have to retype it every time
console.log('starting with example data');
$('#first_name').val('Jack');
$('#last_name').val('Smith');
$('#email_address').val('jack@example.com');
$('#zip_code').val('90210');
$('#name_title').val('Mr.');
$('#home_address').val('123 Example Rd');
$('#id_number').val('123-456-7890');
$('#date_of_birth').val('1979-10-24');


	//end document(ready)
});

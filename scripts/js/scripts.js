var hash = document.location.hash;
			
// Sets up the three UI templates.  Changing the hash tag in the URL switches the UI.

(function( $ ){
	$.fn.serializeJSON=function() {
		var json = {};
		jQuery.map($(this).serializeArray(), function(n, i){
			json[n['name']] = n['value'];
		});
		return json;
	};
})( jQuery );

$(document).ready(function() {
	//ui switch functionality
	if (hash === "#tab") {
		$('.tabs').tab('show');
		$('.tabs').show();
		$("form").addClass("tab-content");
		$("#tab-new, #tab-personal , #tab-additional, #tab-action").addClass("tab-pane");
		$("h1").removeAttr("data-toggle");
		$("#accordion-new, #accordion-personal, #accordion-additional, #accordion-action").removeClass("collapse");
		$("button.continue").removeAttr("data-toggle");
	} else if (hash === "#accordion") {
		$('.tabs').hide();
		$("#tab-link").removeAttr("data-toggle");
	
	} else {
		$('.tabs').hide();
		$("h1").removeAttr("data-toggle");
		$("#accordion-new, #accordion-personal, #accordion-additional, #accordion-action").removeClass("collapse");
		$("button.continue").hide();
	}
	
	//hide optional fields
	$(".mailing").hide();
	$(".name-change").hide();
	$(".address-change").hide();
	
	//show optional fields when necessary
	$("#has_mailing_address").click(function() {
		if($("#has_mailing_address").is(":checked")) {
			$('.mailing').slideDown();
		} else {
			$('.mailing').slideUp();
		}
	});
	$("#change_of_name").click(function() {
		if($("#change_of_name").is(":checked")) {
			$('.name-change').slideDown();
		} else {
			$('.name-change').slideUp();
		}
	});
	$("#change_of_address").click(function() {
		if($("#change_of_address").is(":checked")) {
			$('.address-change').slideDown();
		} else {
			$('.address-change').slideUp();
		}
	});
	
	//first api hit, get state requirements
	$("button#get_started").click(function(event){
		event.preventDefault();
		$.ajax({
			type:"get",
			url:"https://rtvdemo:bullwinkle@rtvstaging2.osuosl.org/api/v1/state_requirements.json",
			data:{'home_zip_code':$("#home_zip_code").val(),
						'lang':'en'},
			success:function(response){
				//load state values
				
				//valid political parties
				for (i in response.party_list) {
					var party = response.party_list[i];
					$('select#party').append("<option val="+party+">"+party+"</option>");
				}
				
				//requirements
				
				//id validation
				
				//
				
			},
			error:function(response){ console.log(response); }
		});
});
	
	//second api hit, send off registration
	$("button#register").click(function(event) {
		event.preventDefault();
		form_data = $('form#ovr').serializeJSON();
		//add data that doesn't yet have inputs
		form_data.lang='en';
		form_data.partner_id='1';
		form_data.partner_tracking_id='0';
		$.ajax({
			type:"post",
			url:"https://rtvdemo:bullwinkle@rtvstaging2.osuosl.org/api/v1/registrations.json",
			data:form_data,
			dataType:'jsonp',
			success:function(response) {
				console.log(response);
			},
			complete:function() {
				console.log('complete');
			}
		});
	});


/*	$(".tab-link").click(function() {
		var link = $(this).attr("href");
		$("a[href=" + link +"]").tab('show');
	});*/

	//end document(ready)
});

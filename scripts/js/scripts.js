	var hash = document.location.hash;
			
			// Sets up the three UI templates.  Changing the hash tag in the URL switches the UI.
			
			$(document).ready(function() {
				if (hash === "#tab") {
					$('.tabs').tab('show');  
					$('.tabs').show();
					$("form").addClass("tab-content");
					$("#tab-new, #tab-personal , #tab-additional, #tab-action").addClass("tab-pane");
					$("h1").removeAttr("data-toggle");
					$("#accordion-new, #accordion-personal, #accordion-additional, #accordion-action").removeClass("collapse");
					$("button.continue").removeAttr("data-toggle");
				} else if (hash === "#accordion") {
					$('.tabs').hide()
					$("#tab-link").removeAttr("data-toggle");
					
				} else {
					$('.tabs').hide();
					$("h1").removeAttr("data-toggle");
					$("#accordion-new, #accordion-personal, #accordion-additional, #accordion-action").removeClass("collapse");
					$("button.continue").hide();
			 	}
			 	
			 	$(".mailing").css("display","none");
			 	$(".name-change").css("display","none");
			 	$(".address-change").css("display","none");
			 	
			 	$("#has_mailing_address").click(function() {
			 		if($("#has_mailing_address").is(":checked")) {
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
			 	
			 	//Ajax request for the form.  
			 	
			 	$("#email_address").live("keyup", function(){
					$.ajax({
						type: "get",
						url: "https://rtvstaging2.osuosl.org/api/v1/state_requirements.json?lang=en&home_zip_code=94608",
						data: this.data,
						dataType: "jsonp",
						success: function(response){alert(response);},
						error: function(response){alert(response);},
						cache: false
					});
				});
			/*
	$("#accordion-group").live("click", function() {
					var url="https://rtvstaging2.osuosl.org/api/v1/registrations.json?callback=?";
					$.getJSON(url, function(data) {
						alert(data);
					});	
				});
*/
				
				
 				$(".tab-link").click(function() {
 					var link = $(this).attr("href");
			 		$("a[href=" + link +"]").tab('show');
			 		delete link;
			 	});	 		
			 		
			 	/* Don't delete this */
			 	});
		
			
			//tooltips

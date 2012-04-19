// TODO - Accordion Form

$(function() 


{
	if(document.location.hash==="#accordion") {
	
	$(".accordion-next").show();
	$(".accordion-hide").hide();
	$("input#get_started").click(function() {
	
		$(".accordion-content:not(:first)").hide();

		$(".accordion-next").click(function() {
			$(this).parent().parent().parent(this).children(".accordion-content").slideUp();
			console.log($(this).parent().parent().parent(this).next().children().slideDown());
			$(".tooltip_text").hide();
		});
		
		$(".accordion-prev").click(function() {
			$(this).parent().parent().parent(this).children(".accordion-content").slideUp();
			console.log($(this).parent().parent().parent(this).prev().children().slideDown());
			$(".tooltip_text").hide();
		});
		
		
	});
	} else {
		$(".accordion-next").hide();
		$(".accordion-prev").hide();
	}

		

	//when user clicks header, hides all other sections but one associated with that header (accordion-header)

});
	
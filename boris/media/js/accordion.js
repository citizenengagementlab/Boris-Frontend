// TODO - Accordion Form

$(function() 

{
	$("input#get_started").click(function() {
	
		$(".accordion-content:not(:first)").hide();
		$(".accordion-header").click(function() {
			$(".accordion-content").slideUp("slow");
			$(this).next().slideDown("slow");
		});
		$(".accordion-next").click(function() {
			$(this).parent().parent().parent(this).children(".accordion-content").slideUp();
			console.log($(this).parent().parent().parent(this).next().children().slideDown());
		});
		
		
		
	});
	

		

	//when user clicks header, hides all other sections but one associated with that header (accordion-header)

});
	
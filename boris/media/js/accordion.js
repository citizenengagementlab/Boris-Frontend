// TODO - Accordion Form

	
function accordion() {

	$("document").ready(function() {
		//hide tabs
		$("ul#tabnav").hide();
		//end
		//show continue and previous buttons
		$(".next-button, .prev-button").show();
		//Accordion functionality
		//Hide all but the first accordion section
		$(".accordion-content:not(:first)").hide();
		
		//Clicking the continue button closes the current section and opens the next.
		$(".next-button, input#get_started").click(function() {
			$(this).parent().parent().parent(this).children(".accordion-content").slideUp();
			$(this).parent().parent().parent(this).next().children().slideDown();
		});
		
		//Clicking the previous button closes the current sections and opens the previous.
		$(".prev-button").click(function() {
			$(this).parent().parent().parent(this).children(".accordion-content").slideUp();
			$(this).parent().parent().parent(this).prev().children().slideDown();
		});
	});
}

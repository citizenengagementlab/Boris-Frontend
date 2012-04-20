// TODO - Accordion Form

	
function accordion() {
	//hide tabs
	$("#tabnav").hide();
	$("#tabnav ul").hide();
	//end
	
	//show continue and previous buttons
	$(".next-button").show();
	$(".prev-button").show();

	//Accordion functionality
	$("input#get_started").click(function() {
		//Hide all but the first accordion section
		$(".accordion-content:not(:first)").hide();
		//Clicking the header closes or opens that particular section (buggy, and not really needed)
	/*
	$(".accordion-header").click(function() {
			$(".accordion-content").slideUp("slow");
			$(this).next().slideDown("slow");
		});
*/
		//Clicking the continue button closes the current section and opens the next.
		$(".next-button").click(function() {
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

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
		$(".accordion-header").click(function() {
			$(".accordion-content").slideUp("slow");
			$(this).next().slideDown("slow");
		});
		$(".next-button").click(function() {
			$(this).parent().parent().parent(this).children(".accordion-content").slideUp();
			$(this).parent().parent().parent(this).next().children().slideDown();
		});
		
		$(".prev-button").click(function() {
			$(this).parent().parent().parent(this).children(".accordion-content").slideUp();
			$(this).parent().parent().parent(this).prev().children().slideDown();
		});
	});
}

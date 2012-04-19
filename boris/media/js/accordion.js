// TODO - Accordion Form

	
function accordion() {	
	$("form ul").css("height","250px");
	
	$(".accordion-next").show();
	$(".accordion-prev").show();

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
}

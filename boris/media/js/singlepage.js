function singlepage() {
	$(".next-button").hide();
	$(".prev-button").hide();
	$("nav").hide();
	$("nav ul").hide();
	$("li.buttons").css("bottom","-10px"); // Keep register button from overlapping content
}
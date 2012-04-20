function singlepage() {
	$(".next-button").hide();
		$(".prev-button").hide();
		$("#tabnav").hide();
		$("#tabnav ul").hide();
		$("li.buttons").css("bottom","-10px"); // Keep register button from overlapping content
}
/* JS for Tooltip behavior */


// State Requirements forms

$("document").ready(function() {

//Hide tooltips on ready

	$(".tooltip_text").hide();

	$(".tooltip > a").hover(function() {
		$(this).next().show();
		}, function() { $(this).next().hide(); 
	});
	
	$("tooltip > a").click(function() {
		if($(this).next().is(!":visible")) {
			$(this).next().show();
		} else {
			$(this).next().hide();
		}
	});
});
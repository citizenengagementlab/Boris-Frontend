/* JS for Tooltip behavior */


// State Requirements forms

$("document").ready(function() {

//Hide tooltips on ready



/*
	$(".tooltip > a").hover(function() {
		$(this).next().show();
		}, function() { $(this).next().hide(); 
	});
*/
	
	$(".tooltip > a").toggle(function(e) {
		e.stopPropagation();
		$(this).next().show();
		$(".tooltip_text").not($(this).next()).hide();
		}, function() { 
		$(this).next().hide(); 
	});
	$(".tooltip_text").click(function(e) {
		$(this).toggle();
	});
});
/* Form Logic
*/((function(){})).call(this);



// Link back to the home page only shows up when the second page is loaded.

$("document").ready(function() {

	$("#top_link").hide();

	$("input#get_started").click(function() {
		$("#top_link").show();	
	});
});
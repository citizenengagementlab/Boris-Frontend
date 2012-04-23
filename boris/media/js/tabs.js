function tabs() {
	
	$("document").ready(function() {
		$(".accordion-content:not(:first)").hide();
		$("ul#tabnav").show();
		//show the first step as being active when the page loads
		$("ul#tabnav li a:first").addClass("tab-active");
		//hide accordion legends
		$(".accordion-header").hide();
		//show continue and go back buttons
		$(".next-button, .prev-button").show();
		
		$("ul#tabnav li a").click(function() {	
			$(this).addClass("tab-active");
			$("ul#tabnav li a").not($(this)).removeClass("tab-active");
			$(".accordion-content:visible").hide();
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();
		});
		
		$("input#get_started").click(function() {
			if(submitStartForm()) {
			//hide the current content
			$(this).parent().parent(this).hide();
			//show the next data-tab
			console.log($(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show());
			}
		});
	
		$(".next-button, input#get_started").click(function() {
			//hide the current content
			$(this).parent().parent(this).hide();
			//show the next data-tab, aka the next step in registration
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();
			//make the current tab inactive, by making them all inactive
			$("ul#tabnav li a").removeClass("tab-active");
			//make the next tab active
			$("ul#tabnav li a[data-tab=" + $(this).attr("data-tab") + "]").addClass("tab-active");
			
		});
	
		$(".prev-button").click(function() {
			//hide the current content
			$(this).parent().parent(this).hide();
			//show the next data-tab, aka the next step in registration
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();	
			//make the current tab inactive, by making them all inactive
			$("ul#tabnav li a").removeClass("tab-active");
			//make the next tab active
			$("ul#tabnav li a[data-tab=" + $(this).attr("data-tab") + "]").addClass("tab-active");
		});

	});
}
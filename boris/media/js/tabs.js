function tabs() {
	$("document").ready(function() {
	
		var buttons = '<input type="button" class="next-button" value="Continue" /><input type="button" data-tab="" class="prev-button" value="Go Back" />';
		//Hide all tabs except the first
		$(".accordion:not(:first)").hide();
		//Show the tab navigation 
		$("ul#tabnav").show();
		//show the first step as being active when the page loads
		$("ul#tabnav li a:first").addClass("tab-active");
		//hide accordion legends
		$(".accordion-header").hide();
		//html to be injected into each tab section
		

		//TODO: loop through each fieldset, append buttons to the bottom
		$("fieldset:not(:first)").each(function () {
			$(this).append(buttons);
		});		
	
		//TODO: How do I mix AJAX in with this
		$("input#get_started").click(function() {
			//Hide get_started fieldset
			$("fieldset#get_started").hide();
			//Show the next fieldset
			$("fieldset#address").show();
			//Remove all active states
			$("ul#tabnav li a").removeClass("tab-active");
			//Make the next tab active
			$("ul#tabnav li a#address").addClass("tab-active");
			
		}); 
		
	
		$(".next-button").click(function() {
			//hide the current content
			$(this).parent("fieldset").hide();
			//show the next content
			var $fieldsetNext = $(this).parent("fieldset").next("fieldset")
			$fieldsetNext.show();
			//make the current tab inactive, by making them all inactive
			$("ul#tabnav li a").removeClass("tab-active");
			//make the next tab active
			$("ul#tabnav li a").filter("#" + $fieldsetNext.attr("id")).addClass("tab-active");
		});
	
		$(".prev-button").click(function() {
			//hide the current content
			$(this).parent("fieldset").hide();
			//show the next data-tab, aka the next step in registration
			var $fieldsetPrev = $(this).parent("fieldset").prev("fieldset")
			$fieldsetPrev.show();
			//make the current tab inactive, by making them all inactive
			$("ul#tabnav li a").removeClass("tab-active");
			//make the next tab active
			$("ul#tabnav li a").filter("#" + $fieldsetPrev.attr("id")).addClass("tab-active");
		});
	});
}
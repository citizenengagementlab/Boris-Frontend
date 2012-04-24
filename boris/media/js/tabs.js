function tabs() {
	$("document").ready(function() {
	
		//Hide all tabs except the first
		$("legend:not(:first)").hide();
		//Show the tab navigation 
		$("nav").show();
		//show the first step as being active when the page loads
		$("nav li a:first").addClass("tab-active");
		//hide legends
		$("legend").hide();
		
		//html to be injected into each tab section
		var buttons = '<input type="button" class="next-button" value="Continue" /><input type="button" data-tab="" class="prev-button" value="Go Back" />';

		//loop through each fieldset, append buttons to the bottom
		$("fieldset:not(:first)").each(function () {
			var $fs = $(this);
			$fs.append(buttons);
			var id = $fs.attr('id');
			switch(id) {
				case 'address':
					$fs.children('.next-button').on('click', function(e){
						if (!validateAddresses())
							{return false;}
					});
					break;
				case 'personal':
					$fs.children('.next-button').on('click', function(e){
						if (!validatePersonal())
							{return false;}
					});
					break;
				case 'contact':
					$fs.children('.next-button').on('click', function(e){
						if (!validateContact())
							{return false;}
					});
					break;
				case 'additional':
					$fs.children('.next-button').on('click', function(e){
						if (!validateAdditional())
							{return false;}
					});
					break;
				default:
					return false;
			}
		});		
	
		//BUT hide the Continue button on the last section.
		$("fieldset#additional").find("input.next-button").hide();
		
		
		$("input#get_started").click(function() {
			//Hide get_started fieldset
			$("fieldset#get_started").hide();
			//Show the next fieldset
			$("fieldset#address").show();
			//Remove all active states
			$("nav li a").removeClass("tab-active");
			//Make the next tab active
			$("nav li a#address").addClass("tab-active");
			
		}); 
		
		$("fieldset#address .prev-button").click(function() {
			$("fieldset#address").hide();
			//Show the next fieldset
			$("fieldset#get_started").show();
			//Remove all active states
			$("nav li a").removeClass("tab-active");
			//Make the next tab active
			$("nav li a#address").addClass("tab-active");
		});
	
		$(".next-button").click(function() {
			//hide the current content
			$(this).parent("fieldset").hide();
			//show the next content
			var $fieldsetNext = $(this).parent("fieldset").next("fieldset");
			$fieldsetNext.show();
			//make the current tab inactive, by making them all inactive
			$("nav li a").removeClass("tab-active");
			//make the next tab active
			$("nav li a").filter("#" + $fieldsetNext.attr("id")).addClass("tab-active");
		});
	
		$(".prev-button").click(function() {
			//hide the current content
			$(this).parent("fieldset").hide();
			//show the next data-tab, aka the next step in registration
			var $fieldsetPrev = $(this).parent("fieldset").prev("fieldset");
			$fieldsetPrev.show();
			//make the current tab inactive, by making them all inactive
			$("nav li a").removeClass("tab-active");
			//make the next tab active
			$("nav li a").filter("#" + $fieldsetPrev.attr("id")).addClass("tab-active");
		});
	});
	
}
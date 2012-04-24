function accordion() {
	$("document").ready(function() {
		var buttons = '<input type="button" class="next-button" value="Continue" /><input type="button" data-tab="" class="prev-button" value="Go Back" />';
		
		//hide tabs
		$("nav").hide();
		//show all accordions
		$("legend").show();
		
		//append buttons to each fieldset
		$("fieldset:not(:first)").each(function () {
			$(this).append(buttons);
		});
		//Accordion functionality
		//Hide all but the first fieldset
		$("fieldset:not(:first)").hide();
		
		$("input#get_started").click(function() {
			if (!validateStartFields()) {
				//Hide get_started fieldset
				$("fieldset#get_started").hide();
				//Show the next fieldset
				$("fieldset#address").show();
			}
		});
		
		//Clicking the continue button closes the current section and opens the next.
		$(".next-button").click(function() {
			var $fieldsetThis = $(this).parents("fieldset");
			var $fieldsetNext = $fieldsetThis.next("fieldset");
			console.log($fieldsetNext);
			$fieldsetNext.slideUp();
			$fieldsetThis.slideDown();
		});
		
		//Clicking the previous button closes the current sections and opens the previous.
		$(".prev-button").click(function() {
			var $fieldsetThis = $(this).parents("fieldset");
			var $fieldsetPrev = $fieldsetThis.prev("fieldset");
			console.log($fieldsetPrev);
			$fieldsetThis.slideUp();
			$fieldsetPrev.slideDown();
		});
	});
}

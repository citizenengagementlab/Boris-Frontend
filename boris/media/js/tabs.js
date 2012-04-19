function tabs() {
	$("input#get_started").click(function() {
		$(".accordion-content").css("height","260px");
		$(".accordion-content:not(:first)").hide();
		$("#tabnav").show();
		$("#tabnav ul").show();
		$("#tabnav ul a:first").css("color", "#AAA");
		$(".next-button").show();
		$(".prev-button").show();
		$(".accordion-header").hide();
		$("#tabnav ul a").click(function() {	
			$(this).css("color", "#AAA");
			$("#tabnav ul a").not($(this)).css("color", "#FFF");
			$(".accordion-content:visible").hide();
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();
		});
		
		$(".next-button").click(function() {
			$(this).parent().parent(this).hide();
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();
			$("#tabnav ul a").css("color","#FFF");
			$("#tabnav ul a[data-tab=" + $(this).attr("data-tab") + "]").css("color", "#AAA");
			
		});
	
		$(".prev-button").click(function() {
			$(this).parent().parent(this).hide();
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();	
		
		});
	});
}


/*button behavior

			
		$(".prev-button").click(function() {
			$(this).parent().parent().parent(this).children(".accordion-content").slideUp();
			$(this).parent().parent().parent(this).prev().children().slideDown();
		});
		
		*/
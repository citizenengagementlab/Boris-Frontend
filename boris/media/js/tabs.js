function tabs() {
	$("input#get_started").click(function() {
		$(".accordion-content:not(:first)").hide();
		$("#tabnav").show();
		$("#tabnav ul").show();
		$("#tabnav ul a:first").addClass("tab-active");
		$(".next-button").show();
		$(".prev-button").show();
		$(".accordion-header").hide();
		$("#tabnav ul a").click(function() {	
			$(this).addClass("tab-active");
			$("#tabnav ul a").not($(this)).removeClass("tab-active");
			$(".accordion-content:visible").hide();
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();
		});
		
		$(".next-button").click(function() {
			$(this).parent().parent(this).hide();
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();
			$("#tabnav ul a").removeClass("tab-active");
			$("#tabnav ul a[data-tab=" + $(this).attr("data-tab") + "]").addClass("tab-active");
			
		});
	
		$(".prev-button").click(function() {
			$(this).parent().parent(this).hide();
			$(".accordion-content[data-content=" + $(this).attr("data-tab") + "]").show();	
			$("#tabnav ul a").removeClass("tab-active");
			$("#tabnav ul a[data-tab=" + $(this).attr("data-tab") + "]").addClass("tab-active");
		
		});
	});
}



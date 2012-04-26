/* JS for Tooltip behavior */

$("document").ready(function() {
	$(".tooltip > a").on('click',
		function(e) {
			e.stopPropagation();
			$(this).next().show();
			$(".tooltip > a").not($(this)).next().hide();
			$('body').on('click',
				function(e) {
					$('.tooltip_text:visible').hide();
					$(this).off('click');
				});
			return false;
		}
	);
});
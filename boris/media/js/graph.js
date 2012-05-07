//Todo: Should we normalize this??  How do we do that since there there isn't validation between sections on the single page element?

var lookupTable = ["home_address", "home_zip_code", "has_mailing_address","mailing_address","mailing_city","mailing_state_id","mailing_zip_code", "change_of_address","prev_address","prev_city","prev_state_id","prev_zip_code","name_title","first_name","last_name","change_of_name","prev_name_title","prev_first_name","prev_last_name","id_number","date_of_birth","opt_in_email","phone","phone_type","opt_in_sms","race", "party","us_citizen","finished"];
				
var progress_tabs;
var progress_accordion;
var progress_singlepage;



$(function() {  
	
	//Generates ticks for the x-axis [works]
	function makeTicks(array) {
	var ticks = [];
	for(i=0;i<lookupTable.length;i++) {
		ticks.push([i+1,lookupTable[i]]);
	}
	return ticks;		
}
	
	//Takes in an unsorted object 
	function lookupCheck(object) {
		var i = 1;
		var sortedData = [];
		for (var prop in lookupTable) {
			if(object[lookupTable[prop]] === undefined) {
				sortedData.push([i, 0]);
			} else {
				sortedData.push([i, object[lookupTable[prop]]]);
			}
			i++;
		}
		return sortedData;
	};
	
	
	var single_data = lookupCheck(progress_singlepage);
	var tabbed_data = lookupCheck(progress_tabs);
	var accord_data = lookupCheck(progress_accordion); 
	
	
		
	//Data Constructor, takes in a label, data, and color

	var Data = function(label, data, color) {
		this.label = label;
		this.data = data;
		this.color = color;
	}						  
					  
	//Let's make our dataplot objects
	var singleData = new Data("Single Form", single_data, '#409628');
	var tabbedData = new Data("Tabbed Form", tabbed_data, '#2918DB');
	var accordionData = new Data("Accordion Form", accord_data, '#988166');	
	
	//Make ticks 
	var ticks = makeTicks(lookupTable);
	 
	//Settings
	var options = {  
		selection: {
			 mode: "xy" },
        grid: { 
        	hoverable: true, 
        	clickable: true },
	    legend: {  
	        show: true,  
	        margin: 10,  
	        backgroundOpacity: 0.5  
	    },
	    series: {
	    	bars: {
	    		show: true, 
	    		barWidth: 0.45, 
	    		align: 'center'},
	    },		
	    xaxis: { 
	    	ticks: ticks
	    		}
	  }   
	  
	var allData = [singleData, tabbedData, accordionData];
	 
	//Set up our graph
    var allPlot = $("#graph_all");  
    $.plot( allPlot , allData, options )   
    
    var singlePlot = $("#graph_singlepage");  
    $.plot( singlePlot , [singleData], options )   
    
    var tabbedPlot = $("#graph_tabbed");  
    $.plot( tabbedPlot , [tabbedData] , options )
    
    var accordionPlot = $("#graph_accordion");  
    $.plot( accordionPlot , [accordionData] , options ) 
    
    //Settings 



});
    
